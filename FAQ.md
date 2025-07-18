# Local Development Assistant FAQ

## General Questions

### What is the Local Development Assistant?
The Local Development Assistant is a tool that provides AI-powered assistance for local development tasks. It helps with creating projects, generating code, analyzing files, and providing development guidance through an interactive interface.

### What can I do with this tool?
- Create new projects with predefined templates
- Generate code snippets based on natural language prompts
- Analyze code for quality, bugs, and best practices
- Get project improvement suggestions
- Chat with an AI assistant for development help

### What are the system requirements?
- Python 3.8 or higher
- Ollama installed and running locally (for AI features)
- The llama3.2 model pulled in Ollama

## Technical Questions

### What is the MCP Server?

MCP stands for "Model Context Protocol" - it's a standardized way for applications to communicate with AI models.

#### How the MCP Server works in this project:

1. **Local Service**: The MCP server runs locally on your machine as a service that coordinates between your commands and the AI capabilities.

2. **Bridge Function**: It acts as a bridge between:
   - Your development tools/applications
   - The AI capabilities provided by Ollama (which runs the llama3.2 model)

3. **Request Handling**: The server receives requests through either:
   - The CLI interface (when you run commands)
   - A FastAPI web interface (for programmatic access)

4. **Processing Flow**:
   - Receives a structured request with an action and parameters
   - Routes it to the appropriate tool or service
   - Processes the request using file tools or Ollama AI
   - Returns a structured response

5. **File Location**: The MCP server code is saved in `src/mcp_server.py`. It's not deployed remotely - it runs locally when you use the development assistant.

### How does the AI integration work?

The project uses Ollama, a local AI model server, to provide AI capabilities:

1. The `OllamaClient` class in `ollama_client.py` communicates with the locally running Ollama service
2. By default, it uses the llama3.2 model
3. All AI processing happens locally on your machine, ensuring privacy
4. The system prompt configures the AI to act as a development assistant

### What project templates are available?

The system currently supports the following project templates:

1. **Python**: Standard Python project with tests, documentation, and best practices
2. **Web**: FastAPI-based web application with database integration
3. **ML**: Machine learning project with data processing and visualization tools
4. **Basic**: Minimal project structure for quick starts

## Usage Questions

### How do I start using the tool?

1. Ensure Ollama is installed and running:
   ```
   ollama serve
   ollama pull llama3.2
   ```

2. Run the CLI with one of the available commands:
   ```
   python src/cli.py [command]
   ```

### What commands are available?

- `create [name] --type [type]`: Create a new project
- `list`: List existing projects
- `generate [prompt] --language [lang]`: Generate code
- `chat`: Start interactive chat with the assistant
- `analyze [file]`: Analyze a code file
- `suggest [project]`: Get project improvement suggestions
- `status`: Check system status

### How do I create a new project?

```
python src/cli.py create my_project --type python
```

Available project types: python, web, ml, basic

### How do I generate code?

```
python src/cli.py generate "function to read CSV file" --language python
```

You can optionally save the generated code to a file:
```
python src/cli.py generate "function to read CSV file" --language python --save output.py
```

### How do I chat with the assistant?

```
python src/cli.py chat
```

This will start an interactive chat session where you can ask development questions.

## Troubleshooting

### AI features aren't working

If AI features aren't working, check that:

1. Ollama is installed and running (`ollama serve`)
2. The llama3.2 model is pulled (`ollama pull llama3.2`)
3. The Ollama API is accessible at http://localhost:11434

You can check the status with:
```
python src/cli.py status
```

### Project creation fails

If project creation fails, check:

1. The workspace directory exists and is writable
2. The project name doesn't already exist
3. You have sufficient permissions to create files and directories

### Other issues

For other issues:

1. Check the error messages for specific details
2. Ensure all dependencies are installed
3. Verify that your Python version is 3.8 or higher