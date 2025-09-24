import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, AsyncGenerator, List, Optional

import httpx
import yaml
from .nested_query_string import NestedQueryString
from pydantic import BaseModel

from .constants import (
    HTTP_DELETE,
    HTTP_GET,
    HTTP_NO_CONTENT_CODE,
    HTTP_OK_CODE,
    HTTP_POST,
    HTTP_PUT,
    HTTP_SEARCH,
)
from .errors import *
from .models import DirectusFile

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AsyncDirectusClient:
    def __init__(
        self,
        base_url: str,
        auth_token: str,
        default_headers: Optional[dict] = None,
    ):
        """
        @param base_url: must not end with / (e.g. https://api.thailandboattickets.nl)
        @param auth_token: will be used in property bearer_header
        @param api_prefix: must start with / and not end with / (e.g. /v2, or /api, or /api/v2, etc)
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.default_headers = default_headers or {"Content-Type": "application/json"}
        self._client: Optional[httpx.AsyncClient] = httpx.AsyncClient(timeout=30.0)

        if self.base_url.endswith("/"):
            raise InvalidBaseUrlError("Base URL must not end with /")

    @staticmethod
    def encode_json_func(val):
        if isinstance(val, datetime.datetime):
            return val.isoformat()
        return val.model_dump() if isinstance(val, BaseModel) else str(val)

    def _construct_url(
        self, path_or_endpoint: str = None, prefix: Optional[str] = None
    ) -> str:
        if path_or_endpoint.startswith("http"):
            # path is an url
            return path_or_endpoint

        url = self.base_url

        if prefix:
            url += "/" + prefix.removeprefix("/")

        path_or_endpoint = path_or_endpoint.removeprefix("/")
        return f"{url}/{path_or_endpoint}"

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client instance."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client

    def _parse_response(
        self, http_method: str, response: httpx.Response, **kwargs
    ) -> Optional[dict]:
        """Parse API response and handle errors."""
        try:
            if response.status_code in {HTTP_OK_CODE, HTTP_NO_CONTENT_CODE}:
                return response.json() if response.content else None
            return self._on_error(response, http_method)
        except json.JSONDecodeError:
            if response.content:
                logger.warning(
                    f"{http_method} request returned non-JSON content: {response.text}"
                )
                return response.text
            logger.info(f"{http_method} request successful, no content returned")
            return None

    def _get_request_headers(self) -> dict:
        # override this in your subclass
        try:
            return {**self._get_bearer_header, **self.default_headers, "sv": "is.cool"}
        except MissingAuthTokenError:
            return self.default_headers

    def _on_error(self, response: httpx.Response, method) -> None:
        # override this in your subclass or remove this at all ?
        msg = (
            f"HTTP error. Method {method} - "
            f"Status code {response.status_code} - "
            f"Body {response.text} - "
            f"URL {response.url}"
        )
        logger.error(msg)
        response.raise_for_status()
        return response.json() if response.content else None

    @property
    def _get_bearer_header(self) -> dict:
        if not self.auth_token:
            logger.error("Missing auth token")
            raise MissingAuthTokenError("Missing auth token")
        return {"Authorization": f"Bearer {self.auth_token}"}

    @staticmethod
    def __prepare_json(data) -> str:
        return json.dumps(data, default=AsyncDirectusClient.encode_json_func)

    async def _get(
        self,
        path: str,
        params: Optional[dict] = None,
        prefix: Optional[str] = None,
        **kwargs,
    ):
        url = self._construct_url(path, prefix=prefix)
        headers = self._get_request_headers()
        if params is not None:
            params = NestedQueryString.encode(params)

        response = await self.client.get(url, params=params, headers=headers, **kwargs)

        if response.status_code != HTTP_OK_CODE:
            return self._on_error(response, HTTP_GET)

        return self._parse_response(HTTP_GET, response)

    async def _post(
        self, path: str, data: dict[str, Any], prefix: Optional[str] = None, **kwargs
    ):
        url = self._construct_url(path, prefix=prefix)
        headers = self._get_request_headers()

        response = await self.client.post(
            url, data=self.__prepare_json(data), headers=headers, **kwargs
        )

        if response.status_code != HTTP_OK_CODE:
            return self._on_error(response, HTTP_POST)

        return self._parse_response(HTTP_POST, response)

    async def _delete(
        self,
        path: str,
   
        params: Any = None,
        prefix: Optional[str] = None,
        **kwargs,
    ) -> Any:
        url = self._construct_url(path, prefix=prefix)
        headers = self._get_request_headers()
        if params is not None:
            params = NestedQueryString.encode(params)

        response = await self.client.delete(
            url, params=params, headers=headers, **kwargs
        )
        if response.status_code in {HTTP_OK_CODE, HTTP_NO_CONTENT_CODE}:
            return self._parse_response(HTTP_DELETE, response) if response else response
        else:
            return self._on_error(response, HTTP_DELETE)

    async def _patch(self, path, data, params=None, prefix: Optional[str] = None, **kwargs):
        url = self._construct_url(path, prefix=prefix)
        headers = self._get_request_headers()
        if params is not None:
            params = NestedQueryString.encode(params)

        data = self.__prepare_json(data)
        response = await self.client.patch(
            url, data=data, headers=headers, params=params, **kwargs
        )
        if response.status_code not in [HTTP_OK_CODE, HTTP_NO_CONTENT_CODE]:
            return self._on_error(response, HTTP_PUT)
        return self._parse_response(HTTP_PUT, response)

    async def get_schema_snapshot(self):
        snapshot = await self._get("schema/snapshot")
        return snapshot

    def items(self, collection):
        return CollectionWrapper(self, collection)

    @property
    def files(self):
        return FileWrapper(self)

    # TODO
    # def dump_collection(self, collection_name: str, export_name: str) -> None:
    #     """Dumps a single collection to a jsonlines file"""
    #     items = self.items(collection_name).list(paginate=True)
    #     if not items.get("data"):
    #         logger.warning(f"No data found for collection: {collection_name}")
    #         return
    #
    #     write_jsonlines(collection_name, items["data"], export_name)
    #     logger.info(f"Exported {len(items['data'])} items from {collection_name}")
    #
    # def load_collection(self, collection_name: str, export_name: str) -> None:
    #     """Loads a collection from a jsonlines file"""
    #     items = read_jsonlines(collection_name, export_name)
    #     if not items:
    #         return
    #
    #     for item in items:
    #         self.items(collection_name).create(item)
    #
    #     logger.info(f"Imported {len(items)} items to collection: {collection_name}")

    # def export_from_config(self, config_path: str, export_name: str) -> None:
    #     """Export collections based on YAML config file"""
    #     with open(config_path) as f:
    #         config = yaml.safe_load(f)
    #
    #     collections = config.get("collections", [])
    #     if not collections:
    #         raise ValueError("No collections specified in config file")
    #
    #     for collection_name in collections:
    #         self.dump_collection(collection_name, export_name)
    #
    # def import_from_config(self, config_path: str, export_name: str) -> None:
    #     """Import collections based on YAML config file"""
    #     with open(config_path) as f:
    #         config = yaml.safe_load(f)
    #
    #     collections = config.get("collections", [])
    #     if not collections:
    #         raise ValueError("No collections specified in config file")
    #
    #     for collection_name in collections:
    #         self.load_collection(collection_name, export_name)
    #


class CollectionWrapper:
    def __init__(self, client: AsyncDirectusClient, collection: str):
        self.client = client
        self.collection = collection

    async def list(
        self,
        fields: Optional[List[str]] = None,
        sort: Optional[List[str]] = None,
        filter: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        iterate_pages: Optional[bool] = False,
        **kwargs,  # For any other Directus parameters not explicitly listed
    ) -> List[dict]:
        
        items = []
        async for item in self.list_generator(
            fields=fields,
            sort=sort,
            filter=filter,
            limit=limit,
            offset=offset,
            iterate_pages=iterate_pages,
            **kwargs,
        ):
            items.append(item)
        return items

    async def list_generator(
        self,
        fields: Optional[List[str]] = None,
        sort: Optional[List[str]] = None,
        filter: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        page: Optional[int] = None,
        deep: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        iterate_pages: Optional[bool] = False,
        **kwargs,  # For any other Directus parameters not explicitly listed
    ) -> AsyncGenerator[dict, None]:
        """
        Lists items in the collection.

        Parameters:
            fields: List of fields to include (e.g., ['title', 'author.name']).
            sort: List of fields to sort by (e.g., ['-date_created', 'title']). Prefix with '-' for descending order.
            filter: Dictionary representing the filter criteria.  Use nested dictionaries for relational filters.
            limit: Maximum number of items to return.
            offset: Number of items to skip.
            page: Page number (1-based). Used in conjunction with 'limit'.
            deep: Nested relational structure (see Directus docs).
            search: Search term to filter by.
            **kwargs: Any other Directus API parameters not explicitly listed above.

        For detailed information on filtering, sorting, and other parameters,
        refer to the Directus API documentation.

        Example usage:
            items = client.items('articles').list(fields=['title', 'author.name'], sort=['-date_created'], limit=20, page=2)
            items = client.items('articles').list(filter={'status': 'published'}, search='keyword')

        """
        path = f"{self.collection}"

        if limit is None:
            limit = 25
        if page is None:
            page = 1

        params = {
            "page": page,
            "limit": limit,
        }

        if fields:
            params["fields"] = fields

        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if deep:
            params["deep"] = deep
        if search:
            params["search"] = search

        params.update(kwargs)  # Add any additional kwargs to the params dict

        result = await self.client._get(path, params=params, prefix="items")
        items = result["data"]

        if not iterate_pages:
            for i in items:
                yield i
            return

        for item in items:
            yield item

        while len(items) >= limit:
            params["page"] = params["page"] + 1
            result = await self.client._get(path, params=params, prefix="items")
            items = result["data"]
            for item in items:
                yield item

        return

    async def find_first(
        self,
        fields: Optional[List[str]] = None,
        sort: Optional[List[str]] = None,
        filter: Optional[Dict[str, Any]] = None,
        page: Optional[int] = None,
        deep: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        **kwargs,  # For any other Directus parameters not explicitly listed
    ) -> dict | None:
        find_args = dict(
            fields=fields,
            sort=sort,
            filter=filter,
            page=page,
            deep=deep,
            search=search,
            limit=1,
        )
        find_args.update(kwargs)

        async for i in self.list_generator(**find_args):
            return i
        return None

    async def create(self, data: dict[str, Any]):
        path = f"{self.collection}"
        result = await self.client._post(path, data=data, prefix="items")
        data = result["data"]
        return data

    async def get(self, id: str, fields: Optional[List[str]] = None):
        params = {}
        if fields:
            params["fields"] = fields
        path = f"{self.collection}/{id}"
        result = await self.client._get(path, params=params, prefix="items")
        data = result["data"]
        return data

    async def update(self, id: str, data: dict[str, Any]):
        path = f"{self.collection}/{id}"
        result = await self.client._patch(path, data, prefix="items")
        data = result["data"]
        return data

    async def delete(self, id: str):
        path = f"{self.collection}/{id}"
        return await self.client._delete(path=path, prefix="items")

    async def delete_many(self, filter: dict[str, Any] = None, limit: int = None):
        path = f"{self.collection}"
        args = {"query": {}}
        if filter:
            args["query"]["filter"] = filter
        if limit:
            args["query"]["limit"] = limit
        return await self.client._delete(path=path, prefix="items", data=args)

    async def update_many(self, data, query=None, ids=None):
        path = f"{self.collection}"
        args = {
            'data': data,
        }
        if query:
            args['query'] = query
        if ids:
            args['keys'] = ids

        print(args)
        result = await self.client._patch(path, args, prefix="items")
        data = result["data"]
        return data

    

class FileWrapper:
    def __init__(self, client: AsyncDirectusClient):
        self.client = client

    async def upload(
        self,
        file,
        filename: Optional[str] = None,
        mime_type: str = "application/pdf",
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        location: Optional[str] = None,
        filename_disk: Optional[str] = None,
        filename_download: Optional[str] = None,
        filesize: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        duration: Optional[int] = None,
        folder: Optional[str] = None,
        embed: Optional[str] = None,
        focal_point_x: Optional[int] = None,
        focal_point_y: Optional[int] = None,
        uploaded_by: Optional[str] = None,
        uploaded_on: Optional[str] = None,
        **kwargs,
    ):
        endpoint = "files"
        if isinstance(file, str) or isinstance(file, Path):
            filepath = Path(file)
            if not filepath.exists():
                raise InvalidFileParamsError(f"File does not exist {file}")
            filename = filepath.name
            file = open(file, "rb")

        if filename is None:
            raise InvalidFileParamsError("Provide filename.")

        url = f"{self.client.base_url}/{endpoint}"
        headers = self.client._get_request_headers()

        data = {
            "filename": filename,
            "filename_disk": filename_disk,
            "filename_download": filename_download,
            "title": title,
            "description": description,
            "tags": tags,
            "location": location,
            "filesize": filesize,
            "width": width,
            "height": height,
            "duration": duration,
            "folder": folder,
            "embed": embed,
            "focal_point_x": focal_point_x,
            "focal_point_y": focal_point_y,
            "uploaded_by": uploaded_by,
            "uploaded_on": uploaded_on,
            **kwargs,
        }

        del headers["Content-Type"]
        files = {"file": (filename, file, mime_type)}
        response = await self.client.client.post(url, data=data, headers=headers, files=files)

        if response.status_code != HTTP_OK_CODE:
            return self.client._on_error(response, HTTP_POST)

        result = self.client._parse_response(HTTP_POST, response)
        return DirectusFile(**result["data"])

    async def download(self, id: str, output_path: str) -> str:
        download_url = f"{self.client.base_url}/assets/{id}"
        headers = self.client._get_request_headers()
        
        async with self.client.client.stream("GET", download_url, headers=headers) as file_response:
            file_response.raise_for_status()
            
            with open(output_path, "wb") as f:
                async for chunk in file_response.aiter_bytes(chunk_size=8192):
                    f.write(chunk)

        return output_path
