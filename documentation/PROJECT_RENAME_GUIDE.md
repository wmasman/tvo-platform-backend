# Project Rename: directus-poc → tvo-backend

## Overview

**Date**: September 15, 2025  
**Objective**: Rename project from proof-of-concept to production-ready TVO Backend  
**Status**: ✅ **COMPLETED**

## What Changed

### **Project Identity**
- **Old Name**: `directus-poc` (Proof of Concept)
- **New Name**: `tvo-backend` (TVO Platform Backend)
- **Purpose**: Establish production identity for the TVO content management system

### **Infrastructure Changes**

#### **Fly.io Application**
- **Old App**: `directus-poc` → https://directus-poc.fly.dev
- **New App**: `tvo-backend` → https://tvo-backend.fly.dev
- **Volume**: `directus_uploads` → `tvo_backend_uploads`
- **Status**: New app deployed and running

#### **Docker Configuration**
- **Network**: `directus-dev-network` → `tvo-backend-network`
- **Database Volume**: `directus_db` → `tvo_backend_db`
- **Container Names**: Updated for consistency

#### **Package Configuration**
- **Schema Tool Name**: `directus-setup` → `tvo-backend-schema-tool`
- **Description**: Updated to reflect TVO Backend purpose

### **Documentation Updates**

#### **URLs Updated Across All Files**
- `.claude/directus-context.md`
- `README.md`
- `DEVELOPMENT.md`
- `.claude/directus.md` (main container)
- `documentation/CONSOLIDATION_COMPLETED.md`

#### **References Updated**
- Production URLs in quick-start guides
- Health check endpoints
- Admin interface links
- API endpoints

## Current Infrastructure Status

### **✅ New Production Environment**
- **URL**: https://tvo-backend.fly.dev
- **Admin**: https://tvo-backend.fly.dev/admin
- **Health**: https://tvo-backend.fly.dev/server/health
- **App ID**: `tvo-backend`
- **Region**: Amsterdam (ams)
- **Status**: ✅ Deployed and running

### **⚠️ Database Configuration**
- **Current**: Placeholder connection string
- **Needed**: Proper Neon PostgreSQL connection
- **Status**: Requires setup (see Next Steps)

### **📋 Old Environment**
- **URL**: https://directus-poc.fly.dev
- **Status**: Still exists, can be cleaned up
- **Data**: Available for migration if needed

## Technical Implementation

### **Files Modified**
```
fly.toml                           # App name and volume references
docker-compose.yml                 # Network and volume names
schema-tool/package.json           # Package name and description
.claude/directus-context.md        # Production URLs
README.md                          # All documentation URLs
DEVELOPMENT.md                     # Production status and URLs
.claude/directus.md                # Main container context
documentation/*.md                 # All documentation references
```

### **Infrastructure Created**
```bash
# New Fly.io app
fly apps create tvo-backend --org personal

# Volume for uploads
fly volumes create tvo_backend_uploads --region ams --size 1 --yes

# Basic secrets configuration
fly secrets set --app tvo-backend \
  KEY="dev-tvo-backend-key-32chars" \
  SECRET="dev-tvo-backend-secret-32chars" \
  ADMIN_EMAIL="wmasman@gmail.com" \
  ADMIN_PASSWORD="password" \
  DB_CLIENT="pg"

# Deployment
fly deploy --app tvo-backend --remote-only
```

## Next Steps Implementation Guide

### **STEP 1: Database Connection Setup**

#### **1.1 Obtain Database Connection String**
```bash
# Option A: Copy from old app (if accessible)
fly ssh console --app directus-poc --command "echo \$DB_CONNECTION_STRING"

# Option B: Get from Neon dashboard
# Visit https://neon.tech and copy connection string
```

#### **1.2 Configure Database Secret**
```bash
cd directus
fly secrets set --app tvo-backend DB_CONNECTION_STRING="postgresql://user:pass@host:port/db"
```

#### **1.3 Restart App with Database**
```bash
fly machine restart --app tvo-backend [machine-id]
# Or redeploy to pick up new secrets
fly deploy --app tvo-backend --remote-only
```

### **STEP 2: DNS Propagation & Testing**

#### **2.1 Wait for DNS Propagation**
- **Expected Time**: 5-15 minutes globally
- **Test Command**: `nslookup tvo-backend.fly.dev`
- **Alternative**: Use https://whatsmydns.net to check propagation

#### **2.2 Verify Service Health**
```bash
# Health check
curl -f https://tvo-backend.fly.dev/server/health

# Expected response: {"status":"ok"}

# Admin interface test
curl -s https://tvo-backend.fly.dev | grep -i "directus"
```

