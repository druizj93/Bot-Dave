import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv

load_dotenv()

class AIRouter:
    def __init__(self):
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        self.mistral_key = os.getenv('MISTRAL_API_KEY')
        # self.openai_key = os.getenv('OPENAI_API_KEY')  # Preparado para futuro
    
    def choose_model(self, query):
        """Router inteligente: elige modelo basado en query."""
        # Lógica simple para demo: alternar o basado en keywords
        if 'trade' in query.lower() or 'precio' in query.lower():
            return 'gemini'  # Bueno para análisis
        elif 'video' in query.lower() or 'youtube' in query.lower():
            return 'mistral'
        else:
            return 'deepseek'  # Default
    
    def generate_response(self, prompt, model='gemini', memory=[]):
        """Genera respuesta usando el modelo elegido."""
        full_prompt = "\n".join([f"Hist: {m[0]} -> {m[1]}" for m in memory]) + "\nUser: " + prompt
        
        if model == 'gemini':
            genai.configure(api_key=self.gemini_key)
            model_g = genai.GenerativeModel('gemini-1.5-flash')
            response = model_g.generate_content(full_prompt)
            return response.text
        elif model == 'deepseek':
            # Implementar llamada a API DeepSeek
            # Ejemplo placeholder
            return f"Respuesta de DeepSeek para: {prompt[:50]}..."
        # Añadir más
        return "Respuesta placeholder"