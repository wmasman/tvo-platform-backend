# Directus Proof of Concept

This directory contains a proof-of-concept for a new application backend using Directus.

## Automated Schema Management

A key feature of this proof-of-concept is the automated schema management system. The schema for the Directus instance is defined in the `schema/migrations/schema_fixed.yml` file. This file is the single source of truth for the database schema.

To apply the schema, navigate to the `schema` directory and run the following command:

```powershell
npm run schema:apply
```

This script will automatically create, update, or delete collections and fields to match the schema defined in the YAML file.

For more detailed information, see the `README.md` file in the `schema-tool` directory.

## Fly.io and Neon Postgres Deployment

This project is configured for deployment to Fly.io with a Neon Postgres database.

### Prerequisites

*   [flyctl](https://fly.io/docs/hands-on/install-flyctl/) installed
*   A Fly.io account
*   A Neon account

### Deployment Steps

1.  **Create a Neon Postgres Database:**
    *   Go to [neon.tech](https://neon.tech/) and create a new project.
    *   In the project dashboard, find your connection string. It will look something like this: `postgres://user:password@host:port/dbname`.

2.  **Login to Fly.io:**
    ```powershell
    fly auth login
    ```

3.  **Launch the app:**
    ```powershell
    fly launch --no-deploy
    ```

4.  **Create a volume:**
    ```powershell
    fly volumes create directus_uploads --region ams --size 1
    ```

5.  **Set up Neon MCP Server (Optional):**
    *   Follow the instructions in the image to set up the Neon MCP server in your VS Code settings. This will allow you to manage your database directly from your editor.

6.  **Set secrets:**
    *   Replace the placeholder with your Neon connection string.
    ```powershell
    fly secrets set KEY="your-strong-random-key" SECRET="your-strong-random-secret" ADMIN_EMAIL="wmasman@gmail.com" ADMIN_PASSWORD="password" DB_CONNECTION_STRING="your-neon-connection-string"
    ```

7.  **Deploy:**
    ```powershell
    fly deploy
    ```

