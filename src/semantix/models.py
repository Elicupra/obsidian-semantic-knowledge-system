import os
from abc import ABC, abstractmethod
from typing import Optional
from semantix.config import (
    get_api_key as config_get_api_key,
    get_default_provider as config_get_default,
    PROVIDER_INFO,
)


class ModelProvider(ABC):
    def __init__(self, model_type: str = "auto"):
        self.model_type = model_type
    
    @abstractmethod
    def generate(self, prompt: str, context: str) -> str:
        pass


class GroqProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__("groq")
        self.api_key = api_key or config_get_api_key("groq")
        self.model = model or PROVIDER_INFO["groq"]["default_model"]
    
    def generate(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY no configurada. Ejecuta: semantix config set groq")
        
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


class OpenRouterProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__("openrouter")
        self.api_key = api_key or config_get_api_key("openrouter")
        self.model = model or PROVIDER_INFO["openrouter"]["default_model"]
    
    def generate(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY no configurada. Ejecuta: semantix config set openrouter")
        
        try:
            import requests
        except ImportError:
            raise ImportError("requests package not installed.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": f"{prompt}\n\nContexto:\n{context}"}],
            "temperature": 0.7,
            "max_tokens": 4000,
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"OpenRouter API error: {response.status_code} - {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


class OpenAIProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__("openai")
        self.api_key = api_key or config_get_api_key("openai")
        self.model = model or PROVIDER_INFO["openai"]["default_model"]
    
    def generate(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no configurada. Ejecuta: semantix config set openai")
        
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        client = OpenAI(api_key=self.api_key)
        
        full_prompt = f"{prompt}\n\nContexto:\n{context}"
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.7,
            max_tokens=4000,
        )
        
        return response.choices[0].message.content


class GeminiProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__("google")
        self.api_key = api_key or config_get_api_key("google")
        self.model = model or PROVIDER_INFO["google"]["default_model"]
    
    def generate(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no configurada. Ejecuta: semantix config set google")
        
        try:
            import requests
        except ImportError:
            raise ImportError("requests package not installed.")
        
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{prompt}\n\nContexto:\n{context}"}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4000,
            }
        }
        
        url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        
        if response.status_code != 200:
            raise RuntimeError(f"Gemini API error: {response.status_code} - {response.text}")
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]


class ClaudeProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__("claude")
        self.api_key = api_key or config_get_api_key("claude")
        self.model = model or PROVIDER_INFO["claude"]["default_model"]
    
    def generate(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY no configurada. Ejecuta: semantix config set claude")
        
        try:
            import requests
        except ImportError:
            raise ImportError("requests package not installed.")
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": f"{prompt}\n\nContexto:\n{context}"}],
            "temperature": 0.7,
            "max_tokens": 4000,
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=120,
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Claude API error: {response.status_code} - {response.text}")
        
        result = response.json()
        return result["content"][0]["text"]


class LocalProvider(ModelProvider):
    def __init__(self, model_name: str = "llama3", base_url: Optional[str] = None):
        super().__init__("local")
        self.model_name = model_name
        self.base_url = base_url or "http://localhost:11434"
    
    def generate(self, prompt: str, context: str) -> str:
        try:
            import requests
        except ImportError:
            raise ImportError("requests package not installed.")
        
        payload = {
            "model": self.model_name,
            "prompt": f"{prompt}\n\nContexto:\n{context}",
            "stream": False,
        }
        
        response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=300)
        
        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.status_code} - {response.text}")
        
        result = response.json()
        return result.get("response", "")


PROVIDERS = {
    "groq": GroqProvider,
    "openrouter": OpenRouterProvider,
    "openai": OpenAIProvider,
    "google": GeminiProvider,
    "claude": ClaudeProvider,
    "local": LocalProvider,
}


def get_provider(model_type: str = "auto") -> ModelProvider:
    if model_type == "auto":
        model_type = config_get_default()
    
    provider_class = PROVIDERS.get(model_type, LocalProvider)
    return provider_class()


def list_providers():
    return list(PROVIDERS.keys())