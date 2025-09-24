const axios = require('axios');
const fs = require('fs');
const yaml = require('js-yaml');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env.local') });

// --- Configuration ---
const DIRECTUS_URL = 'http://localhost:8055';
const ADMIN_EMAIL = process.env.ADMIN_EMAIL;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;
const SCHEMA_PATH = path.join(__dirname, '../schema/schema_pipeline.yml');

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

async function getAdminRoleId() {
    try {
        const response = await api.get('/roles');
        const adminRole = response.data.data.find(role => role.name === 'Administrator');
        if (adminRole) {
            log('Found Administrator role.');
            return adminRole.id;
        }
        throw new Error('Administrator role not found.');
    } catch (err) {
        error('Failed to get Administrator role ID.', err.response ? err.response.data : err.message);
        throw err;
    }
}

async function getBuiltInAdminPolicy() {
    try {
        // Find the built-in Administrator policy with admin_access: true
        const policiesResponse = await api.get('/policies');
        const adminPolicy = policiesResponse.data.data.find(policy =>
            policy.name === 'Administrator' && policy.admin_access === true
        );

        if (adminPolicy) {
            log(`Found built-in Administrator policy with ID: ${adminPolicy.id}`);
            return adminPolicy.id;
        }

        throw new Error('Built-in Administrator policy not found.');
    } catch (err) {
        error('Failed to get built-in Administrator policy.', err.response ? err.response.data : err.message);
        throw err;
    }
}

async function linkPolicyToCurrentUser(policyId) {
    try {
        log(`Linking policy ${policyId} to current user...`);

        // Get current user info
        const userResponse = await api.get('/users/me');
        const currentUser = userResponse.data.data;
        const currentPolicies = currentUser.policies || [];

        if (currentPolicies.some(p => p === policyId || (typeof p === 'object' && p.id === policyId))) {
            log('Policy already linked to user.');
            return;
        }

        // Add policy to current user
        await api.patch(`/users/${currentUser.id}`, {
            policies: [...currentPolicies, policyId]
        });

        log('Policy linked to current user successfully.');
    } catch (err) {
        error('Failed to link policy to current user.', err.response ? err.response.data : err.message);
        // Don't throw - this might not be necessary for admin users
    }
}

// --- Main Execution ---
async function syncSchema() {
    let adminRoleId;
    let adminPolicyId;
    try {
        await authenticateWithRetry();
        adminRoleId = await getAdminRoleId();
        adminPolicyId = await getBuiltInAdminPolicy();

        // Try to link policy to current user instead of role
        await linkPolicyToCurrentUser(adminPolicyId);

        await grantPermissions(adminPolicyId, 'directus_permissions');
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
                await grantPermissions(adminPolicyId, collection.collection);
            } catch (err) {
                error(`Failed to create collection "${collection.collection}".`, err.response ? err.response.data : err.message);
            }
        } else {
            // Collection exists, still grant permissions in case they're missing
            await grantPermissions(adminPolicyId, collection.collection);
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

async function grantPermissions(policyId, collectionName) {
    const actions = ['create', 'read', 'update', 'delete'];

    try {
        log(`Granting permissions for "${collectionName}" to policy...`);

        for (const action of actions) {
            try {
                await api.post('/permissions', {
                    collection: collectionName,
                    action: action,
                    permissions: {},
                    validation: {},
                    presets: {},
                    fields: '*',
                    policy: policyId
                });
                log(`Permission "${action}" granted for "${collectionName}".`);
            } catch (permErr) {
                error(`Failed to grant "${action}" permission for "${collectionName}".`, permErr.response ? permErr.response.data : permErr.message);
            }
        }

        log(`All permissions granted for "${collectionName}".`);
    } catch (err) {
        error(`Failed to grant permissions for "${collectionName}".`, err.response ? err.response.data : err.message);
    }
}

syncSchema();