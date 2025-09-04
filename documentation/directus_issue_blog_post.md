# A Deep Dive into a Directus Schema Migration Mystery

## The Goal: A Reproducible Backend for Our Frontend

As part of developing a proof-of-concept, we aimed to set up a Directus backend that mirrors the data structures of our existing frontend. A key requirement for this project was to have a reliable, automated, and repeatable process for setting up the database schema. This would allow any developer to spin up a consistent environment with a single command.

## The Setup

Our development environment is as follows:

*   **OS:** Windows 11
*   **Virtualization:** Docker Desktop
*   **Project Management:** Node.js with npm
*   **Directus:** Running via Docker, initially with `directus/directus:latest`, and later with `directus/directus:10.8.3`.
*   **Database:** SQLite, managed within the Docker container.

## The Journey: Two Paths, One Destination (Failure)

We embarked on two primary strategies to automate the schema creation, both of which led us down a rabbit hole of troubleshooting.

### Path 1: The Node.js SDK Script

Our first approach was to leverage the official Directus SDK (`@directus/sdk`) to write a Node.js script that would programmatically create our collections, fields, and relations.

This path was fraught with challenges:

1.  **Module System Mismatch:** We initially wrote the script using modern ES Module `import` syntax. However, our Node.js environment was configured for CommonJS, leading to a `SyntaxError`. We then tried to force the module system by adding `"type": "module"` to our `package.json`, but this led to a cascade of `MODULE_NOT_FOUND` errors.

2.  **Module Resolution Failure:** After reverting to CommonJS `require` syntax, we continued to face `MODULE_NOT_FOUND` errors. Even after a clean install of our dependencies (`rm -rf node_modules package-lock.json && npm install`), the script was unable to locate the `@directus/sdk` package.

3.  **The `TypeError: Directus is not a constructor` Puzzle:** After numerous attempts to resolve the module issues, we finally hit a wall with a `TypeError`. This indicated that the way we were importing the `Directus` class was incompatible with the SDK's structure in our environment. We tried every conceivable import syntax (`require('@directus/sdk')`, `require('@directus/sdk').default`, etc.), but to no avail.

### Path 2: The "Official" Way - Schema Migrations

Frustrated with the Node.js script, we pivoted to what we believed would be a more robust and officially supported method: using a YAML file to define the schema and applying it with the `directus schema apply` command.

This path, too, had its own set of obstacles:

1.  **File Not Found:** Our first attempt failed with an `ENOENT` error. The fix was simple: we needed to mount our local `migrations` directory as a volume in the `docker-compose.yml` file so the Directus container could access the `schema.yml` file.

2.  **Invalid Data Type:** We then encountered a payload error: `Illegal type passed: "datetime"`. This was a straightforward fix; we corrected our `schema.yml` to use the valid `timestamp` type.

3.  **Structural Schema Errors:** Next, we were met with a `NOT_NULL_VIOLATION` on the `directus_fields` collection. This indicated a problem with the structure of our YAML file. We corrected this by nesting our field definitions directly under their corresponding collections.

4.  **The Final Boss: `TypeError: Cannot read properties of undefined (reading 'filter')`:** This is where our journey came to a halt. Even with a valid schema file, the `directus schema apply` command would consistently fail with this error.

To ensure the problem wasn't with our configuration, we performed a **complete environment reset**:

*   We stopped and removed the Docker container.
*   We deleted the local `database` and `uploads` volumes.
*   We switched from the `latest` Docker image to a specific, stable version (`10.8.3`).
*   We re-initialized the container and created a fresh admin user.
*   We attempted to apply a **highly simplified** `schema.yml` file with only a handful of collections and basic fields.

The `filter` error persisted.

## The Conclusion: A Bug in the CLI

After systematically eliminating every possible configuration error, we have concluded that the `directus schema apply` CLI command is buggy or incompatible with the environment provided by the official Directus Docker images. The error occurs deep within the CLI's internal logic and is not something that can be fixed through user configuration.

## The Workaround: The HTTP API

The most reliable path forward is to bypass the CLI entirely and use a Node.js script to apply the schema via the Directus HTTP API. This approach is more stable and is the recommended method for production deployments.

We hope this detailed account of our troubleshooting journey will be helpful to the Directus community and the Directus team in resolving this issue.