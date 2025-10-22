# 🚀 Nexus Learn - Modern Learning Management System

<div align="center">

![Nexus Learn Logo](https://img.shields.io/badge/Nexus-Learn-6366f1?style=for-the-badge&logo=graduation-cap&logoColor=white)

**A comprehensive, fully animated learning management system with real-time sync, advanced admin panel, and Telegram bot integration**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a693?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0+-47a248?style=flat-square&logo=mongodb)](https://mongodb.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-0088cc?style=flat-square&logo=telegram)](https://core.telegram.org/bots)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?style=flat-square&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#license)

[Live Demo](https://nexus-learn-demo.com) • [Documentation](https://docs.nexus-learn.com) • [API Docs](https://api.nexus-learn.com/docs) • [Support](https://t.me/nexuslearn_support)

</div>

## ✨ Features

### 🎨 Modern Animated UI
- ✅ **Fully responsive design** with smooth animations and micro-interactions
- ✅ **Dark/Light theme** support with seamless transitions
- ✅ **Progressive Web App** capabilities for offline functionality  
- ✅ **Custom video player** with advanced controls and progress tracking
- ✅ **Integrated PDF viewer** with zoom, search, and annotation features
- ✅ **Real-time progress synchronization** across all devices
- ✅ **Interactive dashboard** with animated charts and metrics

### 🔐 Advanced Security
- ✅ **JWT authentication** with refresh tokens and role-based access
- ✅ **Password hashing** using bcrypt with salt rounds
- ✅ **Rate limiting** protection against API abuse
- ✅ **CORS protection** with configurable origins
- ✅ **Input validation** with comprehensive request validation
- ✅ **XSS & CSRF protection** with content sanitization

### 🤖 Telegram Bot Integration
- ✅ **Advanced bot** with miniapp launching capabilities
- ✅ **Cloud storage integration** for seamless content management
- ✅ **Real-time notifications** and progress updates
- ✅ **Admin commands** for complete system management
- ✅ **Media upload handling** with automatic processing
- ✅ **User registration** and profile management through Telegram

### 📊 Advanced Admin Panel
- ✅ **Complete user management** - add, edit, delete, assign roles
- ✅ **Course management** - create courses, upload content, manage enrollment
- ✅ **Media management** - drag-and-drop upload with preview capabilities
- ✅ **Real-time analytics** - interactive charts with user engagement metrics
- ✅ **System monitoring** - health checks, performance metrics, live activity
- ✅ **Content moderation** - approve/reject content with permissions
- ✅ **Bulk operations** - mass user actions and batch updates

### ⚡ Real-time Features
- ✅ **WebSocket support** for live updates and notifications
- ✅ **MongoDB Change Streams** for real-time data synchronization
- ✅ **Live progress tracking** with animated progress indicators
- ✅ **Instant notifications** delivered in real-time
- ✅ **Collaborative features** for interactive learning

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for manual installation)
- MongoDB 7+ (for manual installation)
- Redis 7+ (for manual installation)

### Option 1: Docker Deployment (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/educatedlucifer02/nexus-learn-lms.git
cd nexus-learn-lms

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings (especially SECRET_KEY and TELEGRAM_BOT_TOKEN)

# 3. Deploy with one command
./deploy.sh
```

### Option 2: Manual Development Setup

```bash
# 1. Clone and setup
git clone https://github.com/educatedlucifer02/nexus-learn-lms.git
cd nexus-learn-lms

# 2. Install dependencies
cd nexus_learn_backend
pip install -r requirements.txt

# 3. Start services
mongod --replSet rs0
redis-server

# 4. Run application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 🌐 Access Your Application

- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Tech Stack

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES2021+)
- **Features**: WebSocket, Service Worker, File API, Notification API
- **Design**: Responsive, Accessible, Progressive Enhancement
- **Animations**: CSS3 Transitions, Custom Animations

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: MongoDB 7 with Change Streams
- **Cache**: Redis 7 for session management
- **Authentication**: JWT with refresh tokens
- **Real-time**: WebSocket connections
- **Background Tasks**: Celery with Redis broker

### Infrastructure  
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx with SSL termination
- **Monitoring**: Prometheus & Grafana integration
- **Deployment**: Production-ready configuration

## 📱 Telegram Bot Setup

### 1. Create Your Bot

```bash
# Message @BotFather on Telegram
/newbot
# Follow instructions to get your bot token
```

### 2. Configure Bot

```bash
# Add to .env file
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/webhook
TELEGRAM_ADMIN_IDS=123456789,987654321
```

### 3. Bot Commands

- `/start` - Welcome message with miniapp launch
- `/courses` - View enrolled courses with progress
- `/progress` - Detailed learning analytics  
- `/profile` - User profile management
- `/admin` - Admin panel access (admins only)
- `/help` - Comprehensive help system

## 🔌 API Documentation

### Authentication Endpoints
```http
POST /api/auth/register     # User registration
POST /api/auth/login        # User login  
POST /api/auth/refresh      # Refresh token
POST /api/auth/logout       # User logout
GET  /api/auth/me          # Current user info
```

### Admin Endpoints
```http
GET    /api/admin/users           # List all users
POST   /api/admin/users           # Create user
PUT    /api/admin/users/{id}      # Update user
DELETE /api/admin/users/{id}      # Delete user
GET    /api/admin/analytics       # System analytics
```

### Student Endpoints
```http
GET  /api/student/courses         # Get enrolled courses
GET  /api/student/progress        # Get learning progress
POST /api/student/enroll          # Enroll in course
PUT  /api/student/progress        # Update progress
```

