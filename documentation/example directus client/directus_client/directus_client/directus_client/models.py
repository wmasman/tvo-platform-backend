from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel


class DirectusFile(BaseModel):
    id: str = None
    storage: Optional[str] = None
    filename_disk: Optional[str] = None
    filename_download: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    folder: Optional[str] = None
    uploaded_by: Optional[str] = None
    created_on: Optional[datetime] = None
    modified_by: Optional[str] = None
    modified_on: Optional[datetime] = None
    charset: Optional[str] = None
    filesize: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    embed: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[Any] = None
    metadata: Optional[Any] = None
    focal_point_x: Optional[float] = None
    focal_point_y: Optional[float] = None
    tus_id: Optional[str] = None
    tus_data: Optional[Any] = None
    uploaded_on: Optional[datetime] = None
