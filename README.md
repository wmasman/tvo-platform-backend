# Directus CMS Platform

Professional headless CMS using Directus with development workflow optimized for solo developers and small teams.

## Quick Start

1. **Setup Environment**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your settings
   ```

2. **Start Development**
   ```bash
   cd schema-tool
   npm run dev:start
   ```

3. **Access Directus**
   - **Local Admin**: http://localhost:8055
   - **Local API**: http://localhost:8055/graphql
   - **Production Admin**: https://tvo-backend.fly.dev/admin
   - **Production API**: https://tvo-backend.fly.dev/graphql

## Development Workflow

### Local Development
```bash
cd schema-tool

# Environment management
npm run dev:start      # Start PostgreSQL + Directus
npm run dev:stop       # Stop all services
npm run dev:restart    # Quick restart
npm run dev:reset      # Fresh start (deletes data)

# Monitoring
npm run status         # Check service status
npm run health         # Verify health endpoints
npm run dev:logs       # View all logs

# Database access
npm run dev:db         # Connect to PostgreSQL
```

### Schema Management (Solo Developer Workflow)

**Simple, git-based schema versioning:**

1. **Make Schema Changes**
   ```bash
   # Edit schema files in schema-tool/
   git add . && git commit -m "feat: add user profiles schema"
   ```

2. **Apply to Local Environment**
   ```bash
   npm run schema:apply
   ```

3. **Deploy to Production** (Automated)
   ```bash
   # Merge to master triggers GitHub Action deployment
   git checkout master && git merge develop
   git push origin master
   
   # Schema applied manually in production admin interface
   # Visit: https://tvo-backend.fly.dev/admin
   ```

4. **Rollback if Needed**
   ```bash
   git revert HEAD
   npm run schema:apply  # Revert to previous schema
   ```

**Key Principles:**
- Schema is version controlled in git
- Manual deployment = safe for small teams
- Git history = complete audit trail
- Simple commands, no complex tooling

## Deployment Strategy

### CMS Backend: Fly.io with Neon PostgreSQL
This project is configured for deployment to Fly.io with a Neon Postgres database for the CMS backend.

### Frontend Integration: Cloudflare Pages
The frontend deploys to Cloudflare Pages with static export optimization, consuming content from this Directus CMS via API.

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

