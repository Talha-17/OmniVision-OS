from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from actions import click_at_coordinate, type_text
from screen import analyze_screen_with_llava
from planner import plan_multi_step_task

app = FastAPI(title="OmniVision OS")

# Enable CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ActionRequest(BaseModel):
    action_type: str
    x: int | None = None
    y: int | None = None
    text: str | None = None

class PromptRequest(BaseModel):
    prompt: str = "Analyze this screen and describe what you see."

class AutonomousRequest(BaseModel):
    goal: str

@app.get("/")
def read_root():
    return {"status": "OmniVision OS active with LLaVA vision"}

@app.post("/analyze-screen")
def analyze_screen(request: PromptRequest):
    analysis = analyze_screen_with_llava(request.prompt)
    return {"status": "success", "analysis": analysis}

@app.post("/execute-action")
def execute_action(request: ActionRequest):
    if request.action_type == "click" and request.x is not None and request.y is not None:
        return click_at_coordinate(request.x, request.y)
    elif request.action_type == "type" and request.text:
        return type_text(request.text)
    return {"status": "error", "message": "Invalid action parameters"}

@app.post("/autonomous-task")
def run_autonomous_task(request: AutonomousRequest):
    prompt = f"""
    You are a desktop automation agent. Look at the screen. 
    Find the UI element related to this goal: "{request.goal}".
    Estimate the approximate screen (x, y) pixel coordinates of the center of this element.
    Respond ONLY with a JSON object in this exact format, with no extra text:
    {{"x": 100, "y": 200, "description": "found target"}}
    """
    analysis = analyze_screen_with_llava(prompt)
    try:
        import json
        clean_json = analysis.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        if "x" in data and "y" in data:
            click_at_coordinate(data["x"], data["y"])
            return {"status": "success", "target_found": data, "raw_response": analysis}
    except Exception as e:
        return {"status": "partial_success", "message": "Could not auto-parse coordinates", "raw_response": analysis, "error": str(e)}
    return {"status": "error", "raw_response": analysis}

@app.post("/run-workflow")
def run_workflow(request: AutonomousRequest):
    steps = plan_multi_step_task(request.goal)
    results = []
    
    for step in steps:
        if step.get("action_type") == "click":
            sub_res = run_autonomous_task(AutonomousRequest(goal=step["description"]))
            results.append({"step": step, "result": sub_res})
        elif step.get("action_type") == "type" and "text" in step:
            sub_res = type_text(step["text"])
            results.append({"step": step, "result": sub_res})
        time.sleep(1)
        
    return {"status": "workflow_completed", "executed_steps": results}