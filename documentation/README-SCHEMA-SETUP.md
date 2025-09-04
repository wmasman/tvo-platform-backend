# Directus Schema Setup - Working Solutions

Based on extensive troubleshooting, the Directus CLI `schema apply` command has known bugs. Here are the working alternatives:

## Option 1: HTTP API Approach (Recommended)

This bypasses all CLI issues by using direct HTTP API calls.

### Steps:
1. **Start Directus**: `docker compose up -d`
2. **Wait for initialization**: Give it 30-60 seconds to fully boot
3. **Install dependencies**: `npm install`
4. **Run schema creation**: `npm run schema-http`

### What it does:
- Authenticates with your admin credentials
- Creates collections via HTTP API
- Creates fields for each collection
- Provides clear progress feedback
- Skips existing collections/fields automatically

### Credentials:
The script uses the credentials from your `docker-compose.yml`:
- Email: `admin@example.com`
- Password: `password`

If you've changed these, update them in `http-api-schema.js`.

## Option 2: Manual Setup (Fallback)

If the HTTP API approach fails:

1. Go to `http://localhost:8055`
2. Login with admin credentials
3. Create collections manually:
   - articles (with title, publication_date fields)
   - authors (with name field)
   - concepts (with name field)
   - insights (with title, creationDate fields)
   - comments (with text field)
   - thematic_collections (with title field)

## Option 3: Alternative CLI Approach

If you want to try the CLI again with the fixed schema:

```bash
docker exec -it directus npx directus schema apply --yes /directus/migrations/schema_fixed.yml
```

⚠️ **Warning**: This is likely to still fail with the `filter` error.

## Troubleshooting

### If authentication fails:
- Check if Directus is running: `docker compose ps`
- Check if the admin user exists: `docker compose logs directus`
- Verify credentials match your docker-compose.yml

### If collections already exist:
- The script will skip existing collections automatically
- Or reset the database: `docker compose down && rm -rf database uploads && docker compose up -d`

### If you get module errors:
- Run `npm install` again
- Delete `node_modules` and `package-lock.json`, then `npm install`

## Why This Works

The HTTP API endpoints are more stable and reliable than the CLI commands. This approach:
- ✅ Bypasses CLI bugs entirely
- ✅ Uses the same API that the admin interface uses
- ✅ Has proper error handling
- ✅ Works consistently across Directus versions
- ✅ Can be easily extended for more complex schemas

## Next Steps

Once your schema is created successfully:
1. Access the admin interface at `http://localhost:8055`
2. Configure field interfaces and displays as needed
3. Set up relationships between collections
4. Add sample data for testing

## Schema Extension

To add more collections or fields, edit `http-api-schema.js` and add them to the respective arrays. The script structure makes it easy to extend.
