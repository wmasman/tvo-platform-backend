# Directus Development Workflow Plan
## Epic-Based Implementation Strategy

### **Overview**
This document outlines the complete transformation of the current Directus setup into a professional development workflow with proper Git branching, Docker containerization, and automated deployments.

---

## **EPIC 1: Repository Migration & Git Workflow Setup**
**Goal**: Establish dedicated repository with proper branching strategy  
**Priority**: Critical  
**Estimated Effort**: 1-2 days  

### **Story 1.1: Create Dedicated Directus Repository**
- **Acceptance Criteria**:
  - [ ] New repository `tvo-platform-backend` created on GitHub
  - [ ] Current `/directus` content migrated to new repo
  - [ ] Proper `.gitignore` configured for Directus/Node.js
  - [ ] Repository connected to local development environment
  - [ ] All commit history preserved during migration

### **Story 1.2: Establish Git Branching Strategy**
- **Acceptance Criteria**:
  - [ ] `develop` branch created as default development branch
  - [ ] `staging` branch created for pre-production testing
  - [ ] `main` branch configured for production deployments
  - [ ] Branch protection rules configured on GitHub
  - [ ] Local git remotes properly configured

### **Story 1.3: Update Container Repository Integration**
- **Acceptance Criteria**:
  - [ ] Update main container `.gitmodules` to reference new repo
  - [ ] Remove old `/directus` from main repo `.gitignore`
  - [ ] Add new repo as git submodule
  - [ ] Update documentation in main CLAUDE.md
  - [ ] Test nested repository workflow

---

## **EPIC 2: Local Development Environment Standardization**
**Goal**: Create consistent Docker-based local development setup  
**Priority**: High  
**Estimated Effort**: 1 day  

### **Story 2.1: Enhanced Docker Compose Configuration**
- **Acceptance Criteria**:
  - [ ] `docker-compose.yml` includes both Directus and PostgreSQL services
  - [ ] Persistent volumes configured for database and uploads
  - [ ] Proper service networking between containers
  - [ ] Health checks implemented for both services
  - [ ] Port mapping configured for local access

### **Story 2.2: Environment Configuration Management**
- **Acceptance Criteria**:
  - [ ] `.env.local` template created for local development
  - [ ] `.env.example` provided with placeholder values
  - [ ] Environment variable validation in startup scripts
  - [ ] Sensitive data excluded from git tracking
  - [ ] Local PostgreSQL credentials properly configured

### **Story 2.3: Development Scripts & Commands**
- **Acceptance Criteria**:
  - [ ] `npm run dev:start` - Start local Docker environment
  - [ ] `npm run dev:stop` - Stop and cleanup containers
  - [ ] `npm run dev:logs` - View container logs
  - [ ] `npm run dev:reset` - Reset database to clean state
  - [ ] `npm run schema:apply` - Apply schema changes locally

---

## **EPIC 3: Schema Management & Version Control**
**Goal**: Robust schema versioning with automated synchronization  
**Priority**: High  
**Estimated Effort**: 0.5 days  

### **Story 3.1: Enhanced Schema Management**
- **Acceptance Criteria**:
  - [ ] YAML schema files properly versioned in git
  - [ ] Schema validation before applying changes
  - [ ] Rollback capability for schema changes
  - [ ] Schema diff reporting between environments
  - [ ] Automated backup before schema updates

### **Story 3.2: Multi-Environment Schema Sync**
- **Acceptance Criteria**:
  - [ ] Schema sync between local ↔ staging
  - [ ] Schema sync between staging ↔ production
  - [ ] Environment-specific schema configurations
  - [ ] Schema drift detection and reporting
  - [ ] Migration scripts for breaking changes

---

## **EPIC 4: Automated Deployment Pipeline**
**Goal**: CI/CD pipeline for seamless deployments  
**Priority**: Medium  
**Estimated Effort**: 2 days  

### **Story 4.1: GitHub Actions Setup**
- **Acceptance Criteria**:
  - [ ] Workflow for `develop` → staging deployment
  - [ ] Workflow for `main` → production deployment
  - [ ] Docker image building and caching
  - [ ] Environment-specific secret management
  - [ ] Deployment status notifications

