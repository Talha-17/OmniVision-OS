
import ollama

class VisionAgent:
    def __init__(self, model_name: str = "llava"):
        self.model_name = model_name

    def analyze_screen(self, image_b64: str, prompt: str) -> str:
        """Analyzes a base64 encoded image frame using local Ollama model."""
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                images=[image_b64]
            )
            return response.get('response', '')
        except Exception as e:
            return f"Error executing vision model: {str(e)}"