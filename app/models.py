from pydantic import BaseModel
from typing import Dict, Any, Optional

class CreateGraphRequest(BaseModel):
    graph_id: str
    example: Optional[str] = None

class RunGraphRequest(BaseModel):
    graph_id: str
    run_id: str
    initial_state: Dict[str, Any]

class RunStateResponse(BaseModel):
    run_id: str
    status: str
    state: Dict[str, Any]
    log: list
