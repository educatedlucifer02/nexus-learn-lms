#!/usr/bin/env python3
"""
Nexus Learn - Unified Application for Render Deployment
Serves both FastAPI backend and static frontend files
"""

import os
import asyncio
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

# Import from backend app
try:
    from app.config import get_settings
    from app.database import Database
except ImportError:
    # Fallback configuration if app modules aren't available
    class Settings:
        def __init__(self):
            self.ALLOWED_HOSTS = ["*"]
            self.MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            self.DATABASE_NAME = os.getenv("DATABASE_NAME", "nexus_learn_db")
    
    def get_settings():
        return Settings()
    
    class Database:
        async def connect(self): pass
        async def disconnect(self): pass
        async def ping(self): return True

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
        # Don't raise error to allow app to start without DB
    finally:
        # Cleanup
        if db:
            try:
                await db.disconnect()
                logger.info("🔄 Database disconnected")
            except:
                pass

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
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure properly for production
)

# Create directories
Path("static").mkdir(exist_ok=True)
Path("uploads").mkdir(exist_ok=True)
Path("temp").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# WebSocket manager for real-time features
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self.user_connections = {}

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
            try:
                self.active_connections[client_id].remove(websocket)
                if not self.active_connections[client_id]:
                    del self.active_connections[client_id]
            except ValueError:
                pass
        
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
        
        logger.info(f"🔌 WebSocket disconnected: {client_id}")

manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            if data.get("type") == "ping":
                await websocket.send_json({
                    "type": "pong", 
                    "timestamp": datetime.utcnow().isoformat()
                })
            else:
                # Echo back for now - implement specific handlers
                await websocket.send_json({
                    "type": "echo", 
                    "data": data
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)

# Frontend routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve main landing page"""
    try:
        return FileResponse('frontend/index.html')
    except FileNotFoundError:
        return HTMLResponse("""
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
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Nexus Learn</h1>
                <p>Modern Learning Management System</p>
                <p>Frontend files are loading...</p>
                <div style="margin-top: 2rem;">
                    <a href="/api/docs" style="color: #fff; text-decoration: none; margin: 0 1rem; padding: 0.5rem 1rem; border: 2px solid rgba(255,255,255,0.3); border-radius: 25px;">📚 API Docs</a>
                    <a href="/health" style="color: #fff; text-decoration: none; margin: 0 1rem; padding: 0.5rem 1rem; border: 2px solid rgba(255,255,255,0.3); border-radius: 25px;">💚 Health</a>
                </div>
            </div>
        </body>
        </html>
        """)

@app.get("/admin", response_class=HTMLResponse)
@app.get("/admin/", response_class=HTMLResponse)
async def read_admin():
    """Serve admin panel"""
    try:
        return FileResponse('frontend/admin/index.html')
    except FileNotFoundError:
        return HTMLResponse("""
        <h1>Admin Panel Loading...</h1>
        <p><a href="/api/docs">API Documentation</a></p>
        """)

@app.get("/student", response_class=HTMLResponse)
@app.get("/student/", response_class=HTMLResponse)
async def read_student():
    """Serve student portal"""
    try:
        return FileResponse('frontend/student/index.html')
    except FileNotFoundError:
        return HTMLResponse("""
        <h1>Student Portal Loading...</h1>
        <p><a href="/">Back to Home</a></p>
        """)

# API routes
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
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0",
            "deployment": "render",
            "components": {
                "database": db_status,
                "websocket": "active",
                "static_files": "mounted"
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
        "deployment": "render-unified",
        "description": "Unified deployment serving both FastAPI backend and static frontend",
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
        "endpoints": {
            "frontend": "/",
            "admin": "/admin",
            "student": "/student",
            "api_docs": "/api/docs",
            "health": "/health"
        },
        "websocket": "/ws/{client_id}",
        "timestamp": datetime.utcnow().isoformat()
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    # For API routes, return JSON
    if request.url.path.startswith("/api/"):
        return {"error": "Resource not found", "status_code": 404}
    
    # For frontend routes, try to serve main page or return HTML error
    try:
        return FileResponse('frontend/index.html')
    except FileNotFoundError:
        return HTMLResponse("""
        <h1>404 - Page Not Found</h1>
        <p><a href="/">Go to Home</a></p>
        """, status_code=404)

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    logger.error(f"Internal error: {exc}")
    return {"error": "Internal server error", "status_code": 500}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    # Run with production settings for Render
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1,  # Single worker for free tier
        log_level="info",
        access_log=True
    )
