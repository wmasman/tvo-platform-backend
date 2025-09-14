# Directus CMS Workspace Context

## Project Overview
Professional headless CMS using Directus with comprehensive development workflow for the TVO platform.

## Git Workflow (Updated)
```
develop  ← Active development branch (current)
staging  ← Pre-production testing
master   ← Production deployments
```

## Directory Structure (Enhanced)
```
directus/
├── .claude/                    # Claude Code context
├── schema-tool/               # Enhanced development tools
│   ├── apply_schema.js       # Schema application script
│   └── package.json          # Comprehensive npm scripts
├── documentation/            # Complete development docs
│   ├── development-workflow-plan.md  # Epic-based implementation
│   └── deployment.md         # Deployment procedures
├── docker-compose.yml        # Full PostgreSQL + Directus stack
├── .env.local               # Local development config
├── .env.example             # Environment template
├── fly.toml                 # Fly.io production deployment
├── DEVELOPMENT.md           # Developer quick-start guide
└── README.md                # Project overview
```

## Development Commands (Enhanced)

### Environment Management
```bash
cd schema-tool

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

### Schema Management (Solo Developer Workflow)
```bash
# Apply schema changes to local instance
npm run schema:apply

# Git-based schema versioning
git add . && git commit -m "feat: add content type"
npm run schema:apply  # Apply locally

# Manual deployment (safe approach)
git push origin develop
# Deploy to staging/production manually when ready

# Rollback if needed
git revert HEAD && npm run schema:apply
```

## Local Development Architecture
- **PostgreSQL** (port 5433): Local development database with persistent volumes
- **Directus** (port 8055): CMS and API server with health checks
- **Network**: Isolated docker network for service communication
- **Volumes**: Persistent database storage and file uploads

## Environment Configuration
- **`.env.local`**: Actual development settings (git-ignored)
- **`.env.example`**: Template with placeholder values (tracked)
- **Docker**: Uses `.env.local` for local development
- **Production**: Uses Fly.io secrets for cloud deployment

## Development Workflow Implementation Status

### ✅ Epic 1: Repository Migration & Git Workflow
- Dedicated repository: `https://github.com/wmasman/tvo-platform-backend`
- Git branches: develop/staging/master with remote tracking
- Documentation: Complete epic-based implementation plan

### 🔄 Epic 2: Local Development Environment (In Progress)
- Enhanced Docker Compose with PostgreSQL + Directus
- Comprehensive development scripts and commands
- Environment configuration management
- Developer documentation and quick-start guide

### ✅ Epic 3: Schema Management (Solo Developer Approach)
- **IMPLEMENTED**: Git-based YAML schema versioning
- **IMPLEMENTED**: Manual deployment workflow (safe for small teams)
- **IMPLEMENTED**: Simple rollback via git revert
- **SKIPPED**: Complex automation (over-engineered for MVP/solo dev)

### 📋 Epic 4: Automated Deployment Pipeline (Planned)
- GitHub Actions for develop → staging → production
- Environment-specific secret management
- Zero-downtime deployment strategies

## TaskWarrior Integration
- **Project**: `tvoo.directus`
- **Current Task**: Epic 2 (ID: 225) - Local Development Environment
- **Priority**: High - Foundation for all future development

## Quick Start (New Developer Setup)
1. `git clone https://github.com/wmasman/tvo-platform-backend.git`
2. `git checkout develop`
3. `cp .env.example .env.local` (edit with your settings)
4. `cd schema-tool && npm run dev:start`
5. Open http://localhost:8055

## Integration Strategy
Hybrid content system: `CMS Content Creation → Processing Pipeline → Knowledge Network → Frontend Display`

1. **Legacy Content**: PDFs processed through existing pipeline
2. **New Content**: CMS-authored articles enhanced with AI processing  
3. **Unified Knowledge**: Both sources contribute to concept clusters
4. **Enhanced Discovery**: AI connects all content types in frontend

## Port Configuration
| Service    | Local Port | Purpose |
|------------|------------|---------|
| Directus   | 8055       | Admin panel & API |
| PostgreSQL | 5433       | Database access |