### **Story 4.2: Staging Environment Configuration**
- **Acceptance Criteria**:
  - [ ] Staging Fly.io app configured
  - [ ] Staging Neon database created
  - [ ] Staging-specific environment variables
  - [ ] Automated testing on staging deployments
  - [ ] Staging URL accessible for testing

### **Story 4.3: Production Deployment Automation**
- **Acceptance Criteria**:
  - [ ] Production deployment triggered by `main` branch
  - [ ] Database migration automation
  - [ ] Zero-downtime deployment strategy
  - [ ] Rollback procedure documented and tested
  - [ ] Production monitoring and alerting

---

## **EPIC 5: Database Management & Synchronization**
**Goal**: Consistent data management across environments  
**Priority**: Medium  
**Estimated Effort**: 1 day  

### **Story 5.1: Database Environment Separation**
- **Acceptance Criteria**:
  - [ ] Local PostgreSQL database (development)
  - [ ] Staging Neon database (testing)
  - [ ] Production Neon database (live)
  - [ ] Connection pooling configured
  - [ ] Database backup strategies implemented

### **Story 5.2: Data Management Tools**
- **Acceptance Criteria**:
  - [ ] Database seeding scripts for development
  - [ ] Data migration tools between environments
  - [ ] Database backup and restore procedures
  - [ ] Data sanitization for staging/development
  - [ ] Performance monitoring and optimization

---

## **EPIC 6: Documentation & Developer Experience**
**Goal**: Comprehensive documentation and smooth developer onboarding  
**Priority**: Medium  
**Estimated Effort**: 1 day  

### **Story 6.1: Developer Documentation**
- **Acceptance Criteria**:
  - [ ] Complete setup instructions for new developers
  - [ ] Development workflow documentation
  - [ ] Troubleshooting guide
  - [ ] Architecture diagrams and explanations
  - [ ] API documentation and examples

### **Story 6.2: Operational Procedures**
- **Acceptance Criteria**:
  - [ ] Deployment procedures documented
  - [ ] Incident response procedures
  - [ ] Database maintenance procedures
  - [ ] Security best practices documented
  - [ ] Performance monitoring guidelines

---

## **Implementation Timeline**

### **Phase 1 (Week 1): Foundation**
- Epic 1: Repository Migration & Git Workflow Setup
- Epic 2: Local Development Environment Standardization

### **Phase 2 (Week 2): Automation**
- Epic 3: Schema Management & Version Control
- Epic 4: Automated Deployment Pipeline

### **Phase 3 (Week 3): Production Ready**
- Epic 5: Database Management & Synchronization
- Epic 6: Documentation & Developer Experience

---

## **Success Criteria**

### **Technical Goals**
- [ ] Single command local environment setup (`npm run dev:start`)
- [ ] Automated deployments on git push
- [ ] Zero-downtime production deployments
- [ ] Complete schema version control
- [ ] Environment parity (dev/staging/prod)

### **Developer Experience Goals**
- [ ] New developer can set up environment in < 15 minutes
- [ ] Schema changes deployed with single command
- [ ] Clear separation between environments
- [ ] Comprehensive documentation
- [ ] Reliable rollback procedures

### **Business Goals**
- [ ] Reduced deployment risks
- [ ] Faster feature delivery
- [ ] Improved system reliability
- [ ] Better change management
- [ ] Scalable development workflow

---

## **Risk Mitigation**

### **High Risk Items**
- **Data Loss During Migration**: Complete backup before any changes
- **Service Downtime**: Implement blue-green deployment strategy
- **Environment Drift**: Automated environment synchronization

### **Monitoring & Validation**
- Database integrity checks before/after deployments
- Automated testing pipeline for all environments
- Performance regression testing
- Security vulnerability scanning

---

## **Post-Implementation Maintenance**

### **Regular Tasks**
- Weekly schema sync validation
- Monthly security updates
- Quarterly performance reviews
- Database backup verification

### **Monitoring Metrics**
- Deployment success rate
- Mean time to recovery (MTTR)
- Development environment setup time
- Schema drift incidents
- Production uptime percentage

---

*This plan provides a comprehensive roadmap for transforming the current Directus setup into a production-ready development workflow. Each epic can be implemented independently, allowing for iterative progress and early wins.*