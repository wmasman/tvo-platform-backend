const axios = require('axios');
const fs = require('fs');
const yaml = require('js-yaml');
const path = require('path');

// --- Configuration ---
const DIRECTUS_URL = 'http://localhost:8055';
const ADMIN_EMAIL = 'wmasman@gmail.com';
const ADMIN_PASSWORD = 'password';
const SCHEMA_PATH = path.join(__dirname, 'migrations', 'schema_fixed.yml');

// --- Axios Instance ---
const api = axios.create({
    baseURL: DIRECTUS_URL,
});

// --- Helper Functions ---
const log = (message) => console.log(`[INFO] ${message}`);
const error = (message, details) => console.error(`[ERROR] ${message}`, details || '');
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// --- Authentication with Retry ---
async function authenticateWithRetry(retries = 5, delayMs = 5000) {
    for (let i = 0; i < retries; i++) {
        try {
            log(`Authentication attempt ${i + 1}/${retries}...`);
            const response = await api.post('/auth/login', {
                email: ADMIN_EMAIL,
                password: ADMIN_PASSWORD,
            });
            const accessToken = response.data.data.access_token;
            api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
            log('Authentication successful.');
            return accessToken;
        } catch (err) {
            error(`Authentication attempt ${i + 1} failed.`, err.response ? err.response.data : err.message);
            if (i < retries - 1) {
                log(`Waiting ${delayMs / 1000}s before retrying...`);
                await delay(delayMs);
            }
        }
    }
    throw new Error('Authentication failed after multiple retries.');
}

// --- Main Execution ---
async function syncSchema() {
    try {
        await authenticateWithRetry();
    } catch (err) {
        error(err.message);
        return;
    }

    // 1. Get Schemas
    const localSchema = yaml.load(fs.readFileSync(SCHEMA_PATH, 'utf8'));
    const remoteSchemaResponse = await api.get('/schema/snapshot');
    const remoteSchema = remoteSchemaResponse.data.data;

    const localCollections = localSchema.collections.map(c => c.collection);
    const remoteCollections = remoteSchema.collections.map(c => c.collection);

    // 2. Collections to Delete
    const collectionsToDelete = remoteCollections.filter(rc => !localCollections.includes(rc) && !rc.startsWith('directus_'));
    for (const collectionName of collectionsToDelete) {
        try {
            log(`Deleting collection: ${collectionName}`);
            await api.delete(`/collections/${collectionName}`);
            log(`Collection "${collectionName}" deleted.`);
        } catch (err) {
            error(`Failed to delete collection "${collectionName}".`, err.response ? err.response.data : err.message);
        }
    }

    // 3. Collections to Create
    for (const collection of localSchema.collections) {
        if (!remoteCollections.includes(collection.collection)) {
            try {
                log(`Creating collection: ${collection.collection}`);
                await api.post('/collections', {
                    collection: collection.collection,
                    meta: collection.meta,
                    schema: collection.schema,
                });
                log(`Collection "${collection.collection}" created.`);
            } catch (err) {
                error(`Failed to create collection "${collection.collection}".`, err.response ? err.response.data : err.message);
            }
        }

        // 4. Fields to Create/Delete
        const remoteCollection = remoteSchema.collections.find(rc => rc.collection === collection.collection);
        const localFields = collection.fields.map(f => f.field);
        const remoteFields = remoteCollection && Array.isArray(remoteCollection.fields) ? remoteCollection.fields.map(f => f.field) : [];

        // Fields to delete
        const fieldsToDelete = remoteFields.filter(rf => !localFields.includes(rf));
        for (const fieldName of fieldsToDelete) {
            try {
                log(`Deleting field "${fieldName}" from "${collection.collection}"`);
                await api.delete(`/fields/${collection.collection}/${fieldName}`);
                log(`Field "${fieldName}" deleted.`);
            } catch (err) {
                error(`Failed to delete field "${fieldName}".`, err.response ? err.response.data : err.message);
            }
        }

        // Fields to create
        for (const field of collection.fields) {
            if (!remoteFields.includes(field.field)) {
                try {
                    log(`Creating field "${field.field}" in "${collection.collection}"...`);
                    await api.post(`/fields/${collection.collection}`, {
                        field: field.field,
                        type: field.type,
                        meta: field.meta,
                        schema: field.schema,
                    });
                    log(`Field "${field.field}" created.`);
                } catch (err) {
                    error(`Failed to create field "${field.field}" in "${collection.collection}".`, err.response ? err.response.data : err.message);
                }
            }
        }
    }

    log('Schema sync process complete.');
}

syncSchema();