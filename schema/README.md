# Directus Schema Management

This directory contains the tools for managing the Directus schema in a reliable and automated way.

## How it Works

The `apply_schema.js` script is the core of this system. It reads the `migrations/schema_fixed.yml` file and syncs the Directus database schema to match it. This means:

*   **Collections** that exist in the YAML file but not in Directus will be created.
*   **Fields** that exist in the YAML file but not in Directus will be created.
*   **Collections** that exist in Directus but not in the YAML file will be **deleted**.
*   **Fields** that exist in Directus but not in the YAML file will be **deleted**.

This makes the `migrations/schema_fixed.yml` file the single source of truth for your schema.

## How to Use

1.  **Start Directus:** Make sure the Directus container is running.
    ```powershell
    cd directus
    docker-compose up -d
    ```

2.  **Install Dependencies:**
    ```powershell
    cd directus/schema
    npm install
    ```

3.  **Apply the Schema:**
    ```powershell
    cd directus/schema
    npm run schema:apply