"""
FastAPI application entry point
"""
from fastapi import FastAPI
from app.api.routes import router
from app.config import HOST, PORT
from app.logging_config import logger
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="PKI-Based 2FA Microservice",
    description="Secure 2FA microservice using RSA encryption and TOTP",
    version="1.0.0"
)

# Include API routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting PKI-Based 2FA Microservice")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down PKI-Based 2FA Microservice")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        log_level="info"
    )
