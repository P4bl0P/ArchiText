import requests

class AIEngine:
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.url = "http://127.0.0.1:11434/api/generate"

    def generate_readme(self, structure: str, context: str, lang: str = "auto") -> str:
       # Definimos la orden de idioma de forma muy clara
        if lang == "es":
            target_lang = "Escribe el README exclusivamente en ESPAÑOL."
        elif lang == "en":
            target_lang = "Write the README exclusively in ENGLISH."
        else:
            target_lang = "Detect the language of the code and comments and respond in that language."

        prompt = f"""### ROLE
Act as a Senior Full-Stack Developer and Professional Technical Writer.
Your goal is to create a modern, clean, and aesthetic README.md for GitHub.

### PROJECT CONTEXT
STRUCTURE:
{structure}

KEY FILES CONTENT:
{context}

### INSTRUCTIONS & STYLE
1. Style: Professional, concise, and modern (Vercel/Supabase style).
2. Layout: Use clear headings, badges, and well-formatted code blocks.
3. Sections required:
   - Project Title with a tagline.
   - Professional Description (purpose and target audience).
   - Features (list).
   - Tech Stack (use badges or icons).
   - Step-by-step Installation and Usage.
   - Project Structure (tree view).
   - Roadmap, Contributing, and License.
4. {target_lang}

### OUTPUT RULES
- Output ONLY the Markdown content.
- Do not include any intro like "Here is your readme".
- Do not use generic filler text.

FINAL COMMAND: Generate the professional README.md now."""
        try:
            response = requests.post(
                self.url, 
                json={
                    "model": self.model, 
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": 4096,
                        "temperature": 0.3
                    }
                  },
                timeout=300
            )
            
            if response.status_code != 200:
                return f"Error de Ollama: {response.status_code} - {response.text}"
            
            data = response.json()
            # Si 'response' no está, probamos con 'message' (a veces cambia según la versión)
            return data.get("response") or data.get("message", {}).get("content") or "⚠️ No hay respuesta de la IA"
            
        except Exception as e:
            return f"Error crítico: {str(e)}"