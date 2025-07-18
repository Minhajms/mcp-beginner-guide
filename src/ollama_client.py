import requests
import json
from typing import Optional, Dict, Any

class OllamaClient:
    """Client for communicating with Ollama API"""
    
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3.2"):
        self.host = host
        self.model = model
        self.base_url = f"{host}/api"
    
    def is_available(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(self.model in model.get("name", "") for model in models)
            return False
        except requests.exceptions.RequestException:
            return False
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate response from Ollama"""
        
        # Build the request payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        # Add system prompt if provided
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "model": result.get("model", self.model),
                    "done": result.get("done", True)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
    
    def chat(self, messages: list, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Chat with Ollama using conversation history"""
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        if system_prompt:
            # Add system message at the beginning
            payload["messages"] = [{"role": "system", "content": system_prompt}] + messages
        
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "message": result.get("message", {}),
                    "done": result.get("done", True)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }

# Test the client
def test_ollama():
    """Test Ollama connection and basic functionality"""
    print("🔍 Testing Ollama connection...")
    
    client = OllamaClient()
    
    # Test availability
    if not client.is_available():
        print("❌ Ollama is not available. Make sure it's running with:")
        print("   ollama serve")
        print("   ollama pull llama3.2")
        return False
    
    print("✅ Ollama is available!")
    
    # Test generation
    print("\n🤖 Testing code generation...")
    result = client.generate(
        "Write a Python function to create a directory safely:",
        system_prompt="You are a helpful coding assistant. Provide clean, well-documented Python code."
    )
    
    if result["success"]:
        print("✅ Code generation successful!")
        print("\n📝 Generated code:")
        print(result["response"])
        return True
    else:
        print(f"❌ Generation failed: {result['error']}")
        return False

if __name__ == "__main__":
    test_ollama()
