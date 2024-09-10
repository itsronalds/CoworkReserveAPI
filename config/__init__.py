import os

CONFIG = {
    'DATABASE_URI': os.getenv('DATABASE_URI'),
    'TOKEN_SECRET': os.getenv('TOKEN_SECRET'),
}
