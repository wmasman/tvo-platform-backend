# Directus Backend Integration Setup Guide

## Overview

This guide provides step-by-step instructions for setting up Directus CMS to work with the TVO Backend Python pipeline. It covers API Agent user creation, permission configuration, and database schema requirements.

## Prerequisites

- Directus v11.12.0+ running locally or in production
- PostgreSQL database backend
- Administrator access to Directus UI
- TVO Backend codebase with Python 3.13

## Setup Steps

### 1. Create API Agent User

1. **Navigate to Settings → Access Control → Users**
2. **Click "Create New"**
3. **Fill in user details:**
   ```
   First Name: API
   Last Name: Agent
   Email: api-agent@tvo.local.nl
   Password: SecureApiPassword123!
   Status: Active
   ```
4. **Save the user**

### 2. Create API Agent Role

1. **Navigate to Settings → Access Control → User Roles**
2. **Click "Create New"**
3. **Configure role:**
   ```
   Name: API Agent
   Icon: compare_arrows
   Description: Dedicated API user for Python integration
   Admin Access: NO
   App Access: NO
   ```
4. **Save the role**

### 3. Create API Agent Policy

1. **Navigate to Settings → Access Control → Access Policies**
2. **Click "Create New"**
3. **Configure policy:**
   ```
   Name: API Agent Full Access
   Icon: compare_arrows
   Description: Full API access for Python integration - bypasses Administrator role bugs
   Admin Access: NO
   App Access: NO
   ```
4. **Save the policy**

### 4. Configure Collection Permissions

For each collection that the backend needs to access, add permissions to the **API Agent Full Access** policy:

1. **Navigate to Settings → Access Control → Access Policies**
2. **Select "API Agent Full Access" policy**
3. **Add permissions for each collection:**

#### Articles Collection (Required)
```
Collection: articles
Actions: create, read, update, delete
Fields: * (all fields)
Permissions: {} (no restrictions)
```

#### Other Collections (Add as needed)
- `authors` - Full CRUD
- `processing_logs` - Full CRUD
- `patterns` - Full CRUD
- Any other collections the backend will use

### 5. Assign Policy to Role and User

#### Assign Policy to Role
1. **Navigate to Settings → Access Control → User Roles**
2. **Edit "API Agent" role**
3. **In Policies section, add "API Agent Full Access"**
4. **Save**

#### Assign Role to User
1. **Navigate to Settings → Access Control → Users**
2. **Edit the API Agent user**
3. **Set Role to "API Agent"**
4. **Assign "API Agent Full Access" policy directly to user**
5. **Save**

### 6. Database Schema Setup

Ensure the articles table has all required columns:

```sql
-- Connect to your Directus database
-- For local development:
docker-compose exec postgres psql -U directus -d directus_local

-- Add missing columns if they don't exist
ALTER TABLE articles ADD COLUMN IF NOT EXISTS authors json;
ALTER TABLE articles ADD COLUMN IF NOT EXISTS "references" json;

-- Verify table structure
\d articles;
```

Expected articles table structure:
```sql
Column                         | Type                     | Nullable
-------------------------------|--------------------------|----------
id                            | integer                  | not null
title                         | character varying(255)   |
publication_date              | timestamp with time zone |
content                       | text                     |
processing_status             | character varying(255)   |
summary_card                  | text                     |
summary_detail                | text                     |
small_image_url               | character varying(255)   |
estimated_reading_time_minutes| integer                  |
article_type                  | character varying(255)   |
separated_content             | json                     |
base_content_flow             | json                     |
content_flow_cache            | json                     |
article_metadata              | json                     |
authors                       | json                     |
references                    | json                     |
```

## Verification Steps

### 1. Test API Agent Authentication

Create a test script to verify the setup:

