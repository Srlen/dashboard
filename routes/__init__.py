import os
from typing import List
from quart import Quart
from dotenv import load_dotenv
from routes.auth import auth
from routes.guilds import guilds
from routes.user import user