import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

class FileSystemTools:
    """Tools for managing files and project structures"""
    
    def __init__(self, workspace_dir: str = "./workspace"):
        self.workspace = Path(workspace_dir).expanduser().resolve()
        self.workspace.mkdir(exist_ok=True)
        print(f"📁 Workspace: {self.workspace}")
    
    def create_project(self, project_name: str, project_type: str = "python") -> Dict[str, Any]:
        """Create a complete project structure"""
        
        project_path = self.workspace / project_name
        
        if project_path.exists():
            return {
                "success": False,
                "message": f"Project '{project_name}' already exists at {project_path}"
            }
        
        try:
            # Create project directory
            project_path.mkdir(parents=True)
            
            # Get project template based on type
            if project_type == "python":
                files = self._get_python_template(project_name)
            elif project_type == "web":
                files = self._get_web_template(project_name)
            elif project_type == "ml":
                files = self._get_ml_template(project_name)
            else:
                files = self._get_basic_template(project_name)
            
            # Create all files
            created_files = []
            for file_path, content in files.items():
                full_path = project_path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding='utf-8')
                created_files.append(str(file_path))
            
            # Initialize git repository
            self._init_git(project_path)
            
            return {
                "success": True,
                "message": f"✅ Created {project_type} project '{project_name}'",
                "path": str(project_path),
                "files": created_files
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error creating project: {str(e)}"
            }
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects in workspace"""
        projects = []
        
        try:
            for item in self.workspace.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if it looks like a project
                    has_src = (item / "src").exists()
                    has_readme = (item / "README.md").exists()
                    has_requirements = (item / "requirements.txt").exists()
                    
                    project_type = "unknown"
                    if has_requirements:
                        project_type = "python"
                    if (item / "package.json").exists():
                        project_type = "javascript"
                    
                    projects.append({
                        "name": item.name,
                        "path": str(item),
                        "type": project_type,
                        "has_src": has_src,
                        "has_readme": has_readme,
                        "modified": item.stat().st_mtime
                    })
            
            return sorted(projects, key=lambda x: x["modified"], reverse=True)
            
        except Exception as e:
            print(f"Error listing projects: {e}")
            return []
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read a file and return its content"""
        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = self.workspace / path
            
            if not path.exists():
                return {
                    "success": False,
                    "message": f"File not found: {file_path}"
                }
            
            content = path.read_text(encoding='utf-8')
            return {
                "success": True,
                "content": content,
                "path": str(path),
                "size": len(content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error reading file: {str(e)}"
            }
    
    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Write content to a file"""
        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = self.workspace / path
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            path.write_text(content, encoding='utf-8')
            
            return {
                "success": True,
                "message": f"✅ File written: {path}",
                "path": str(path),
                "size": len(content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error writing file: {str(e)}"
            }
    
    def run_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Run a shell command safely"""
        try:
            work_dir = self.workspace
            if cwd:
                work_dir = work_dir / cwd
            
            result = subprocess.run(
                command.split(),
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "command": command
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "Command timed out after 30 seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error running command: {str(e)}"
            }
    
    def _get_python_template(self, project_name: str) -> Dict[str, str]:
        """Get Python project template"""
        return {
            "README.md": f"""# {project_name}

A Python project created by Local Development Assistant.

## Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
python src/main.py
```

## Development
```bash
# Run tests
pytest tests/

# Format code
black src/ tests/

# Type checking
mypy src/
```
""",
            "requirements.txt": """# Core dependencies
requests>=2.25.1
python-dotenv>=0.19.0

# Development dependencies
pytest>=6.2.4
black>=21.5b0
mypy>=0.910
flake8>=3.9.2
""",
            "src/__init__.py": "",
            "src/main.py": f'''#!/usr/bin/env python3
"""
{project_name} - Main application module
"""

def main():
    """Main application entry point"""
    print("🚀 Welcome to {project_name}!")
    print("This project was created by Local Development Assistant.")

if __name__ == "__main__":
    main()
''',
            "src/utils.py": '''"""
Utility functions for the project
"""

def safe_divide(a: float, b: float) -> float:
    """Safely divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def format_message(message: str, prefix: str = "INFO") -> str:
    """Format a message with a prefix"""
    return f"[{prefix}] {message}"
''',
            "tests/__init__.py": "",
            "tests/test_main.py": f'''"""
Tests for main module
"""
import pytest
from src.main import main

def test_main():
    """Test that main function runs without error"""
    try:
        main()
        assert True
    except Exception as e:
        pytest.fail(f"main() raised {{e}}")
''',
            "tests/test_utils.py": '''"""
Tests for utility functions
"""
import pytest
from src.utils import safe_divide, format_message

def test_safe_divide():
    """Test safe division function"""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(7, 3) == pytest.approx(2.333, rel=1e-2)
    
    with pytest.raises(ValueError):
        safe_divide(10, 0)

def test_format_message():
    """Test message formatting"""
    assert format_message("test") == "[INFO] test"
    assert format_message("error", "ERROR") == "[ERROR] error"
''',
            ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
""",
            ".env.example": f"""# Environment variables for {project_name}
DEBUG=True
LOG_LEVEL=INFO
""",
            "pyproject.toml": f'''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "A Python project created by Local Development Assistant"
authors = [{{name = "Developer", email = "dev@example.com"}}]
license = {{text = "MIT"}}
readme = "README.md"
requires-python = ">=3.8"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
'''
        }
    
    def _get_ml_template(self, project_name: str) -> Dict[str, str]:
        """Get Machine Learning project template"""
        base_template = self._get_python_template(project_name)
        
        # Update requirements for ML
        base_template["requirements.txt"] = """# Machine Learning
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0

# Data processing
scipy>=1.7.0
plotly>=5.0.0

# Development
pytest>=6.2.4
black>=21.5b0
mypy>=0.910
"""
        
        # Add ML-specific files
        base_template["src/data_loader.py"] = '''"""
Data loading and preprocessing utilities
"""
import pandas as pd
import numpy as np
from pathlib import Path

class DataLoader:
    """Handle data loading and basic preprocessing"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """Load CSV file"""
        file_path = self.data_dir / filename
        return pd.read_csv(file_path)
    
    def basic_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Basic data cleaning"""
        # Remove duplicates
        df_clean = df.drop_duplicates()
        
        # Handle missing values (simple strategy)
        df_clean = df_clean.fillna(df_clean.mean(numeric_only=True))
        
        return df_clean
'''
        
        base_template["notebooks/.gitkeep"] = ""
        base_template["data/.gitkeep"] = ""
        base_template["models/.gitkeep"] = ""
        
        return base_template
    
    def _get_web_template(self, project_name: str) -> Dict[str, str]:
        """Get web project template with FastAPI"""
        base_template = self._get_python_template(project_name)
        
        # Update requirements for web
        base_template["requirements.txt"] = """# Web framework
fastapi>=0.68.0
uvicorn[standard]>=0.15.0

# Database
sqlalchemy>=1.4.0
alembic>=1.7.0

# HTTP requests
requests>=2.26.0
httpx>=0.24.0

# Development
pytest>=6.2.4
pytest-asyncio>=0.15.0
black>=21.5b0
"""
        
        # Update main.py for FastAPI
        base_template["src/main.py"] = f'''"""
{project_name} - FastAPI Web Application
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="{project_name}", version="0.1.0")

@app.get("/")
async def root():
    """Root endpoint"""
    return {{"message": "Welcome to {project_name}!"}}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        return base_template
    
    def _get_basic_template(self, project_name: str) -> Dict[str, str]:
        """Get basic project template"""
        return {
            "README.md": f"# {project_name}\n\nA project created by Local Development Assistant.",
            "main.py": f'print("Hello from {project_name}!")',
            ".gitignore": "*.pyc\n__pycache__/\n.env\n"
        }
    
    def _init_git(self, project_path: Path):
        """Initialize git repository"""
        try:
            subprocess.run(["git", "init"], cwd=project_path, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=project_path, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_path, capture_output=True)
        except:
            pass  # Git is optional

# Test the file tools
def test_file_tools():
    """Test file system tools"""
    print("🔧 Testing File System Tools...")
    
    tools = FileSystemTools("./test_workspace")
    
    # Test project creation
    result = tools.create_project("test_project", "python")
    print(f"Project creation: {result['message']}")
    
    # Test listing projects
    projects = tools.list_projects()
    print(f"Found {len(projects)} projects")
    
    # Test file operations
    test_file = "test_project/hello.txt"
    write_result = tools.write_file(test_file, "Hello from File Tools!")
    print(f"File write: {write_result['message']}")
    
    read_result = tools.read_file(test_file)
    if read_result["success"]:
        print(f"File read: {read_result['content']}")
    
    print("✅ File tools test complete!")

if __name__ == "__main__":
    test_file_tools()