### Media Endpoints
```http
POST /api/media/upload            # Upload media file
GET  /api/media/stream/{hash}     # Stream media
GET  /api/media/courses/{id}      # Get course media
```

## 🔒 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment (development/production) | `development` |
| `MONGODB_URL` | MongoDB connection URL | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `nexus_learn_db` |
| `SECRET_KEY` | JWT secret key (min 32 chars) | `change-in-production` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | `None` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `MAX_FILE_SIZE` | Max upload size in bytes | `104857600` (100MB) |

### Feature Flags

| Flag | Description | Default |
|------|-------------|---------|
| `ENABLE_REAL_TIME_SYNC` | Real-time data sync | `True` |
| `ENABLE_WEBSOCKETS` | WebSocket support | `True` |
| `ENABLE_NOTIFICATIONS` | Push notifications | `True` |
| `ENABLE_ANALYTICS` | Analytics tracking | `True` |
| `PROMETHEUS_METRICS` | Prometheus metrics | `True` |

## 🔄 Deployment Options

### Production Deployment

```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d

# With SSL and monitoring
./scripts/setup-ssl.sh
./scripts/setup-monitoring.sh
```

### Cloud Deployment

#### AWS ECS
```bash
# Deploy to AWS ECS
aws ecs create-cluster --cluster-name nexus-learn
./scripts/deploy-aws.sh
```

#### Google Cloud Run
```bash
# Deploy to Google Cloud Run  
gcloud run deploy nexus-learn --source .
```

#### DigitalOcean App Platform
```bash
# Deploy to DigitalOcean
doctl apps create --spec .do/app.yaml
```

## 📋 Monitoring & Analytics

### Built-in Monitoring
- **Health Check Endpoint**: `/health`
- **Metrics Endpoint**: `/metrics` (Prometheus format)
- **Real-time Dashboard**: Admin panel analytics section
- **Error Tracking**: Structured logging with error capture

### External Monitoring Setup
```bash
# Start monitoring stack
docker-compose -f monitoring/docker-compose.yml up -d

# Access Grafana: http://localhost:3000
# Access Prometheus: http://localhost:9090
```

## 🛠️ Development

### Project Structure
```
nexus-learn-lms/
├── nexus_learn_backend/     # Backend application
│   ├── app/                 # Main application code
│   │   ├── api/             # API routes
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic
│   │   ├── telegram/        # Telegram bot
│   │   └── utils/           # Utilities
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Docker configuration
├── frontend/               # Frontend application (served by FastAPI)
├── scripts/                # Deployment scripts
├── monitoring/             # Monitoring configuration
├── docker-compose.yml      # Development setup
├── docker-compose.prod.yml # Production setup
└── .env.example            # Environment template
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

### Code Quality
```bash
# Format code
black app/
isort app/

# Lint code  
flake8 app/
mypy app/

# Security check
bandit -r app/
```

## 🔍 Troubleshooting

### Common Issues

**MongoDB Connection Failed**
```bash
# Check MongoDB status
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

**Telegram Bot Not Responding**
```bash
# Check bot token
echo $TELEGRAM_BOT_TOKEN

# Verify webhook
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo
```

**File Upload Issues**
```bash
# Check upload directory permissions
ls -la uploads/

# Fix permissions
chmod 755 uploads/
chown -R 1000:1000 uploads/
```

### Debugging
```bash
# View application logs
docker-compose logs -f nexus-learn-app

# View all service logs
docker-compose logs -f

# Enter container for debugging
docker-compose exec nexus-learn-app bash
```

## 🔄 Updates & Maintenance

### Updating the System
```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Database Backup
```bash
# Create backup
./scripts/backup-database.sh

# Restore from backup
./scripts/restore-database.sh backup-file.gz
```

### Security Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Update Docker images
docker-compose pull
docker-compose up -d
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for your changes
5. Run tests: `pytest`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Roadmap

### Version 2.1 (Next Release)
- [ ] Advanced AI-powered recommendations
- [ ] Blockchain certificates and NFT badges
- [ ] Advanced video analytics with engagement tracking
- [ ] Multi-language support (i18n)
- [ ] Advanced reporting and exports

### Version 2.2 (Future)
- [ ] Virtual classroom integration
- [ ] Advanced proctoring system
- [ ] Gamification features
- [ ] Social learning features
- [ ] Advanced analytics with ML insights

## 🎆 Support

- 📧 **Email**: support@nexuslearn.com
- 💬 **Telegram**: [@nexuslearn_support](https://t.me/nexuslearn_support)
- 📚 **Documentation**: [docs.nexuslearn.com](https://docs.nexuslearn.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/educatedlucifer02/nexus-learn-lms/issues)
- 📰 **Discussions**: [GitHub Discussions](https://github.com/educatedlucifer02/nexus-learn-lms/discussions)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The amazing web framework
- [MongoDB](https://mongodb.com/) - The flexible database
- [Telegram Bot API](https://core.telegram.org/bots/api) - Bot integration
- [Docker](https://docker.com/) - Containerization platform
- All the amazing contributors and users!

---

<div align="center">

**Made with ❤️ by the Nexus Learn Team**

[![GitHub Stars](https://img.shields.io/github/stars/educatedlucifer02/nexus-learn-lms?style=social)](https://github.com/educatedlucifer02/nexus-learn-lms/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/educatedlucifer02/nexus-learn-lms?style=social)](https://github.com/educatedlucifer02/nexus-learn-lms/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/educatedlucifer02/nexus-learn-lms)](https://github.com/educatedlucifer02/nexus-learn-lms/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/educatedlucifer02/nexus-learn-lms)](https://github.com/educatedlucifer02/nexus-learn-lms/pulls)

</div>