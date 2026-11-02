
import os
import pyautogui
import ollama

def capture_screen():
    """Takes a screenshot of the primary monitor and saves it to disk."""
    img_path = "temp_screen.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(img_path)
    return img_path

def analyze_screen_with_llava(prompt: str):
    """Sends the screenshot and screen dimensions to the local LLaVA model."""
    img_path = capture_screen()
    width, height = pyautogui.size()
    
    enhanced_prompt = f"""
    The screen resolution is {width} pixels wide by {height} pixels high.
    {prompt}
    """
    
    try:
        response = ollama.chat(
            model='llava',
            messages=[
                {
                    'role': 'user',
                    'content': enhanced_prompt,
                    'images': [img_path]
                }
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error analyzing screen: {str(e)}"
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)