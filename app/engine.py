from typing import Callable, Dict, Any, List, Optional
import asyncio

RunStore = Dict[str, Dict[str, Any]]

class GraphEngine:
    def __init__(self):
        self.graphs: Dict[str, Dict[str, Any]] = {}
        self.tools: Dict[str, Callable] = {}
        self.runs: RunStore = {}

    def register_tool(self, name: str, fn: Callable):
        self.tools[name] = fn

    def create_graph(self, graph_id: str, nodes: Dict[str, Callable], edges: Dict[str, str], start_node: str):
        self.graphs[graph_id] = {"nodes": nodes, "edges": edges, "start": start_node}
        return graph_id

    async def _run_node(self, node_fn: Callable, state: Dict[str, Any]):
        if asyncio.iscoroutinefunction(node_fn):
            return await node_fn(state, self.tools)
        else:
            return node_fn(state, self.tools)

    async def run_graph(self, graph_id: str, initial_state: Dict[str, Any], run_id: str, loop_limit: int = 50):
        if graph_id not in self.graphs:
            raise ValueError("unknown graph_id")
        graph = self.graphs[graph_id]
        nodes = graph["nodes"]
        edges = graph["edges"]
        current = graph["start"]
        state = dict(initial_state)
        log: List[str] = []
        self.runs[run_id] = {"state": state, "log": log, "status": "running"}

        loop_counter = 0
        while current is not None:
            loop_counter += 1
            if loop_counter > loop_limit:
                log.append("Loop limit reached, stopping.")
                break

            node_fn = nodes.get(current)
            if node_fn is None:
                log.append(f"Node `{current}` not found. Stopping.")
                break

            log.append(f"Running node: {current}")
            try:
                result = await self._run_node(node_fn, state)
            except Exception as e:
                log.append(f"Node `{current}` raised error: {e}")
                self.runs[run_id]["status"] = "failed"
                break

            next_node: Optional[str] = None
            if isinstance(result, dict) and "_next" in result:
                next_node = result["_next"]
            else:
                edge_val = edges.get(current)
                if isinstance(edge_val, str):
                    next_node = edge_val
                elif callable(edge_val):
                    try:
                        next_node = edge_val(state)
                    except Exception as e:
                        log.append(f"Routing function for `{current}` raised {e}")
                        next_node = None
                else:
                    next_node = None

            self.runs[run_id]["state"] = state
            self.runs[run_id]["log"] = log.copy()

            if next_node is None:
                log.append("No next node. Stopping.")
                break
            current = next_node

        self.runs[run_id]["status"] = "finished"
        self.runs[run_id]["state"] = state
        self.runs[run_id]["log"] = log
        return {"final_state": state, "log": log}
