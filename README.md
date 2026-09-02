# Autonomous Refactoring Agent

An autonomous, self-healing system that ingests repositories, proposes AST-aware changes, tests them in a sandbox, and streams the process to a user for final PR approval.

## Structure
- `/backend`: FastAPI Python application with agentic workflows.
- `/frontend`: React + TypeScript frontend with Monaco Diff Editor.

## Setup
1. Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ./start.sh
   ```
2. Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
