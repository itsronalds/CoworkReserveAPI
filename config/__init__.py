import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'DATABASE_URI': os.getenv('DATABASE_URI'),
    'TOKEN_SECRET': os.getenv('TOKEN_SECRET'),
}
