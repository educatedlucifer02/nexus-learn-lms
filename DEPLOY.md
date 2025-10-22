# 🚀 Nexus Learn - Render Deployment Guide

## Overview
This repository is configured for **unified deployment** on Render, serving both the FastAPI backend and static frontend files through a single web service.

## 📦 Deployment Files

### Core Files
- `Dockerfile` - Unified container configuration for both backend and frontend
- `main.py` - Combined FastAPI application serving API and static files
- `render.yaml` - Render service configuration (optional)

### Configuration Files
- `nginx.conf` - Nginx configuration for production optimization
- `supervisord.conf` - Multi-service management configuration

## 🔧 Quick Deploy to Render

### Method 1: One-Click Deploy (Recommended)

1. **Fork/Clone this repository**
2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `nexus-learn-lms` repository

3. **Configure Service:**
   ```
   Name: nexus-learn-lms
   Environment: Python 3
   Build Command: pip install -r nexus_learn_backend/requirements.txt
   Start Command: python main.py
   ```

4. **Set Environment Variables:**
   ```
   PYTHON_VERSION=3.11.0
   ENVIRONMENT=production
   SECRET_KEY=your-secret-key-here
   MONGODB_URL=your-mongodb-connection-string
   DATABASE_NAME=nexus_learn_db
   ```

### Method 2: Using render.yaml

1. Place `render.yaml` in your repository root
2. In Render Dashboard, click "New +" → "Blueprint"
3. Connect repository and deploy

## 🌍 Environment Variables

### Required Variables
```env
SECRET_KEY=your-super-secret-key-minimum-32-characters
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=nexus_learn_db
```

### Optional Variables
```env
ENVIRONMENT=production
DEBUG=false
ALLOWED_HOSTS=your-domain.onrender.com,localhost
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_WEBHOOK_URL=https://your-app.onrender.com/webhook
```

## 📊 Database Setup

### MongoDB Atlas (Recommended)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get connection string
4. Add to Render environment variables

### Render PostgreSQL (Alternative)
```yaml
databases:
  - name: nexus-learn-db
    databaseName: nexus_learn_db
    user: nexus_user
```

## 🔗 Access URLs

After deployment, your application will be available at:

- **Main Application:** `https://your-app-name.onrender.com`
- **Admin Panel:** `https://your-app-name.onrender.com/admin`
- **Student Portal:** `https://your-app-name.onrender.com/student`
- **API Documentation:** `https://your-app-name.onrender.com/api/docs`
- **Health Check:** `https://your-app-name.onrender.com/health`

## 🐛 Troubleshooting

### Common Issues

**1. Build Failures**
```bash
# Check Python dependencies
pip install -r nexus_learn_backend/requirements.txt

# Verify file paths
ls -la frontend/
ls -la static/
```

**2. Database Connection Issues**
```env
# Ensure MongoDB URL is correct
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/dbname?retryWrites=true&w=majority
```

**3. Static Files Not Loading**
- Verify `frontend/` and `static/` directories exist
- Check file permissions in Dockerfile
- Ensure FastAPI static file mounting is correct

**4. WebSocket Connection Issues**
- WebSocket endpoint: `wss://your-app.onrender.com/ws/main`
- Check browser console for connection errors

### Logs and Debugging
```bash
# View application logs in Render dashboard
# Or check specific service logs:
docker logs <container-id>
```

## 🔧 Local Development

### Using Docker
```bash
# Build and run locally
docker build -t nexus-learn .
docker run -p 8000:8000 nexus-learn
```

### Using Python directly
```bash
# Install dependencies
pip install -r nexus_learn_backend/requirements.txt

# Run application
python main.py
```

### Access Local Application
- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin
- API Docs: http://localhost:8000/api/docs

## 🚀 Production Optimizations

### Performance
- Nginx reverse proxy (included in Dockerfile)
- Gzip compression enabled
- Static file caching
- WebSocket connection pooling

### Security
- CORS configuration
- Trusted host middleware
- Environment variable management
- Non-root user execution

### Monitoring
- Health check endpoint
- Structured logging
- WebSocket connection tracking
- Database connection monitoring

## 📈 Scaling Options

### Free Tier Limitations
- Single web service
- 512 MB RAM
- Sleeps after 15 minutes of inactivity

### Paid Tier Benefits
- Multiple services
- Auto-scaling
- Always-on availability
- Custom domains
- SSL certificates

## 🔄 Deployment Updates

### Automatic Deployment
- Push changes to main branch
- Render automatically rebuilds and deploys
- Zero-downtime deployment

### Manual Deployment
```bash
# In Render dashboard
1. Go to your service
2. Click "Manual Deploy"
3. Select branch to deploy
```

## 📚 Additional Resources

- Render Documentation
- FastAPI Documentation
- MongoDB Atlas Setup
- Docker Best Practices

## 💡 Tips for Success

1. **Always test locally first** before deploying
2. **Use environment variables** for sensitive data
3. **Monitor application logs** for issues
4. **Set up database backups** for production
5. **Configure custom domain** for professional appearance
6. **Enable SSL certificates** for security
7. **Set up monitoring alerts** for uptime tracking

## 🆘 Support

If you encounter issues:
1. Check Render service logs
2. Verify environment variables
3. Test database connectivity
4. Review application health check endpoint
5. Contact Render support for platform issues

---

**Happy Deploying! 🎉**
