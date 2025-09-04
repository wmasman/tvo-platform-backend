# Summary of Directus Schema Automation Issues

## Objective

The primary goal was to set up a proof-of-concept backend using Directus. A key requirement was to automate the creation of the database schema based on the frontend's data structures to ensure a reliable and repeatable process.

## Core Problem

We have been unable to automate the creation of the Directus schema. We attempted two different methods—a custom Node.js script using the Directus SDK and the built-in `schema apply` command with a YAML file. Both approaches ultimately failed due to a series of persistent and evolving errors.

The final, blocking error is a `TypeError: Cannot read properties of undefined (reading 'filter')` that originates from within the Directus command-line interface (CLI) when trying to apply a schema snapshot. This error occurred even after a complete environment reset and with a simplified schema, which strongly suggests a bug within the Directus CLI tool itself rather than a problem with our configuration.

## Detailed Troubleshooting History

### Approach 1: Custom Node.js Script (`setup.js`)

Our first strategy was to write a Node.js script to create the collections and fields programmatically using the Directus SDK.

1.  **Initial `SyntaxError`:** The script was written with modern ES Module `import` syntax but the Node.js environment was configured for CommonJS.
    *   **Fix 1:** We added `"type": "module"` to `package.json`. This led to a `MODULE_NOT_FOUND` error, as Node.js could not resolve the `@directus/sdk` package.
    *   **Fix 2:** We reverted to CommonJS by removing `"type": "module"` and changing the script to use `require`. This also resulted in a `MODULE_NOT_FOUND` error.
    *   **Fix 3:** We performed a clean install by deleting `node_modules` and `package-lock.json` and running `npm install` again. The module resolution errors persisted.

2.  **`TypeError: Directus is not a constructor`:** After several attempts to fix the module resolution, we encountered errors indicating that the `Directus` class was not being imported correctly. We tried multiple import syntaxes (`const { Directus } = require('@directus/sdk')`, `const { Directus } = require('@directus/sdk').default`, etc.), but each resulted in a similar `TypeError`.

This led us to abandon the custom script in favor of the official schema migration tools.

### Approach 2: Directus Schema Migrations (`schema.yml`)

We switched to the recommended approach of using a YAML file to define the schema and applying it with the `directus schema apply` command.

1.  **`ENOENT: no such file or directory`:** The first attempt failed because the CLI, running inside the Docker container, could not access the local `schema.yml` file.
    *   **Fix:** We updated the `docker-compose.yml` to mount the local `./migrations` directory as a volume at `/directus/migrations` inside the container and restarted the container. This successfully resolved the file access issue.

2.  **`Invalid payload. Illegal type passed: "datetime"`:** The schema failed to apply because we used an incorrect data type.
    *   **Fix:** We corrected the `schema.yml` file, replacing all instances of `datetime` with the valid Directus type `timestamp`.

3.  **`Value for field "collection" in collection "directus_fields" can't be null`:** This error indicated a structural problem in the `schema.yml` file.
    *   **Fix:** We restructured the YAML file to nest the `fields` definitions directly under their corresponding `collections`, which is a more explicit and robust format.

4.  **`TypeError: Cannot read properties of undefined (reading 'filter')`:** This is the final, persistent error. It occurs within the Directus CLI's internal `getSnapshotDiff` utility.
    *   **Diagnosis:** To isolate the cause, we performed a **full reset of the Directus environment**:
        1.  Stopped and removed the Docker container (`docker-compose down`).
        2.  Deleted the local `database` and `uploads` volumes to ensure a clean slate.
        3.  Updated the `docker-compose.yml` to use a specific, stable version of Directus (`10.8.3`) instead of `latest`.
        4.  Recreated and re-initialized the container.
        5.  Attempted to apply a **highly simplified** `schema.yml` file containing only collection definitions and a few basic fields.
    *   **Result:** The `filter` error persisted even on a completely fresh instance with a minimal schema.

## Final Conclusion

The evidence strongly suggests that the `directus schema apply` CLI command is buggy or incompatible with the environment provided by the official Directus Docker images (both `latest` and `10.8.3`). The error occurs deep within the CLI's internal logic and persists even after a full environment reset and with a valid, simplified schema.

The most reliable path forward is to bypass the CLI for schema management and either:
1.  Create the schema manually through the Directus admin interface.
2.  Use a script to apply the schema via the Directus HTTP API, which is known to be more stable.