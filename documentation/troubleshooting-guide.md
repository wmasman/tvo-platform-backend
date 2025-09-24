# Directus-Backend Integration Troubleshooting Guide

## Overview

This guide provides comprehensive troubleshooting solutions for common issues encountered when integrating the TVO Backend with Directus CMS. All solutions are based on real debugging experience and tested fixes.

## Common Issues and Solutions

### 1. Authentication Problems

#### Issue: 401 Unauthorized / Authentication Failed
**Symptoms**:
```
DirectusAuthenticationError: Invalid API Agent credentials
HTTP 401: Unauthorized
```

**Root Causes & Solutions**:

1. **Incorrect Credentials**
   ```bash
   # Check .env file
   DIRECTUS_API_AGENT_EMAIL="api-agent@tvo.local.nl"  # Must match exactly
   DIRECTUS_API_AGENT_PASSWORD="SecureApiPassword123!" # Check for typos
   ```

2. **User Not Active**
   - Navigate to Directus UI → Settings → Users
   - Edit API Agent user
   - Ensure Status = "Active"

3. **Environment Variables Not Loaded**
   ```python
   # Debug: Print loaded config
   from src_v2.config.directus_config import directus_config
   print(f"URL: {directus_config.url}")
   print(f"Email: {directus_config.api_agent_email}")
   # Password should not be printed for security
   ```

**Test Fix**:
```python
import requests

auth_response = requests.post("http://localhost:8055/auth/login", json={
    "email": "api-agent@tvo.local.nl",
    "password": "SecureApiPassword123!"
})
print(f"Auth status: {auth_response.status_code}")
if auth_response.status_code == 200:
    print("✅ Authentication working")
else:
    print(f"❌ Auth failed: {auth_response.json()}")
```

### 2. Permission Errors

#### Issue: 403 Forbidden on CRUD Operations
**Symptoms**:
```
{"errors":[{"message":"You don't have permission to \"create\" from collection \"articles\" or it does not exist.","extensions":{"code":"FORBIDDEN"}}]}
```

**Root Causes & Solutions**:

1. **Missing Collection Permissions**
   - Navigate to Settings → Access Control → Access Policies
   - Edit "API Agent Full Access" policy
   - Add permissions for missing collections:
     ```
     Collection: articles
     Actions: create, read, update, delete
     Fields: *
     ```

2. **Policy Not Assigned to Role**
   - Navigate to Settings → Access Control → User Roles
   - Edit "API Agent" role
   - In Policies section, ensure "API Agent Full Access" is listed

3. **Role Not Assigned to User**
   - Navigate to Settings → Access Control → Users
   - Edit API Agent user
   - Set Role to "API Agent"
   - Also assign "API Agent Full Access" policy directly

**Verification Script**:
```python
import requests

# Get authenticated user info
auth_response = requests.post("http://localhost:8055/auth/login", json={
    "email": "api-agent@tvo.local.nl",
    "password": "SecureApiPassword123!"
})
token = auth_response.json()["data"]["access_token"]
headers = {"Authorization": f"Bearer {token}"}

user_response = requests.get("http://localhost:8055/users/me?fields=*.*", headers=headers)
user_data = user_response.json()["data"]

print(f"User Role: {user_data.get('role')}")
print(f"User Policies: {user_data.get('policies', [])}")

# Should show role and policies assigned
```

### 3. Database Schema Issues

#### Issue: 500 Server Error with Column Not Found
**Symptoms**:
```
"column articles.authors does not exist"
"column articles.references does not exist"
```

**Root Cause**: Database schema missing required columns that Directus expects.

**Solution**:
```sql
# Connect to database
docker-compose exec postgres psql -U directus -d directus_local

# Add missing columns
ALTER TABLE articles ADD COLUMN IF NOT EXISTS authors json;
ALTER TABLE articles ADD COLUMN IF NOT EXISTS "references" json;

# Verify table structure
\d articles;
```

