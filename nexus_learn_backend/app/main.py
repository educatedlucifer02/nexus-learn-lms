#!/usr/bin/env python3
"""
Nexus Learn - Modern Animated Learning Management System
A comprehensive LMS with real-time sync, advanced admin panel, and Telegram bot integration
"""

import os
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from app.config import get_settings
from app.database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
settings = get_settings()
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global db
    
    try:
        # Initialize database
        db = Database()
        await db.connect()
        logger.info("✅ Database connected successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
        raise
    finally:
        # Cleanup
        if db:
            await db.disconnect()
            logger.info("🔄 Database disconnected")

# Create FastAPI app
app = FastAPI(
    title="Nexus Learn - Modern Learning Management System",
    description="Comprehensive LMS with real-time features, advanced admin panel, and Telegram integration",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Create directories
Path("static").mkdir(exist_ok=True)
Path("uploads").mkdir(exist_ok=True)
Path("temp").mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# WebSocket manager for real-time features
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.user_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str, user_id: int = None):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        
        if user_id:
            self.user_connections[user_id] = websocket
        
        logger.info(f"🔗 WebSocket connected: {client_id}")

    def disconnect(self, websocket: WebSocket, client_id: str, user_id: int = None):
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
        
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
        
        logger.info(f"🔌 WebSocket disconnected: {client_id}")

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, user_id: int = None):
    await manager.connect(websocket, client_id, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong", "timestamp": datetime.utcnow().isoformat()})
            else:
                # Echo back for now - implement specific handlers
                await websocket.send_json({"type": "echo", "data": data})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id, user_id)

# Main application routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Landing page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nexus Learn - Modern Learning Platform</title>
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                text-align: center;
                padding: 2rem;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            h1 { font-size: 3rem; margin-bottom: 1rem; }
            p { font-size: 1.2rem; opacity: 0.9; }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 2rem;
            }
            .feature {
                padding: 1rem;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                transition: transform 0.3s ease;
            }
            .feature:hover {
                transform: translateY(-5px);
            }
            .api-links {
                margin-top: 2rem;
            }
            .api-links a {
                color: #fff;
                text-decoration: none;
                margin: 0 1rem;
                padding: 0.5rem 1rem;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 25px;
                transition: all 0.3s ease;
            }
            .api-links a:hover {
                background: rgba(255,255,255,0.2);
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Nexus Learn</h1>
            <p>Modern Animated Learning Management System</p>
            
            <div class="features">
                <div class="feature">
                    <h3>🎨 Modern UI</h3>
                    <p>Fully animated and responsive interface</p>
                </div>
                <div class="feature">
                    <h3>📱 Telegram Bot</h3>
                    <p>Integrated bot for seamless access</p>
                </div>
                <div class="feature">
                    <h3>📊 Real-time Analytics</h3>
                    <p>Live progress tracking and insights</p>
                </div>
                <div class="feature">
                    <h3>🔐 Advanced Security</h3>
                    <p>JWT authentication with role-based access</p>
                </div>
            </div>
            
            <div class="api-links">
                <a href="/api/docs">📚 API Documentation</a>
                <a href="/health">💚 Health Check</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Enhanced health check with system status"""
    try:
        # Check database
        db_status = "disconnected"
        if db:
            try:
                await db.ping()
                db_status = "connected"
            except:
                db_status = "error"
        
        return {
            "status": "healthy" if db_status == "connected" else "partial",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0",
            "components": {
                "database": db_status,
                "websocket": "active"
            },
            "features": {
                "real_time_sync": True,
                "media_streaming": True,
                "advanced_analytics": True,
                "telegram_integration": True
            }
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/api/system/info")
async def system_info():
    """Get comprehensive system information"""
    return {
        "system_name": "Nexus Learn - Modern Learning Management System",
        "version": "2.0.0",
        "description": "Comprehensive LMS with real-time sync, advanced admin panel, and Telegram integration",
        "features": {
            "modern_animated_ui": True,
            "real_time_sync": True,
            "advanced_admin_panel": True,
            "telegram_bot_integration": True,
            "media_streaming": True,
            "advanced_analytics": True,
            "websocket_support": True,
            "mobile_responsive": True
        },
        "api_endpoints": {
            "authentication": "/api/auth/*",
            "admin": "/api/admin/*",
            "student": "/api/student/*",
            "media": "/api/media/*",
            "analytics": "/api/analytics/*"
        },
        "websocket": "/ws/{client_id}",
        "documentation": "/api/docs",
        "timestamp": datetime.utcnow().isoformat()
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return {"error": "Resource not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    logger.error(f"Internal error: {exc}")
    return {"error": "Internal server error", "status_code": 500}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False,
        log_level="info"
    )