# MCP Beginner's Guide

This project demonstrates the Model Context Protocol (MCP) concepts in a practical way that's easy for students to understand.

## What is MCP (Model Context Protocol)?

MCP is a standardized way for applications to communicate with AI models. It defines how:

1. Applications can request AI capabilities
2. AI models can access tools and resources
3. Results are returned in a structured format

Think of MCP as a bridge between your application and AI capabilities.

## Key MCP Components Explained

### 1. MCP Host
The component that manages communication between clients and the MCP server.
- In this project: `mcp_server.py` with the FastAPI application

### 2. MCP Client
The application that sends requests to the MCP server.
- In this project: `cli.py` (command-line interface)

### 3. MCP Server
The component that processes requests and provides AI capabilities.
- In this project: `LocalDevAssistantMCP` class in `mcp_server.py`

### 4. MCP Resources
File-like data that can be read by clients.
- In this project: File contents, project listings, analysis results

### 5. MCP Tools
Functions that can be called by the AI model.
- In this project: Project creation, code generation, file operations

### 6. MCP Prompts
Pre-written templates that help accomplish specific tasks.
- In this project: System prompt, code generation prompts, analysis prompts

## How MCP Works in This Project

1. **Request Flow**:
   ```
   User → CLI (client) → MCP Server → Ollama (AI) → Response → User
   ```

2. **Example**: When you run `python src/cli.py generate "function to read CSV"`:
   - CLI formats this as an MCP request with action "generate_code"
   - MCP server receives the request
   - Server prepares a prompt and sends it to Ollama
   - Ollama generates code
   - Response is formatted and returned to the user

## Try It Yourself

### Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Ollama and the required model:
   ```bash
   # Install Ollama from https://ollama.ai
   ollama serve
   ollama pull llama3.2
   ```

### Basic MCP Commands

1. **Generate Code** (MCP Tool Example):
   ```bash
   python src/cli.py generate "function to read CSV file" --language python
   ```

2. **Create Project** (MCP Resource Example):
   ```bash
   python src/cli.py create my_project --type python
   ```

3. **Chat with AI** (MCP Prompt Example):
   ```bash
   python src/cli.py chat
   ```

## Project Structure

```
├── src/
│   ├── cli.py           # MCP Client
│   ├── mcp_server.py    # MCP Host & Server
│   ├── file_tools.py    # File operations tools
│   └── ollama_client.py # AI model interface
├── workspace/           # Project workspace
└── README.md            # This file
```

## Learning MCP Concepts

### 1. MCP Request Structure
```python
# From mcp_server.py
class MCPRequest(BaseModel):
    """Request model for MCP operations"""
    action: str
    parameters: Dict[str, Any] = {}
    context: Optional[str] = None
```

### 2. MCP Response Structure
```python
# From mcp_server.py
class MCPResponse(BaseModel):
    """Response model for MCP operations"""
    success: bool
    data: Optional[Any] = None
    message: str = ""
    error: Optional[str] = None
```

### 3. MCP Tool Registration
```python
# From mcp_server.py
self.tools = {
    "create_project": self._create_project,
    "list_projects": self._list_projects,
    "generate_code": self._generate_code,
    # ... more tools
}
```

## Why MCP Matters

MCP provides a standardized way to:
1. Access AI capabilities in applications
2. Give AI models access to tools and resources
3. Structure requests and responses
4. Maintain security through controlled access

By understanding MCP, you'll be better equipped to build applications that leverage AI capabilities in a structured, secure way.

## Next Steps

1. Explore the code to see how MCP is implemented
2. Try modifying the tools or adding new ones
3. Experiment with different prompts
4. Build your own MCP client application

## Resources

- [MCP Documentation](https://github.com/microsoft/mcp)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ollama](https://ollama.ai/)