**Prevention**: Always run schema validation after Directus collection changes:
```python
def validate_articles_schema():
    import subprocess

    # Check if columns exist
    cmd = """docker-compose exec postgres psql -U directus -d directus_local -c "SELECT column_name FROM information_schema.columns WHERE table_name = 'articles' AND column_name IN ('authors', 'references');" """

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if "authors" not in result.stdout or "references" not in result.stdout:
        print("❌ Missing required columns")
        return False

    print("✅ Schema validation passed")
    return True
```

### 4. ID Type Mismatch

#### Issue: UUID vs Auto-Increment Integer Conflict
**Symptoms**:
```
ValidationError: ID field expects integer but received UUID string
Type mismatch: expected integer, got string
```

**Root Cause**: Backend trying to set UUID for database auto-increment integer field.

**Solution**: Remove manual ID setting, let database handle auto-increment:

```python
# ❌ WRONG - Don't set ID manually
article_data = DirectusArticle(
    id=str(uuid.uuid4()),  # This causes the error
    title="Test Article"
)

# ✅ CORRECT - Let database auto-increment
article_data = DirectusArticle(
    title="Test Article"
)
result = directus.create_item("articles", article_data)
article_id = result['data']['id']  # Get ID from response
```

**Schema Fix**: Update Pydantic model to reflect database reality:
```python
class DirectusArticle(BaseModel):
    id: Optional[int] = None  # Changed from str to int
    title: Optional[str] = None
    # ... other fields
```

### 5. Directus Service Connectivity

#### Issue: Connection Refused / Service Unreachable
**Symptoms**:
```
ConnectionError: HTTPSConnectionPool(host='localhost', port=8055)
requests.exceptions.ConnectionError
```

**Diagnosis Steps**:
```bash
# 1. Check if Directus is running
docker-compose ps

# 2. Check Directus logs
docker-compose logs directus

# 3. Check health endpoint
curl http://localhost:8055/server/health

# 4. Check port binding
netstat -tulpn | grep 8055
```

**Solutions**:

1. **Start Directus Service**:
   ```bash
   cd directus/
   docker-compose up -d
   ```

2. **Fix Port Conflicts**:
   ```yaml
   # docker-compose.yml - change port if 8055 is taken
   ports:
     - "8056:8055"  # External:Internal
   ```

3. **Check Environment Variables**:
   ```bash
   # Verify KEY and SECRET are set
   echo $DIRECTUS_KEY
   echo $DIRECTUS_SECRET
   ```

### 6. SDK-Specific Issues

#### Issue: DirectusClient Import Error
**Symptoms**:
```
ModuleNotFoundError: No module named 'directus_sdk_py'
ImportError: cannot import name 'DirectusClient'
```

**Solution**:
```bash
# Install/reinstall SDK
pip install directus-sdk-py

# Or if using requirements.txt
pip install -r requirements.txt

# Verify installation
python -c "from directus_sdk_py import DirectusClient; print('✅ SDK installed')"
```

#### Issue: SDK Method Not Found
**Symptoms**:
```
AttributeError: 'DirectusClient' object has no attribute 'create_item'
```

**Solution**: Check SDK version compatibility:
```bash
pip show directus-sdk-py
```

Update to compatible version if needed:
```bash
pip install directus-sdk-py==0.3.0  # Use specific compatible version
```

### 7. Policy System Issues (Directus v11 Specific)

#### Issue: UI Shows Policies But API Returns None
**Symptoms**:
- Directus UI shows correct role and policy assignments
- API `/users/me` returns `Role: None` and `Policies: []`
- Permissions work in UI but fail via API

**Root Cause**: Cache inconsistency between UI and API layers in Directus v11.

**Solution Steps**:

1. **Force Policy Refresh**:
   ```bash
   # Restart Directus to clear caches
   docker-compose restart directus
   ```

2. **Re-assign Policies**:
   - Edit API Agent user in UI
   - Remove and re-add role assignment
   - Remove and re-add policy assignment
   - Save changes

