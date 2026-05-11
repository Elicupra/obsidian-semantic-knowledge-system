import os
import json
import keyring
from pathlib import Path
from typing import Optional, Dict, List
from dotenv import load_dotenv

CONFIG_DIR = Path.home() / ".semantix"
CONFIG_FILE = CONFIG_DIR / "config.json"
SERVICE_NAME = "semantix"

PROVIDER_INFO = {
    "groq": {
        "name": "Groq",
        "env_key": "GROQ_API_KEY",
        "description": "GPU accelerators for AI inference",
        "default_model": "llama-3.3-70b-versatile",
    },
    "openrouter": {
        "name": "OpenRouter",
        "env_key": "OPENROUTER_API_KEY",
        "description": "Unified API for 200+ LLMs",
        "default_model": "anthropic/claude-3.5-sonnet",
    },
    "openai": {
        "name": "OpenAI",
        "env_key": "OPENAI_API_KEY",
        "description": "GPT-4, GPT-4o models",
        "default_model": "gpt-4o",
    },
    "google": {
        "name": "Google Gemini",
        "env_key": "GEMINI_API_KEY",
        "description": "Google Gemini models",
        "default_model": "gemini-1.5-pro",
    },
    "claude": {
        "name": "Anthropic Claude",
        "env_key": "CLAUDE_API_KEY",
        "description": "Claude 3.5 Sonnet",
        "default_model": "claude-3-5-sonnet-20241022",
    },
    "local": {
        "name": "Local (Ollama)",
        "env_key": None,
        "description": "Local models via Ollama",
        "default_model": "llama3",
    },
}

AVAILABLE_PROVIDERS = list(PROVIDER_INFO.keys())


def _ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _load_config() -> Dict:
    _ensure_config_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"default_provider": "local", "providers": {}}


def _save_config(config: Dict):
    _ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def init():
    load_dotenv()
    _ensure_config_dir()


def get_configured_providers() -> List[str]:
    config = _load_config()
    configured = []

    for provider in AVAILABLE_PROVIDERS:
        env_key = PROVIDER_INFO[provider]["env_key"]
        if env_key and os.getenv(env_key):
            configured.append(provider)
        elif _get_api_key(provider):
            configured.append(provider)

    return configured


def _get_api_key(provider: str) -> Optional[str]:
    try:
        key = keyring.get_password(SERVICE_NAME, provider)
        return key
    except Exception:
        return None


def set_api_key(provider: str, api_key: str):
    if provider not in PROVIDER_INFO:
        raise ValueError(f"Provider '{provider}' no soportado. Disponibles: {AVAILABLE_PROVIDERS}")

    if provider == "local":
        raise ValueError("Local provider no requiere API key")

    try:
        keyring.set_password(SERVICE_NAME, provider, api_key)
    except Exception as e:
        raise RuntimeError(f"Error al guardar credencial: {e}")


def get_api_key(provider: str) -> Optional[str]:
    env_key = PROVIDER_INFO[provider]["env_key"]
    if env_key:
        key = os.getenv(env_key)
        if key:
            return key

    return _get_api_key(provider)


def remove_api_key(provider: str):
    if provider not in PROVIDER_INFO:
        raise ValueError(f"Provider '{provider}' no soportado")

    try:
        keyring.delete_password(SERVICE_NAME, provider)
    except Exception:
        pass


def get_default_provider() -> str:
    config = _load_config()
    return config.get("default_provider", "local")


def set_default_provider(provider: str):
    if provider not in PROVIDER_INFO:
        raise ValueError(f"Provider '{provider}' no soportado")

    config = _load_config()
    config["default_provider"] = provider
    _save_config(config)


def show_config():
    config = _load_config()
    configured = get_configured_providers()

    print("\n=== Configuracion de Semantix ===\n")
    print(f"Proveedor por defecto: {config.get('default_provider', 'local')}")

    print("\nProveedores configurados:")
    if not configured:
        print("  (ninguno)")
    else:
        for p in configured:
            info = PROVIDER_INFO[p]
            print(f"  - {p}: {info['name']} ({info['description']})")

    print("\nProveedores disponibles:")
    for p, info in PROVIDER_INFO.items():
        status = "[x]" if p in configured else "[ ]"
        print(f"  {status} {p}: {info['name']}")

    print()


def get_provider_config(provider: str) -> Dict:
    config = _load_config()
    return config.get("providers", {}).get(provider, {})