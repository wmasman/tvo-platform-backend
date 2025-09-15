# TVO Backend Environment Workflow Guide

## Overview

The TVO Backend (Directus CMS) uses **separate environments** for development and production. Understanding this separation is crucial for effective development workflow.

## Environment Architecture

### **Production Environment**
- **URL**: https://tvo-backend.fly.dev
- **Database**: Neon PostgreSQL (cloud-hosted)
- **File Storage**: Fly.io volume (`tvo_backend_uploads`)
- **Purpose**: Live content management and API serving

### **Local Development Environment**  
- **URL**: http://localhost:8055
- **Database**: PostgreSQL Docker container (local)
- **File Storage**: Local `./uploads` directory
- **Purpose**: Schema development, testing, content modeling

## 🚨 **Critical Understanding: NO AUTO-SYNC**

**Environments are completely separate:**
- Changes in production → Stay in production
- Changes in local → Stay in local
- **NO automatic synchronization** between environments

### **What This Means:**

#### **Production Changes**
When you work at https://tvo-backend.fly.dev/admin:
- ✅ Schema changes → Only affect Neon PostgreSQL
- ✅ Content creation → Only stored in Neon PostgreSQL  
- ✅ User management → Only affects production users
- ✅ File uploads → Only stored in Fly.io volume

#### **Local Changes**
When you work at http://localhost:8055/admin:
- ✅ Schema changes → Only affect local PostgreSQL container
- ✅ Content creation → Only stored locally
- ✅ User management → Only affects local users
- ✅ File uploads → Only stored in local `./uploads` directory

## 🔄 **Recommended Development Workflow**

### **Schema Development Process**

#### **Step 1: Local Development**
```bash
cd directus/schema-tool
npm run dev:start        # Start local environment
```
- Access: http://localhost:8055/admin
- Create and test schema changes locally
- Verify functionality thoroughly

#### **Step 2: Local Testing**
- Create test content to validate schema
- Test all relationships and field types
- Ensure UI/UX works as expected

#### **Step 3: Production Application**
- Access: https://tvo-backend.fly.dev/admin
- **Manually recreate** the same schema changes
- Apply identical configuration to production

#### **Step 4: Validation**
- Test production schema with sample content
- Verify API endpoints work correctly
- Confirm all functionality matches local testing

### **Content Development Process**

#### **For Testing Content**
- **Use local environment** for all testing and experimentation
- Create sample content locally to test workflows
- Local content is disposable and safe to experiment with

#### **For Production Content**
- **Work directly in production** for real content creation
- Production content is persistent and serves the live application
- Be careful with destructive operations

## 🛠 **Environment Management Commands**

### **Local Environment**
```bash
cd directus/schema-tool

# Environment Control
npm run dev:start      # Start PostgreSQL + Directus
npm run dev:stop       # Stop all services
npm run dev:restart    # Quick restart
npm run dev:reset      # Fresh start (deletes all data)

# Monitoring
npm run status         # Check service status
npm run health         # Verify health endpoints
npm run dev:logs       # View logs

# Database Access
npm run dev:db         # Connect to local PostgreSQL
```

### **Production Environment**
```bash
cd directus

# Status Monitoring
fly status --app tvo-backend
fly logs --app tvo-backend
curl https://tvo-backend.fly.dev/server/health

# Management
fly machine restart --app tvo-backend [machine-id]
fly secrets list --app tvo-backend
```

## 🔐 **Environment Credentials**

### **Production Access**
- **URL**: https://tvo-backend.fly.dev/admin
- **Email**: wmasman@gmail.com
- **Password**: password (change after first login)

### **Local Access**
- **URL**: http://localhost:8055/admin  
- **Email**: wmasman@gmail.com (auto-created)
- **Password**: password (configured in docker-compose)

## 📋 **Development Scenarios**

### **Scenario 1: Creating New Content Types**
1. **Local**: Design and test content type in local admin
2. **Local**: Create sample content to validate structure
3. **Production**: Recreate identical content type in production admin
4. **Production**: Create initial real content

### **Scenario 2: Modifying Existing Schema**
1. **Local**: Test schema modifications with existing local data
2. **Local**: Verify no data loss or corruption occurs
3. **Production**: Apply same modifications to production
4. **Production**: Validate existing production content remains intact

### **Scenario 3: API Development**
1. **Local**: Test GraphQL queries against local data
2. **Local**: Develop and debug API integration
3. **Production**: Validate API works with production data structure
4. **Frontend**: Connect to production API endpoints

## ⚠️ **Important Considerations**

### **Data Safety**
- **Production data is irreplaceable** - always test locally first
- **Local data is disposable** - can be reset anytime with `npm run dev:reset`
- **Backup production** before major schema changes

### **Development Speed**
- **Fast iteration** - local changes are instant and safe
- **Production deployment** - requires manual recreation but ensures quality
- **Testing flexibility** - local environment can be reset/modified freely

### **Team Collaboration**
- **Schema documentation** should be maintained in git
- **Production changes** should be communicated to team
- **Local setup** allows independent development without conflicts

## 🔄 **Alternative Workflows**

### **Option A: Current Workflow (Recommended)**
- ✅ **Safety**: No risk of accidentally affecting production
- ✅ **Control**: Manual verification of each change
- ✅ **Testing**: Thorough local testing before production
- ❌ **Speed**: Manual sync required

### **Option B: Shared Database (Advanced)**
Configure local development to use Neon PostgreSQL:
- ✅ **Sync**: Automatic synchronization
- ✅ **Speed**: No manual sync needed
- ❌ **Risk**: Local development can affect production
- ❌ **Safety**: No isolation for testing

### **Option C: Migration-Based (Future)**
Version-controlled schema changes:
- ✅ **Version Control**: Schema changes tracked in git
- ✅ **Automation**: Automated deployment pipeline
- ✅ **Rollback**: Easy rollback capabilities
- ❌ **Complexity**: Requires additional tooling

## 🎯 **Best Practices**

### **Schema Development**
1. **Always start locally** for schema changes
2. **Test thoroughly** before applying to production
3. **Document changes** in git commits
4. **Apply to production manually** when confident

### **Content Management**
1. **Use local** for testing and experimentation
2. **Use production** for real content creation
3. **Export/import** for content migration if needed

### **Debugging**
1. **Reproduce issues locally** when possible
2. **Check logs** in both environments
3. **Use health endpoints** to verify status

### **Deployment**
1. **Local development** → comprehensive testing
2. **Production application** → careful manual recreation  
3. **Validation** → verify everything works correctly
4. **Documentation** → update guides and team knowledge

---

**This workflow ensures safe, controlled development while maintaining production stability for the TVO Backend CMS.**