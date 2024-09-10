from fastapi import FastAPI

# routes
from routes.auth import router as auth_router

app = FastAPI()

# include routes
app.include_router(auth_router)