```python
import requests

DIRECTUS_URL = "http://localhost:8055"
API_AGENT_EMAIL = "api-agent@tvo.local.nl"
API_AGENT_PASSWORD = "SecureApiPassword123!"

# Test authentication
auth_response = requests.post(f"{DIRECTUS_URL}/auth/login", json={
    "email": API_AGENT_EMAIL,
    "password": API_AGENT_PASSWORD
})

if auth_response.status_code == 200:
    print("✅ API Agent authentication successful")
    token = auth_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test article creation
    test_article = {
        "title": "Test Article",
        "processing_status": "pending"
    }

    create_response = requests.post(
        f"{DIRECTUS_URL}/items/articles",
        headers=headers,
        json=test_article
    )

    if create_response.status_code in [200, 201]:
        print("✅ Article creation successful")
        article_id = create_response.json()["data"]["id"]
        print(f"Created article ID: {article_id}")

        # Clean up
        requests.delete(f"{DIRECTUS_URL}/items/articles/{article_id}", headers=headers)
        print("✅ Test cleanup successful")
    else:
        print(f"❌ Article creation failed: {create_response.json()}")
else:
    print(f"❌ Authentication failed: {auth_response.json()}")
```

### 2. Verify Permissions

Check that the API Agent user has proper permissions:

1. **Navigate to Settings → Access Control → Users**
2. **Edit API Agent user**
3. **Verify:**
   - Role is set to "API Agent"
   - "API Agent Full Access" policy is assigned
   - Status is "Active"

## Common Issues & Solutions

### Issue: 403 FORBIDDEN on article operations
**Cause**: Missing permissions for articles collection
**Solution**: Ensure articles collection has create/read/update/delete permissions in the API Agent Full Access policy

### Issue: 500 SERVER ERROR with column not found
**Cause**: Database schema missing required columns
**Solution**: Run the database schema setup commands above

### Issue: API returns Role: None for API Agent
**Cause**: Role assignment not properly saved
**Solution**:
1. Edit API Agent user in UI
2. Re-assign the role
3. Save
4. Restart Directus service

### Issue: UUID vs Integer ID conflicts
**Cause**: Backend trying to set UUID for auto-increment integer field
**Solution**: Let database handle ID auto-increment, don't set manually

## Best Practices

### Security
1. **Use dedicated API Agent user** - Don't use Administrator for API operations
2. **Scope permissions** - Only grant access to collections the backend needs
3. **Secure credentials** - Store API Agent password in environment variables
4. **Audit trails** - Monitor API Agent user activity in Directus logs

### Performance
1. **Connection pooling** - Reuse DirectusClient instances when possible
2. **Batch operations** - Group related API calls together
3. **Caching** - Cache authentication tokens until expiry
4. **Error handling** - Implement retry logic for transient failures

### Maintenance
1. **Schema validation** - Keep Pydantic models in sync with Directus schema
2. **Version compatibility** - Test with Directus updates before upgrading
3. **Backup strategy** - Regular backups of Directus database
4. **Monitor API usage** - Track API rate limits and usage patterns

## Integration Testing

Use the backend test suite to verify the integration:

```bash
cd tvoo_backend
export PYTHONPATH=.
python scripts/utilities/test_directus_service.py
```

Expected output:
```
Initializing DirectusService...

--- Testing create_item ---
Successfully created article with ID: 123

--- Testing get_item ---
Successfully fetched article: [Test Article] My New Article

--- Testing update_item ---
Successfully updated article status to: completed

--- Testing delete_item ---
Successfully deleted article with ID: 123
```

## Production Considerations

### Environment Variables
```bash
# Production .env
DIRECTUS_URL="https://your-directus-instance.com"
DIRECTUS_API_AGENT_EMAIL="api-agent@yourdomain.com"
DIRECTUS_API_AGENT_PASSWORD="your-secure-password"
```

### SSL/TLS
- Ensure Directus is served over HTTPS in production
- Validate SSL certificates in API calls
- Use secure password for API Agent user

### Rate Limiting
- Monitor Directus API rate limits
- Implement exponential backoff for failed requests
- Consider API key authentication for higher limits

## Support & Troubleshooting

For additional support:
1. Check Directus logs: `docker-compose logs directus`
2. Check PostgreSQL logs: `docker-compose logs postgres`
3. Review API Agent user activity in Directus UI
4. Verify network connectivity between backend and Directus

## Status: ✅ PRODUCTION READY

This setup has been tested and verified for both development and production use.