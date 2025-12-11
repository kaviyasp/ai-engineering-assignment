from fastapi import FastAPI, HTTPException, BackgroundTasks
from .engine import GraphEngine
from . import tools as tools_module
from .workflows import make_nodes_and_edges
from .models import CreateGraphRequest, RunGraphRequest
import asyncio

app = FastAPI(title="Mini Workflow Engine")

engine = GraphEngine()

engine.register_tool("extract_functions", tools_module.extract_functions)
engine.register_tool("check_complexity", tools_module.check_complexity)
engine.register_tool("detect_issues", tools_module.detect_issues)
engine.register_tool("suggest_improvements", tools_module.suggest_improvements)

@app.post("/graph/create")
def create_graph(req: CreateGraphRequest):
    if req.example == "code_review_option_a":
        nodes, edges, start = make_nodes_and_edges()
        engine.create_graph(req.graph_id, nodes, edges, start)
        return {"graph_id": req.graph_id}
    else:
        raise HTTPException(status_code=400, detail="only example 'code_review_option_a' supported in this repo")

@app.post("/graph/run")
async def run_graph(req: RunGraphRequest, background_tasks: BackgroundTasks):
    if req.graph_id not in engine.graphs:
        raise HTTPException(status_code=404, detail="graph not found")
    run_id = req.run_id
    async def _runner():
        await engine.run_graph(req.graph_id, req.initial_state, run_id)
    background_tasks.add_task(asyncio.create_task, _runner())
    return {"run_id": run_id, "status": "started"}

@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    run = engine.runs.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    return {"run_id": run_id, "status": run.get("status"), "state": run.get("state"), "log": run.get("log")}
