# 🚀 Directus Deployment Checklist

## Pre-Deployment (Local Testing)
- [ ] Ensure your Directus works locally with `docker compose up`
- [ ] Test your schema creation script: `npm run schema-http`
- [ ] Commit all changes to GitHub
- [ ] Generate secure keys for production:
  ```bash
  node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
  ```

## Railway Deployment Steps

### 1. Setup Railway Account
- [ ] Sign up at [railway.app](https://railway.app)
- [ ] Connect your GitHub account
- [ ] Install Railway CLI: `npm install -g @railway/cli`

### 2. Create Project
- [ ] Create new project in Railway
- [ ] Connect your GitHub repository
- [ ] Add PostgreSQL database from template marketplace

### 3. Configure Environment Variables
Add these in Railway dashboard under Variables:
- [ ] `KEY` = (32-character random string)
- [ ] `SECRET` = (random secret string)  
- [ ] `ADMIN_EMAIL` = your admin email
- [ ] `ADMIN_PASSWORD` = secure password
- [ ] `NODE_ENV` = production

### 4. Deploy
- [ ] Railway auto-detects your Dockerfile
- [ ] First deployment may take 3-5 minutes
- [ ] Check deployment logs for any errors
- [ ] Access your app via the generated Railway URL

### 5. Post-Deployment Setup
- [ ] Login to Directus admin at `https://your-app.railway.app`
- [ ] Run schema creation: update your script to use production URL
- [ ] Test creating content
- [ ] Configure custom domain (optional)

## Alternative: Render Deployment

### 1. Setup Render Account  
- [ ] Sign up at [render.com](https://render.com)
- [ ] Connect GitHub repository

### 2. Create Services
- [ ] Create PostgreSQL database
- [ ] Create Web Service from Docker image
- [ ] Link database to web service

### 3. Environment Configuration
Same variables as Railway, plus:
- [ ] `DATABASE_URL` = (auto-provided by Render)

## Troubleshooting

### Common Issues:
1. **Build fails**: Check Dockerfile and ensure all files are committed
2. **Database connection fails**: Verify environment variables
3. **File uploads fail**: Check volume mount configuration
4. **Schema creation fails**: Use HTTP API method instead of CLI

### Useful Commands:
```bash
# Railway
railway login
railway link
railway logs
railway shell

# Local testing
docker compose -f docker-compose.railway.yml up
npm run schema-http
```

## Cost Optimization Tips

1. **Start small**: Use hobby tiers initially
2. **Monitor usage**: Check monthly costs regularly  
3. **Consider VPS**: If costs exceed $25/month
4. **Use CDN**: For file storage optimization
5. **Database optimization**: Regular cleanup of logs/revisions

## Next Steps After Deployment

1. **Custom Domain**: Point your domain to Railway/Render
2. **SSL Certificate**: Auto-provisioned by platform
3. **Backups**: Set up automated database backups
4. **Monitoring**: Add uptime monitoring
5. **CI/CD**: Automate deployments on GitHub push

## Getting Help

- Railway: [docs.railway.app](https://docs.railway.app)
- Render: [render.com/docs](https://render.com/docs)  
- Directus: [docs.directus.io](https://docs.directus.io)
- Issues: Check platform status pages first
