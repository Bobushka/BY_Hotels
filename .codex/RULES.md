# Codex Operating Rules

## Core Principles
1. Always follow these rules exactly.  
2. Be brief, precise, and task-focused.  
3. Choose one correct approach — do not list alternatives.  
4. Confirm the **goal and architecture first**, then provide code.  
5. Always specify **user, host, and port** for any command.  
6. Never use placeholders (like `<user>` or `<path>`).  
7. Use only verified and previously confirmed code.  
8. If unsure — say **“don’t know”**, not assumptions.  
9. Proceed **step by step**, waiting for explicit “OK / next”.  
10. Do not propose tests, refactors, or extra features unless requested.  
11. If code requires assumptions, explicitly confirm each assumption with the user before coding.  
12. Every function must include a PEP 8–style docstring, e.g.:
    """
    Brief one-line summary.

    Args:
        param_name: Explanation.

    Returns:
        Description of return value.
    """
13. Avoid OOP — пишем только функции; допускаются `@dataclass`, если иначе нельзя.
14. Каждый логический блок кода сопровождай развёрнутым комментарием на русском языке.
15. Если что-то непонятно — спрашивай, прежде чем делать.
16. Перед тем как отчитываться — проверяй соответствует ли результат заданию.

## Communication Rules
- Answer in simple, direct English (or Russian if the user switches).  
- Never explain obvious things unless asked.  
- Do not add commentary or stylistic improvements.  
- Always follow the current working context (SGB, SLLM, M64, etc.).  
- If a task requires coding — provide the **full code**, no omissions.

## Technical Scope
- Environment: macOS / Apple Silicon (M4, M1, etc.)  
- Stack: Python 3.12, FastAPI, Uvicorn, Jinja2, Nginx, Ollama, Brew, launchd.  
- Primary repositories: `SGB`, `devSGB`, `SGB-prod`.  
- Architecture:  
  - `SLLM` = LLM node (Ollama)  
  - `SGB` = backend (FastAPI + RAG)  
  - `M64` = production host (Nginx/SSL)  

## Workflow
- Discuss → Confirm → Implement → Test → Approve.  
- Never skip the confirm step.  
- Never change UI, prompts, or file structure without approval.
