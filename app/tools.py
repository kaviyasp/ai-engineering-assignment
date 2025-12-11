from typing import Dict, Any
import re

def extract_functions(code: str) -> Dict[str, Any]:
    funcs = re.findall(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    return {"functions": funcs, "function_count": len(funcs)}

def check_complexity(state: Dict[str, Any]) -> Dict[str, Any]:
    count = state.get("functions", [])
    if isinstance(count, list):
        score = max(0, 100 - (len(count) * 10))
    else:
        score = state.get("function_count", 50)
    return {"complexity_score": score}

def detect_issues(code: str) -> Dict[str, Any]:
    issues = []
    if "print(" in code:
        issues.append("uses-print")
    if len(code.splitlines()) > 200:
        issues.append("very-long-file")
    return {"issues": issues, "issue_count": len(issues)}

def suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    suggestions = []
    if state.get("complexity_score", 0) < 50:
        suggestions.append("refactor_functions")
    if state.get("issue_count", 0) > 0:
        suggestions.append("fix_basic_issues")
    quality_score = min(100, state.get("complexity_score", 0) + max(0, 20 - state.get("issue_count", 0)*5))
    return {"suggestions": suggestions, "quality_score": quality_score}
