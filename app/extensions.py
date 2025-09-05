from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
from flask_smorest import Api
from flask_talisman import Talisman

# Core

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
cache = Cache()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
csrf = CSRFProtect()
smorest_api = Api()
socketio = SocketIO(async_mode="eventlet")
talisman = Talisman()
