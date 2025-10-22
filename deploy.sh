#!/bin/bash

# Nexus Learn Deployment Script
# This script automates the deployment process

set -e

echo "🚀 Starting Nexus Learn Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads logs static temp

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing."
    echo "Press Enter to continue after editing .env file..."
    read -r
fi

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Test API endpoint
echo "🧪 Testing API endpoint..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API is responding!"
else
    echo "❌ API is not responding. Check logs:"
    docker-compose logs nexus-learn-app
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "🌐 Access your application:"
echo "   Main App: http://localhost:8000"
echo "   Admin Panel: http://localhost:8000/admin"
echo "   API Docs: http://localhost:8000/api/docs"
echo ""
echo "📊 Monitor your application:"
echo "   Health Check: http://localhost:8000/health"
echo "   Logs: docker-compose logs -f"
echo ""
echo "🤖 Next steps:"
echo "   1. Configure your Telegram bot token in .env"
echo "   2. Set up your domain and SSL certificate"
echo "   3. Configure backup schedules"
echo "   4. Set up monitoring and alerts"