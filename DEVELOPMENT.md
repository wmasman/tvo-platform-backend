# Directus Local Development Guide

## Quick Start

1. **Setup Environment**
   ```bash
   # Copy environment template and configure
   cp .env.example .env.local
   # Edit .env.local with your settings
   ```

2. **Start Development Environment**
   ```bash
   cd schema-tool
   npm run dev:start
   ```

3. **Access Directus**
   - **Local Admin**: http://localhost:8055
   - **Local API**: http://localhost:8055/graphql  
   - **Local Health**: http://localhost:8055/server/health
   - **Production Admin**: https://directus-poc.fly.dev/admin
   - **Production API**: https://directus-poc.fly.dev/graphql
   - **Production Health**: https://directus-poc.fly.dev/server/health

## Development Commands

### Environment Management
```bash
# Start full development stack (PostgreSQL + Directus)
npm run dev:start

# Stop all services
npm run dev:stop

# Restart services (quick refresh)
npm run dev:restart

# Reset everything (delete volumes, fresh start)
npm run dev:reset

# Check service status
npm run status
```

### Monitoring & Debugging
```bash
# View all logs (real-time)
npm run dev:logs

# View Directus logs only
npm run dev:logs:directus

# View PostgreSQL logs only
npm run dev:logs:postgres

# Check if services are healthy
npm run health

# Access Directus shell
npm run dev:shell

# Access PostgreSQL database
npm run dev:db
```

### Schema Management (Solo Developer Approach)
```bash
# Apply schema changes to local instance
npm run schema:apply

# Validate schema without applying (future)
npm run schema:validate
```

### Schema Development Workflow
**Git-based versioning with manual deployment (safe for small teams)**

1. **Development Cycle**
   ```bash
   # Make schema changes in YAML files
   git add . && git commit -m "feat: add new content type"
   npm run schema:apply  # Apply to local
   ```

2. **Environment Promotion** 
   ```bash
   # Manual deployment to staging/production
   # (Prevents accidental breaking changes)
   git push origin develop
   # Deploy manually when ready
   ```

3. **Rollback Strategy**
   ```bash
   git revert HEAD           # Revert schema change
   npm run schema:apply      # Apply reverted schema
   ```

**Why Manual Over Automated:**
- ✅ Solo developer control
- ✅ Prevents accidental production changes  
- ✅ Simple to understand and debug
- ✅ Git history = complete audit trail

## Architecture

### Services
- **PostgreSQL** (port 5433): Local development database
- **Directus** (port 8055): CMS and API server

### Data Persistence
- **PostgreSQL Data**: Docker volume `directus_db`
- **File Uploads**: Local directory `./uploads`
- **Schema**: Version controlled in `schema-tool/`

### Environment Configuration
- **`.env.local`**: Your actual development settings (not tracked in git)
- **`.env.example`**: Template with placeholder values
- **`.env`**: Legacy file (still supported)

## Development Workflow

### Daily Development
1. `npm run dev:start` - Start your environment
2. Make schema changes in YAML files
3. `npm run schema:apply` - Apply schema changes
4. Develop and test your features
5. `npm run dev:stop` - Clean shutdown

### Troubleshooting
1. **Services won't start**: `npm run dev:reset`
2. **Database issues**: `npm run dev:logs:postgres`
3. **Directus issues**: `npm run dev:logs:directus`
4. **Check health**: `npm run health`

### Git Workflow
- **develop**: Active development branch
- **staging**: Pre-production testing
- **master**: Production deployments (✅ **ACTIVE** - auto-deploys to Fly.io)

### Production Status
- **✅ DEPLOYED**: September 14, 2025
- **URL**: https://directus-poc.fly.dev
- **Status**: Active with enhanced development setup
- **Deployment**: Automatic via GitHub Actions on master push

## Port Configuration

| Service    | Local Port | Container Port | Purpose |
|------------|------------|----------------|---------|
| Directus   | 8055       | 8055           | Admin panel & API |
| PostgreSQL | 5433       | 5432           | Database access |

## Database Access

### From Host Machine
```bash
# Using npm script (recommended)
npm run dev:db

# Direct psql connection
psql -h localhost -p 5433 -U directus -d directus_local
```

### Connection Details
- **Host**: localhost
- **Port**: 5433
- **Database**: directus_local
- **Username**: directus
- **Password**: directus_dev_password

## Environment Variables

### Required
- `KEY`: Encryption key for Directus
- `SECRET`: JWT secret for authentication
- `ADMIN_EMAIL`: Admin user email
- `ADMIN_PASSWORD`: Admin user password

### Database (Auto-configured)
- `DB_CLIENT`: PostgreSQL client
- `DB_HOST`: postgres (Docker network)
- `DB_PORT`: 5432 (internal)
- `DB_DATABASE`: directus_local
- `DB_USER`: directus
- `DB_PASSWORD`: directus_dev_password

### Development
- `LOG_LEVEL`: debug (verbose logging)
- `CACHE_ENABLED`: false (disable caching)
- `RATE_LIMITER_ENABLED`: false (disable rate limiting)

## Production Differences

| Feature | Development | Production |
|---------|-------------|------------|
| Database | Local PostgreSQL | Neon PostgreSQL |
| Caching | Disabled | Enabled |
| Logging | Debug level | Info level |
| Rate Limiting | Disabled | Enabled |
| Admin Access | Open | Secured |

## Next Steps

1. **Epic 3**: Schema Management & Version Control
2. **Epic 4**: Automated Deployment Pipeline
3. **Epic 5**: Database Management & Synchronization
4. **Epic 6**: Documentation & Developer Experience