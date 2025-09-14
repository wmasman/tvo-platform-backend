# Directus CMS Workspace Context

## Project Overview
Proof-of-concept headless CMS using Directus for future editorial content creation in the TVO platform.

## Directory Structure
```
directus/
├── schema-tool/           # Automated schema management
│   ├── apply_schema.js   # Schema application script
│   └── package.json      # npm run schema:apply
├── documentation/        # Setup and deployment docs
├── docker-compose.yml    # Local development
├── fly.toml             # Fly.io deployment config
└── README.md            # Main documentation
```

## Key Commands

### Schema Management
```bash
cd schema-tool
npm run schema:apply     # Apply schema from YAML
npm run docker:restart   # Restart local Directus
```

### Local Development
```bash
docker-compose up -d     # Start Directus locally
docker-compose down      # Stop Directus
```

### Deployment
```bash
fly deploy              # Deploy to Fly.io
fly secrets set KEY="..." SECRET="..." # Set environment variables
```

## Configuration Files
- **Schema**: `schema/migrations/schema_fixed.yml` - Single source of truth
- **Docker**: `docker-compose.yml` - Local development environment
- **Deploy**: `fly.toml` - Production deployment configuration

## Technology Stack
- **CMS**: Directus 11.3.5
- **Database**: PostgreSQL (Neon for production, local for dev)
- **Deployment**: Fly.io
- **Schema Management**: Custom Node.js tool with Directus SDK

## Integration Strategy
Future integration with TVO backend:
1. **Content Creation**: Authors use Directus interface
2. **Content Processing**: New articles flow through TVO pipeline
3. **Knowledge Network**: CMS content contributes to concept clusters
4. **Unified Frontend**: Both PDF and CMS content in same interface

## Development Status
- ✅ Basic Directus setup working
- ✅ Automated schema management
- ✅ Fly.io deployment pipeline
- 🟡 Integration with TVO backend pending
- 🟠 Content workflow definition needed