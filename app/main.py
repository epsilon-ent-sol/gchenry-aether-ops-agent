"""
FastAPI Application Entrypoint for Cloud Run
"""
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from app.config import settings
from app.auth import verify_agent_identity
from app.agent import run_agent_turn
from app.memory import session_store

app = FastAPI(
    title="Aether Ops Agent Service",
    version="2.0.0",
    description="Autonomous Multi-Agent Security & Release Gate for Google Cloud"
)

class AgentRequest(BaseModel):
    prompt: str
    session_id: str = "default-session"

class AgentResponse(BaseModel):
    response: str
    session_id: str
    actor_spiffe_id: str
    status: str

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": "aether-ops-agent",
        "environment": settings.ENVIRONMENT,
        "model": settings.GEMINI_MODEL
    }

@app.post("/api/v1/agent/invoke", response_model=AgentResponse)
def invoke_agent(
    req: AgentRequest,
    auth_ctx: dict = Depends(verify_agent_identity)
):
    actor_id = auth_ctx.get("spiffe_id", auth_ctx.get("sub", "anonymous"))
    
    # Save user message to decoupled store
    session_store.append_message(req.session_id, "user", req.prompt)

    # Run agent loop
    agent_output = run_agent_turn(req.prompt, actor_id=actor_id, session_id=req.session_id)

    # Save assistant response to decoupled store
    session_store.append_message(req.session_id, "assistant", agent_output)

    return AgentResponse(
        response=agent_output,
        session_id=req.session_id,
        actor_spiffe_id=actor_id,
        status="SUCCESS"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)

