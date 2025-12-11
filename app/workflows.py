from typing import Dict, Any
from . import tools

def node_extract(state: Dict[str, Any], registry) -> Dict[str, Any]:
    code = state.get("code", "")
    res = registry['extract_functions'](code)
    state.update(res)
    return state

def node_check_complexity(state: Dict[str, Any], registry):
    res = registry['check_complexity'](state)
    state.update(res)
    return state

def node_detect_issues(state: Dict[str, Any], registry):
    code = state.get("code", "")
    res = registry['detect_issues'](code)
    state.update(res)
    return state

def node_suggest(state: Dict[str, Any], registry):
    res = registry['suggest_improvements'](state)
    state.update(res)
    return state

def route_suggest_to_extract(state):
    threshold = state.get("threshold", 70)
    if state.get("quality_score", 0) < threshold:
        return "extract"
    return None

def make_nodes_and_edges():
    nodes = {
        "extract": node_extract,
        "check_complexity": node_check_complexity,
        "detect_issues": node_detect_issues,
        "suggest": node_suggest,
    }
    edges = {
        "extract": "check_complexity",
        "check_complexity": "detect_issues",
        "detect_issues": "suggest",
        "suggest": route_suggest_to_extract,
    }
    start = "extract"
    return nodes, edges, start
