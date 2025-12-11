Mini Workflow Engine - AI Engineering Assignment

Overview
--------
This repository contains a Mini Workflow/Graph Engine implemented in Python using FastAPI.
The engine supports defining nodes as Python functions, linking them with edges, conditional
routing, and executing runs that mutate a shared state dictionary.

This submission implements the example workflow "Code Review Mini-Agent" (Option A).

Contents
--------
- app/engine.py         : Core graph engine and run management
- app/tools.py          : Utility functions used by nodes
- app/workflows.py      : Example workflow definition and routing
- app/main.py           : FastAPI application and endpoints
- app/models.py         : Pydantic request/response models
- app/utils.py          : Small helper utilities
- requirements.txt
- .gitignore

Example Workflow Description
----------------------------
Input: Python source code and a quality threshold.

Nodes:
1. extract - extracts function names and counts from source code.
2. check_complexity - computes a naive complexity score.
3. detect_issues - detects simple issues like use of print statements or very long files.
4. suggest - provides improvement suggestions and computes a quality score.

Routing: The workflow repeats (loops back to extract) while the quality_score is below the provided threshold.

Running Locally
---------------
1. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate      (Windows: venv\Scripts\activate)

2. Install dependencies:
   pip install -r requirements.txt

3. Start the FastAPI server:
   uvicorn app.main:app --reload --port 8000

4. Open the interactive API documentation:
   http://127.0.0.1:8000/docs

API Endpoints
-------------
- POST /graph/create
  Request body:
  {
    "graph_id": "g1",
    "example": "code_review_option_a"
  }

- POST /graph/run
  Request body:
  {
    "graph_id": "g1",
    "run_id": "r1",
    "initial_state": {
      "code": "def foo():\n    print(1)",
      "threshold": 70
    }
  }

- GET /graph/state/{run_id}

Git - Create Repository and Push
--------------------------------
git init
git add .
git commit -m "Initial submission: mini workflow engine"
Create a repository on GitHub, then:
git remote add origin <repo-url>
git branch -M main
git push -u origin main

Notes and Next Steps
--------------------
The engine is intentionally simple and uses in-memory storage. Suggested improvements:
- Persist graphs and runs to a database
- Add authentication on API endpoints
- Provide upload support for workflow modules
- Add unit tests and CI pipeline
