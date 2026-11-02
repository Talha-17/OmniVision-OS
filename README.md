
# OmniVision OS 👁️🤖

OmniVision OS is an offline, private, autonomous desktop agent powered by local computer vision and automated control. Built with FastAPI, Ollama (LLaVA), and PyAutoGUI, it interprets user goals, analyzes desktop screen states, determines precise coordinate interactions, and executes multi-step workflows entirely locally.

---

## Key Features
1. 100% Offline & Private: Runs entirely on local hardware with zero data leaving your machine.
2. Vision-Language Understanding: Integrates local multi-modal vision models (LLaVA) to inspect screen captures and locate UI targets.
3. Resolution-Aware Mapping: Dynamically scales target coordinates to match primary display resolutions.
4. Autonomous Task Planner: Deconstructs complex high-level natural language goals into sequential execution steps.
5. Desktop Automation: Automates keyboard and mouse actions using PyAutoGUI.
6. Web Dashboard: Includes a lightweight local frontend interface to issue commands and view real-time API logs.

---

## Project Structure
text
OmniVision-OS/
│
├── main.py          # FastAPI backend server with CORS & workflow endpoints
├── planner.py       # LLM-based multi-step task decomposition engine
├── screen.py        # Desktop screen capture and resolution-aware LLaVA parser
├── actions.py       # PyAutoGUI keyboard and mouse execution handlers
└── index.html       # Local web dashboard UI