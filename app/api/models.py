"""API request and response models using Pydantic"""
from pydantic import BaseModel
from datetime import datetime

# Request models
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class VerifyTOTPRequest(BaseModel):
    code: str

# Response models
class DecryptSeedResponse(BaseModel):
    status: str

class GenerateTOTPResponse(BaseModel):
    code: str
    valid_for: int

class VerifyTOTPResponse(BaseModel):
    valid: bool

class HealthResponse(BaseModel):
    status: str
    timestamp: str

class ErrorResponse(BaseModel):
    detail: str
