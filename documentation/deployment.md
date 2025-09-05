# Directus Deployment on Fly.io

This document outlines the process for deploying the Directus application to Fly.io.

## Prerequisites

- A Fly.io account with a credit card on file.
- The `flyctl` command-line tool installed.
- A GitHub repository with the Directus project.

## Initial Deployment

1.  **Configure Secrets:** Before deploying, you must set the following secrets in your Fly.io application:
    - `KEY`: A long, random, unique string for securely signing tokens.
    - `SECRET`: Another long, random, unique string for the same purpose.
    - `DB_CONNECTION_STRING`: The connection string for your PostgreSQL database.
    - `ADMIN_EMAIL`: The email address for the initial admin user.
    - `ADMIN_PASSWORD`: The password for the initial admin user.
    - `DB_CLIENT`: Set to `pg` to ensure the correct database driver is used.

2.  **Bootstrap the Database:** For the initial deployment, the `release_command` in `fly.toml` should be set to `npx directus bootstrap`. This will create the necessary tables in the database.

3.  **Deploy:** The application can be deployed using `fly deploy` or by pushing to the `main` branch, which will trigger the GitHub Actions workflow.

## Subsequent Deployments

After the initial deployment, the `release_command` in `fly.toml` should be changed to `npx directus database migrate latest`. This will ensure that database migrations are applied on subsequent deployments without re-initializing the database.

## Troubleshooting

- **`fly` command not found:** Ensure that `flyctl` is installed and that the `~/.fly/bin` directory is in your `PATH`.
- **Database connection errors:** Verify that all required secrets are set correctly in your Fly.io application.
- **Application not listening:** Ensure that the `.env` file is included in your `.dockerignore` file to prevent it from being included in the build.