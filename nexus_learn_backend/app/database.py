"""
Modern MongoDB database layer with real-time sync capabilities
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

import motor.motor_asyncio
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from bson import ObjectId

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class DatabaseError(Exception):
    """Custom database exception"""
    pass


class Database:
    """Modern MongoDB database management with advanced features"""
    
    def __init__(self):
        self.client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
        self.db: Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Establish database connection with optimization"""
        try:
            # Create client with optimized settings
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                settings.MONGODB_URL,
                maxPoolSize=100,
                minPoolSize=10,
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=30000,
                retryWrites=True,
                retryReads=True
            )
            
            # Get database
            self.db = self.client[settings.DATABASE_NAME]
            
            # Test connection
            await self.client.admin.command('ismaster')
            
            # Create indexes
            await self._create_indexes()
            
            self._connected = True
            logger.info(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise DatabaseError(f"Database connection failed: {e}")
    
    async def disconnect(self) -> None:
        """Close database connection"""
        if self.client:
            self.client.close()
            self._connected = False
            logger.info("🔄 Disconnected from MongoDB")
    
    async def ping(self) -> bool:
        """Health check for database connection"""
        try:
            await self.client.admin.command('ping')
            return True
        except:
            return False
    
    @property
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self._connected and self.client is not None
    
    async def _create_indexes(self) -> None:
        """Create optimized indexes for performance"""
        try:
            # Users collection indexes
            if "users" not in await self.db.list_collection_names():
                await self.db.create_collection("users")
                
            await self.db.users.create_indexes([
                IndexModel([("email", ASCENDING)], unique=True),
                IndexModel([("username", ASCENDING)], unique=True),
                IndexModel([("telegram_id", ASCENDING)], unique=True, sparse=True),
                IndexModel([("role", ASCENDING)]),
                IndexModel([("active", ASCENDING)]),
                IndexModel([("created_at", DESCENDING)])
            ])
            
            logger.info("✅ Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"❌ Error creating indexes: {e}")
            raise
    
    # User operations
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user with validation"""
        try:
            user_data["created_at"] = datetime.utcnow()
            user_data["updated_at"] = datetime.utcnow()
            user_data["active"] = True
            
            result = await self.db.users.insert_one(user_data)
            user_data["_id"] = result.inserted_id
            
            logger.info(f"✅ User created: {user_data.get('email')}")
            return user_data
            
        except DuplicateKeyError:
            raise DatabaseError("User with this email or username already exists")
        except Exception as e:
            logger.error(f"❌ Error creating user: {e}")
            raise DatabaseError(f"Failed to create user: {e}")
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            user = await self.db.users.find_one({"_id": ObjectId(user_id)})
            return user
        except Exception as e:
            logger.error(f"❌ Error getting user: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            user = await self.db.users.find_one({"email": email})
            return user
        except Exception as e:
            logger.error(f"❌ Error getting user by email: {e}")
            return None
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user by Telegram ID"""
        try:
            user = await self.db.users.find_one({"telegram_id": telegram_id})
            return user
        except Exception as e:
            logger.error(f"❌ Error getting user by telegram ID: {e}")
            return None
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {}
            
            # Count documents
            stats["users"] = await self.db.users.count_documents({"active": True})
            
            return stats
        except Exception as e:
            logger.error(f"❌ Error getting stats: {e}")
            return {}