
import pyautogui

# Safety fail-safe: move mouse to upper-left corner to abort actions if needed
pyautogui.FAILSAFE = True

def click_at_coordinate(x: int, y: int):
    """Executes a mouse click at specific screen coordinates."""
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()
    return {"status": "success", "action": "click", "target": [x, y]}

def type_text(text: str):
    """Types out a given text string."""
    pyautogui.write(text, interval=0.05)
    return {"status": "success", "action": "type", "text": text}