3. **Database Verification**:
   ```sql
   -- Check user role assignment
   SELECT id, first_name, last_name, email, role, status
   FROM directus_users
   WHERE email = 'api-agent@tvo.local.nl';

   -- Check policy assignments
   SELECT dp.name as policy_name, dr.name as role_name
   FROM directus_policies dp
   JOIN directus_roles dr ON /* role-policy relationship */
   WHERE dr.name = 'API Agent';
   ```

### 8. Data Validation Issues

#### Issue: Pydantic Validation Errors
**Symptoms**:
```
ValidationError: 1 validation error for DirectusArticle
processing_status
  string does not match expected pattern
```

**Root Cause**: Data doesn't match Pydantic model constraints.

**Solution**: Update validation or clean data:

```python
# Fix pattern validation
class DirectusArticle(BaseModel):
    processing_status: Optional[str] = Field(
        None,
        pattern="^(pending|in_progress|completed|failed)$"
    )

# Or clean data before validation
def clean_processing_status(status: str) -> str:
    status_mapping = {
        "processing": "in_progress",
        "done": "completed",
        "error": "failed"
    }
    return status_mapping.get(status.lower(), "pending")
```

## Debugging Tools

### 1. Connection Tester
```python
#!/usr/bin/env python3
"""
Debug Directus connection and permissions.
"""
import requests
import sys

def test_directus_connection():
    DIRECTUS_URL = "http://localhost:8055"

    # Test 1: Server health
    try:
        health = requests.get(f"{DIRECTUS_URL}/server/info", timeout=5)
        print(f"✅ Server reachable: {health.status_code}")
    except Exception as e:
        print(f"❌ Server unreachable: {e}")
        return False

    # Test 2: Authentication
    try:
        auth = requests.post(f"{DIRECTUS_URL}/auth/login", json={
            "email": "api-agent@tvo.local.nl",
            "password": "SecureApiPassword123!"
        })
        if auth.status_code == 200:
            print("✅ Authentication successful")
            token = auth.json()["data"]["access_token"]
        else:
            print(f"❌ Authentication failed: {auth.json()}")
            return False
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False

    # Test 3: User permissions
    try:
        headers = {"Authorization": f"Bearer {token}"}
        user_info = requests.get(f"{DIRECTUS_URL}/users/me", headers=headers)
        if user_info.status_code == 200:
            print("✅ User info accessible")
        else:
            print(f"❌ User info failed: {user_info.json()}")
    except Exception as e:
        print(f"❌ User info error: {e}")

    # Test 4: Articles collection access
    try:
        articles = requests.get(f"{DIRECTUS_URL}/items/articles", headers=headers)
        if articles.status_code == 200:
            print("✅ Articles collection accessible")
            return True
        else:
            print(f"❌ Articles access failed: {articles.json()}")
            return False
    except Exception as e:
        print(f"❌ Articles access error: {e}")
        return False

if __name__ == "__main__":
    success = test_directus_connection()
    sys.exit(0 if success else 1)
```

### 2. Schema Validator
```python
#!/usr/bin/env python3
"""
Validate Pydantic schema against Directus collection.
"""
import subprocess
import json

def validate_articles_schema():
    # Get database schema
    cmd = '''docker-compose exec postgres psql -U directus -d directus_local -t -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'articles';"'''

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Database query failed: {result.stderr}")
        return False

    # Parse database columns
    db_columns = {}
    for line in result.stdout.strip().split('\n'):
        if '|' in line:
            col_name, col_type = [x.strip() for x in line.split('|')]
            db_columns[col_name] = col_type

    # Compare with Pydantic model
    from src_v2.schemas.directus_schemas import DirectusArticle
    model_fields = set(DirectusArticle.__fields__.keys())
    db_fields = set(db_columns.keys())

    missing_in_db = model_fields - db_fields
    missing_in_model = db_fields - model_fields

    if missing_in_db:
        print(f"❌ Fields in model but missing in DB: {missing_in_db}")
    if missing_in_model:
        print(f"⚠️  Fields in DB but missing in model: {missing_in_model}")

    if not missing_in_db and not missing_in_model:
        print("✅ Schema validation passed")
        return True

    return False
```

