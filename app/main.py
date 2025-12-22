from fastapi import FastAPI
from app.api.v1 import groups, participants, draws
from app.core.config import settings

is_docs_enabled = "/docs" if settings.enable_docs else None

app = FastAPI(
    title="Secretly API",
    docs_url=is_docs_enabled,
    redoc_url=None,
    description="API simples para gerenciamento de amigo secreto",
    version="1.0.0"
)

app.include_router(groups.router, prefix="/api/v1/groups", tags=["grupos"])
app.include_router(participants.router, prefix="/api/v1/participants", tags=["participantes"])
app.include_router(draws.router, prefix="/api/v1/draws", tags=["sorteios"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Secretly API - API simples para amigo secreto!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}