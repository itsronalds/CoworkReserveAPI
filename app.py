from fastapi import FastAPI

# routes
from routes.auth import router as auth_router
from routes.coworking import router as coworking_router

app = FastAPI()

# include routes
app.include_router(auth_router)
app.include_router(coworking_router)