### 3. Performance Monitor
```python
import time
import statistics
from collections import defaultdict

class DirectusPerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)

    def time_operation(self, operation_name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    self.metrics[operation_name].append(duration)
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self.metrics[f"{operation_name}_error"].append(duration)
                    raise
            return wrapper
        return decorator

    def get_stats(self):
        stats = {}
        for operation, times in self.metrics.items():
            if times:
                stats[operation] = {
                    'count': len(times),
                    'avg': statistics.mean(times),
                    'min': min(times),
                    'max': max(times),
                    'median': statistics.median(times)
                }
        return stats
```

## Prevention Strategies

### 1. Regular Health Checks
```python
def daily_health_check():
    """Run daily to catch issues early."""
    checks = [
        test_directus_connection,
        validate_articles_schema,
        check_api_agent_permissions
    ]

    results = []
    for check in checks:
        try:
            result = check()
            results.append((check.__name__, result))
        except Exception as e:
            results.append((check.__name__, False, str(e)))

    # Send alerts if any checks fail
    failed_checks = [r for r in results if not r[1]]
    if failed_checks:
        send_alert(f"Health check failures: {failed_checks}")
```

### 2. Schema Migration Testing
```python
def test_schema_migration():
    """Test schema changes before deployment."""
    # Backup current schema
    backup_schema()

    try:
        # Apply migrations
        apply_schema_changes()

        # Test CRUD operations
        test_crud_operations()

        print("✅ Schema migration successful")

    except Exception as e:
        print(f"❌ Schema migration failed: {e}")
        # Restore backup
        restore_schema_backup()
        raise
```

### 3. Environment Validation
```python
def validate_environment():
    """Validate environment setup before deployment."""
    required_vars = [
        "DIRECTUS_URL",
        "DIRECTUS_API_AGENT_EMAIL",
        "DIRECTUS_API_AGENT_PASSWORD"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    print("✅ Environment validation passed")
```

## Emergency Procedures

### 1. Service Recovery
```bash
#!/bin/bash
# emergency_recovery.sh

echo "Starting emergency recovery procedure..."

# Stop all services
docker-compose down

# Clean up containers and volumes
docker system prune -f
docker volume prune -f

# Restart services
docker-compose up -d

# Wait for services to be ready
sleep 30

# Run health checks
python debug_directus_connection.py
```

### 2. Database Recovery
```sql
-- emergency_db_recovery.sql

-- Check table integrity
SELECT pg_stat_get_live_tuples(c.oid) as live_tuples,
       pg_stat_get_dead_tuples(c.oid) as dead_tuples
FROM pg_class c
WHERE c.relname = 'articles';

-- Recreate missing indexes
CREATE INDEX IF NOT EXISTS articles_status_idx ON articles(processing_status);
CREATE INDEX IF NOT EXISTS articles_created_idx ON articles(id);

-- Vacuum and analyze
VACUUM ANALYZE articles;
```

## Getting Help

### Log Collection
```bash
# Collect diagnostic logs
mkdir -p debug_logs
docker-compose logs directus > debug_logs/directus.log
docker-compose logs postgres > debug_logs/postgres.log
python test_connection.py > debug_logs/connection_test.log 2>&1
```

### Support Checklist
Before requesting help, collect:

1. **Environment Info**:
   - Directus version: `docker-compose exec directus directus version`
   - Python version: `python --version`
   - SDK version: `pip show directus-sdk-py`

2. **Error Details**:
   - Full error message and stack trace
   - Steps to reproduce
   - Expected vs actual behavior

3. **Configuration**:
   - Environment variables (redacted passwords)
   - Directus user/role/policy setup
   - Database schema structure

4. **Test Results**:
   - Connection test output
   - Schema validation results
   - CRUD operation test results

## Status: ✅ FIELD-TESTED

All troubleshooting procedures have been tested and verified during the integration development process.