from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import traceback

from ollama_client import OllamaClient
from file_tools import FileSystemTools

class MCPRequest(BaseModel):
    """Request model for MCP operations"""
    action: str
    parameters: Dict[str, Any] = {}
    context: Optional[str] = None

class MCPResponse(BaseModel):
    """Response model for MCP operations"""
    success: bool
    data: Optional[Any] = None
    message: str = ""
    error: Optional[str] = None

class LocalDevAssistantMCP:
    """MCP Server for Local Development Assistant"""
    
    def __init__(self):
        self.ollama = OllamaClient()
        self.file_tools = FileSystemTools()
        
        # System prompt for the assistant
        self.system_prompt = """You are a Local Development Assistant. You help developers by:

1. Creating project structures and files
2. Generating code based on requirements
3. Managing development workflows
4. Providing coding assistance and explanations

Always provide practical, working code with proper error handling.
When creating projects, suggest appropriate structures and best practices.
Be concise but thorough in your responses."""

        # Available tools/actions
        self.tools = {
            "create_project": self._create_project,
            "list_projects": self._list_projects,
            "generate_code": self._generate_code,
            "read_file": self._read_file,
            "write_file": self._write_file,
            "run_command": self._run_command,
            "chat": self._chat,
            "analyze_code": self._analyze_code,
            "suggest_improvements": self._suggest_improvements
        }
    
    def process_request(self, request: MCPRequest) -> MCPResponse:
        """Process an MCP request"""
        try:
            # Check if Ollama is available for AI-powered actions
            ai_actions = ["generate_code", "chat", "analyze_code", "suggest_improvements"]
            if request.action in ai_actions and not self.ollama.is_available():
                return MCPResponse(
                    success=False,
                    error="Ollama is not available. Please ensure it's running with 'ollama serve'."
                )
            
            # Execute the requested action
            if request.action in self.tools:
                result = self.tools[request.action](request.parameters)
                
                if isinstance(result, dict) and "success" in result:
                    return MCPResponse(
                        success=result["success"],
                        data=result.get("data"),
                        message=result.get("message", ""),
                        error=result.get("error")
                    )
                else:
                    return MCPResponse(
                        success=True,
                        data=result,
                        message="Action completed successfully"
                    )
            else:
                return MCPResponse(
                    success=False,
                    error=f"Unknown action: {request.action}. Available actions: {list(self.tools.keys())}"
                )
                
        except Exception as e:
            return MCPResponse(
                success=False,
                error=f"Error processing request: {str(e)}",
                message=traceback.format_exc()
            )
    
    def _create_project(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project"""
        project_name = params.get("name", "")
        project_type = params.get("type", "python")
        
        if not project_name:
            return {"success": False, "error": "Project name is required"}
        
        return self.file_tools.create_project(project_name, project_type)
    
    def _list_projects(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all projects"""
        projects = self.file_tools.list_projects()
        return {
            "success": True,
            "data": projects,
            "message": f"Found {len(projects)} projects"
        }
    
    def _read_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a file"""
        file_path = params.get("path", "")
        if not file_path:
            return {"success": False, "error": "File path is required"}
        
        return self.file_tools.read_file(file_path)
    
    def _write_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Write content to a file"""
        file_path = params.get("path", "")
        content = params.get("content", "")
        
        if not file_path:
            return {"success": False, "error": "File path is required"}
        
        return self.file_tools.write_file(file_path, content)
    
    def _run_command(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run a shell command"""
        command = params.get("command", "")
        cwd = params.get("cwd")
        
        if not command:
            return {"success": False, "error": "Command is required"}
        
        return self.file_tools.run_command(command, cwd)
    
    def _generate_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code using Ollama"""
        prompt = params.get("prompt", "")
        language = params.get("language", "python")
        
        if not prompt:
            return {"success": False, "error": "Code prompt is required"}
        
        # Enhanced prompt for code generation
        enhanced_prompt = f"""Generate {language} code for: {prompt}

Requirements:
- Provide clean, well-documented code
- Include proper error handling
- Add comments explaining key parts
- Follow best practices for {language}
- Make the code production-ready

Code:"""
        
        result = self.ollama.generate(enhanced_prompt, self.system_prompt)
        
        if result["success"]:
            return {
                "success": True,
                "data": {
                    "code": result["response"],
                    "language": language,
                    "prompt": prompt
                },
                "message": "Code generated successfully"
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }
    
    def _chat(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Chat with the assistant"""
        message = params.get("message", "")
        history = params.get("history", [])
        
        if not message:
            return {"success": False, "error": "Message is required"}
        
        # Build conversation history
        messages = []
        for msg in history:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        result = self.ollama.chat(messages, self.system_prompt)
        
        if result["success"]:
            response_content = result["message"].get("content", "")
            return {
                "success": True,
                "data": {
                    "response": response_content,
                    "role": "assistant"
                },
                "message": "Chat response generated"
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }
    
    def _analyze_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code for issues and improvements"""
        code = params.get("code", "")
        file_path = params.get("file_path", "")
        
        # Get code from file if path provided
        if file_path:
            file_result = self.file_tools.read_file(file_path)
            if not file_result["success"]:
                return file_result
            code = file_result["content"]
        
        if not code:
            return {"success": False, "error": "Code or file path is required"}
        
        prompt = f"""Analyze this code for potential issues, improvements, and best practices:

```
{code}
```

Please provide:
1. Code quality assessment
2. Potential bugs or issues
3. Performance improvements
4. Security considerations
5. Best practice recommendations

Analysis:"""
        
        result = self.ollama.generate(prompt, self.system_prompt)
        
        if result["success"]:
            return {
                "success": True,
                "data": {
                    "analysis": result["response"],
                    "code_length": len(code)
                },
                "message": "Code analysis completed"
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }
    
    def _suggest_improvements(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest improvements for a project or code"""
        project_name = params.get("project", "")
        
        if not project_name:
            return {"success": False, "error": "Project name is required"}
        
        # Get project info
        projects = self.file_tools.list_projects()
        project = next((p for p in projects if p["name"] == project_name), None)
        
        if not project:
            return {"success": False, "error": f"Project '{project_name}' not found"}
        
        # Read key files to understand project structure
        key_files = ["README.md", "requirements.txt", "src/main.py"]
        project_info = {"files": {}}
        
        for file_path in key_files:
            full_path = f"{project_name}/{file_path}"
            file_result = self.file_tools.read_file(full_path)
            if file_result["success"]:
                project_info["files"][file_path] = file_result["content"]
        
        prompt = f"""Analyze this project and suggest improvements:

Project: {project_name}
Type: {project["type"]}

Project files:
{json.dumps(project_info, indent=2)}

Please suggest:
1. Project structure improvements
2. Code organization enhancements
3. Missing files or dependencies
4. Development workflow improvements
5. Testing and documentation suggestions

Suggestions:"""
        
        result = self.ollama.generate(prompt, self.system_prompt)
        
        if result["success"]:
            return {
                "success": True,
                "data": {
                    "suggestions": result["response"],
                    "project": project_name,
                    "analyzed_files": list(project_info["files"].keys())
                },
                "message": "Project analysis completed"
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }

# FastAPI app
app = FastAPI(title="Local Development Assistant MCP Server", version="1.0.0")
mcp_server = LocalDevAssistantMCP()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Local Development Assistant MCP Server",
        "version": "1.0.0",
        "available_actions": list(mcp_server.tools.keys()),
        "ollama_available": mcp_server.ollama.is_available()
    }

@app.post("/mcp", response_model=MCPResponse)
async def process_mcp_request(request: MCPRequest):
    """Process MCP requests"""
    return mcp_server.process_request(request)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ollama_available": mcp_server.ollama.is_available(),
        "workspace": str(mcp_server.file_tools.workspace)
    }

@app.get("/tools")
async def list_tools():
    """List available tools"""
    return {
        "tools": list(mcp_server.tools.keys()),
        "descriptions": {
            "create_project": "Create a new project with specified type",
            "list_projects": "List all projects in workspace",
            "generate_code": "Generate code using AI",
            "read_file": "Read file contents",
            "write_file": "Write content to file",
            "run_command": "Execute shell commands",
            "chat": "Chat with the assistant",
            "analyze_code": "Analyze code for improvements",
            "suggest_improvements": "Suggest project improvements"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Local Development Assistant MCP Server...")
    print(f"🤖 Ollama available: {mcp_server.ollama.is_available()}")
    print(f"📁 Workspace: {mcp_server.file_tools.workspace}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
