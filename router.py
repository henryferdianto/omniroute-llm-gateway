"""Optional FastAPI wrapper around the routing core.

Run: pip install fastapi uvicorn && uvicorn router:app --reload
"""
from src.router_core import AllProvidersFailed, route

try:
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI(title="OmniRoute LLM Gateway")

    class Request(BaseModel):
        prompt: str
        complexity: str = "medium"

    @app.post("/route")
    def handle(req: Request):
        try:
            return route(req.prompt, req.complexity)
        except AllProvidersFailed as exc:
            return {"error": "all providers failed", "details": exc.args[0]}

except ImportError:  # FastAPI not installed: CLI usage only
    app = None