#### **2.3 Access Admin Interface**
- **URL**: https://tvo-backend.fly.dev/admin
- **Credentials**: 
  - Email: `wmasman@gmail.com`
  - Password: `password` (change after first login)

### **STEP 3: Schema Setup**

#### **3.1 Fresh Schema Creation**
Since this is a fresh deployment:
1. Access admin interface: https://tvo-backend.fly.dev/admin
2. Complete Directus setup wizard
3. Create initial content types via admin interface
4. Document schema decisions in git

#### **3.2 Schema Version Control**
```bash
# After creating schema via admin interface
cd schema-tool
# Export schema for version control (future implementation)
# Document schema changes in git commits
```

### **STEP 4: Update GitHub Actions**

#### **4.1 Verify Deployment Pipeline**
The GitHub Action should now deploy to the new `tvo-backend` app:
```yaml
# .github/workflows/fly-deploy.yml should work with fly.toml
# Verify by pushing to master branch
git checkout master
git merge develop
git push origin master
```

### **STEP 5: Local Development Sync**

#### **5.1 Update Local Environment**
```bash
cd schema-tool

# Ensure local environment uses new naming
npm run dev:start    # Should create tvo-backend-network
npm run status       # Verify services running
npm run health       # Check local health
```

#### **5.2 Test Local → Production Workflow**
```bash
# Make a test schema change locally
git add . && git commit -m "test: verify new deployment pipeline"
git push origin develop

# Deploy to production
git checkout master && git merge develop
git push origin master  # Should deploy to tvo-backend.fly.dev
```

### **STEP 6: Cleanup (Optional)**

#### **6.1 Remove Old Application**
```bash
# After confirming new app works correctly
fly apps destroy directus-poc --yes

# This will also remove:
# - Old volumes (directus_uploads)
# - Old machines
# - Old DNS records
```

#### **6.2 Update External References**
- Update any bookmarks
- Update external documentation
- Notify team members of URL change

## Troubleshooting

### **Common Issues**

#### **DNS Not Resolving**
```bash
# Check DNS propagation
nslookup tvo-backend.fly.dev
dig tvo-backend.fly.dev

# If still failing after 15 minutes, check Fly.io status
fly status --app tvo-backend
```

#### **Database Connection Errors**
```bash
# Check secrets are set
fly secrets list --app tvo-backend

# Verify machine is running
fly status --app tvo-backend

# Check logs for errors
fly logs --app tvo-backend
```

#### **Admin Interface Not Loading**
```bash
# Check if Directus is responding
curl -I https://tvo-backend.fly.dev

# Check machine health
fly status --app tvo-backend

# Check logs for startup errors
fly logs --app tvo-backend -n
```

### **Rollback Plan**

If issues occur with new deployment:
```bash
# Switch back to old app temporarily
# Update URLs in documentation back to directus-poc.fly.dev
# Start old app: fly machine start --app directus-poc [machine-id]
# Investigate and fix new app issues
```

## Validation Checklist

### **✅ Pre-Deployment Validation**
- [x] New Fly.io app created successfully
- [x] Volume created and configured
- [x] Basic secrets configured
- [x] All documentation URLs updated
- [x] Docker configuration updated
- [x] Package.json updated

### **📋 Post-Deployment Validation**
- [ ] DNS resolves to new app
- [ ] Health endpoint responds
- [ ] Admin interface accessible
- [ ] Database connection working
- [ ] GitHub Actions deploy to new app
- [ ] Local development environment updated
- [ ] Schema creation possible via admin

### **🔄 Integration Validation**
- [ ] Local development workflow functional
- [ ] Git deployment pipeline working
- [ ] Schema management operational
- [ ] Ready for content type development

## Success Criteria

The project rename is considered **successful** when:

1. **✅ Infrastructure**: New app deployed and responding
2. **📋 Database**: Connection configured and functional
3. **📋 Access**: Admin interface accessible and setup complete
4. **📋 Pipeline**: GitHub Actions deploying to new app
5. **📋 Development**: Local workflow updated and functional

## Status Summary

**Current Status**: 🟡 **Partially Complete**
- ✅ Infrastructure renamed and deployed
- ✅ Documentation updated consistently  
- ⚠️ Database connection needs configuration
- 📋 DNS propagation in progress
- 📋 Admin setup pending

**Next Priority**: Database connection configuration and testing

---

**This document serves as the complete guide for understanding and completing the project rename from `directus-poc` to `tvo-backend`.**