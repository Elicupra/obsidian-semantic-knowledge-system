import os
from abc import ABC, abstractmethod
from typing import Optional


class ModelProvider(ABC):
    def __init__(self, model_type: str = "auto"):
        self.model_type = model_type
    
    @abstractmethod
    def generate(self, prompt: str, context: str) -> str:
        pass


class GroqProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("groq")
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = "llama-3.3-70b-versatile"
    
    def generate(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY no configurada")
        
        try:
            from groq import Groq
        except ImportError:
            raise ImportError("groq package not installed. Run: pip install groq")
        
        client = Groq(api_key=self.api_key)
        
        full_prompt = f"{prompt}\n\nContexto:\n{context}"
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.7,
            max_tokens=4000,
        )
        
        return response.choices[0].message.content


class GeminiProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("gemini")
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
    
    def generate(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no configurada")
        return f"[Gemini] {prompt[:50]}..."


class ClaudeProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("claude")
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
    
    def generate(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY no configurada")
        return f"[Claude] {prompt[:50]}..."


class LocalProvider(ModelProvider):
    def __init__(self, model_name: str = "llama3"):
        super().__init__("local")
        self.model_name = model_name
    
    def generate(self, prompt: str, context: str) -> str:
        return f"[Local:{self.model_name}] {prompt[:50]}..."


def get_provider(model_type: str = "auto") -> ModelProvider:
    if model_type == "auto":
        if os.getenv("GROQ_API_KEY"):
            return GroqProvider()
        elif os.getenv("GEMINI_API_KEY"):
            return GeminiProvider()
        elif os.getenv("CLAUDE_API_KEY"):
            return ClaudeProvider()
        else:
            return LocalProvider()
    
    providers = {
        "groq": GroqProvider,
        "gemini": GeminiProvider,
        "claude": ClaudeProvider,
        "local": LocalProvider,
    }
    
    provider_class = providers.get(model_type, LocalProvider)
    return provider_class()
