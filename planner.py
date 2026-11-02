
import json
import ollama

def plan_multi_step_task(goal: str):
    """Breaks down a complex user goal into a sequence of atomic actions."""
    prompt = f"""
    You are an AI desktop agent task planner.
    Break down the following user goal into a sequence of steps: "{goal}"
    
    Allowed action types: "click", "type".
    
    Respond ONLY with a valid JSON array of objects with no extra text or markdown formatting. 
    Example format:
    [
      {{"step": 1, "description": "Click search icon", "action_type": "click"}},
      {{"step": 2, "description": "Type text", "action_type": "type", "text": "Notepad"}}
    ]
    """
    
    response = ollama.chat(
        model='llava',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    content = response['message']['content'].strip()
    clean_json = content.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(clean_json)
    except Exception:
        return [{"step": 1, "description": goal, "action_type": "click"}]