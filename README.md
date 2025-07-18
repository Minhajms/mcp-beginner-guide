# Local Development Assistant

A powerful AI-powered tool to help with your coding and development tasks, right on your local machine.

## What is this?

Local Development Assistant is a tool that helps you:
- Create new coding projects with the right structure
- Generate code based on your descriptions
- Analyze your code for improvements
- Chat with an AI assistant about coding problems

All of this happens on your computer - your code stays private and secure.

## How it works

This tool combines:
1. A simple command-line interface
2. Local AI capabilities (using Ollama)
3. Project management tools

It's like having a helpful coding buddy who can create projects, write code, and answer your questions!

## Requirements

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- The llama3.2 model pulled in Ollama

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/local-dev-assistant.git
   cd local-dev-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure Ollama is running with the required model:
   ```bash
   ollama serve
   ollama pull llama3.2
   ```

## Quick Start

### Create a new project

```bash
python src/cli.py create my_project --type python
```

This creates a new Python project with all the necessary files and structure.

### Generate code

```bash
python src/cli.py generate "function to read a CSV file and return a pandas dataframe" --language python
```

### Chat with the assistant

```bash
python src/cli.py chat
```

This opens an interactive chat where you can ask coding questions.

### Analyze your code

```bash
python src/cli.py analyze path/to/your/file.py
```

### Check system status

```bash
python src/cli.py status
```

## Available Project Types

- `python`: Standard Python project with tests
- `web`: Web application using FastAPI
- `ml`: Machine learning project with data science tools
- `basic`: Simple project with minimal structure

## How Commands Work

When you run a command:

1. The CLI processes your request
2. It sends the request to the local MCP server
3. The server uses Ollama to generate AI responses
4. Results are formatted and displayed to you

All processing happens on your machine - no data is sent to external services.

## Troubleshooting

### AI features not working?

Make sure Ollama is running:
```bash
ollama serve
```

And that you have the required model:
```bash
ollama pull llama3.2
```

### Need to see what's happening?

Check the system status:
```bash
python src/cli.py status
```

## Examples

### Creating a machine learning project

```bash
python src/cli.py create customer_prediction --type ml
```

### Generating a function

```bash
python src/cli.py generate "function that validates email addresses" --language python --save email_validator.py
```

### Getting project suggestions

```bash
python src/cli.py suggest my_project
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.