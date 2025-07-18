#!/usr/bin/env python3
"""
CLI interface for Local Development Assistant
"""

import argparse
import json
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server import LocalDevAssistantMCP, MCPRequest

class DevAssistantCLI:
    """Command line interface for the development assistant"""
    
    def __init__(self):
        self.mcp = LocalDevAssistantMCP()
    
    def create_project(self, args):
        """Create a new project"""
        request = MCPRequest(
            action="create_project",
            parameters={
                "name": args.name,
                "type": args.type
            }
        )
        
        response = self.mcp.process_request(request)
        
        if response.success:
            print(f"✅ {response.message}")
            if response.data:
                print(f"📁 Path: {response.data.get('path', 'N/A')}")
                files = response.data.get('files', [])
                print(f"📄 Created {len(files)} files")
        else:
            print(f"❌ Error: {response.error}")
    
    def list_projects(self, args):
        """List all projects"""
        request = MCPRequest(action="list_projects")
        response = self.mcp.process_request(request)
        
        if response.success:
            projects = response.data or []
            if not projects:
                print("📂 No projects found")
                return
            
            print(f"📂 Found {len(projects)} projects:")
            print("-" * 50)
            for project in projects:
                print(f"🔸 {project['name']} ({project['type']})")
                print(f"   Path: {project['path']}")
                if project.get('has_readme'):
                    print("   ✅ Has README")
                print()
        else:
            print(f"❌ Error: {response.error}")
    
    def generate_code(self, args):
        """Generate code"""
        request = MCPRequest(
            action="generate_code",
            parameters={
                "prompt": args.prompt,
                "language": args.language
            }
        )
        
        response = self.mcp.process_request(request)
        
        if response.success:
            print(f"🤖 Generated {args.language} code:")
            print("-" * 50)
            print(response.data["code"])
            print("-" * 50)
            
            # Offer to save to file
            if args.save:
                file_path = args.save
                write_request = MCPRequest(
                    action="write_file",
                    parameters={
                        "path": file_path,
                        "content": response.data["code"]
                    }
                )
                write_response = self.mcp.process_request(write_request)
                if write_response.success:
                    print(f"💾 Code saved to: {file_path}")
                else:
                    print(f"❌ Error saving file: {write_response.error}")
        else:
            print(f"❌ Error: {response.error}")
    
    def chat(self, args):
        """Chat with the assistant"""
        print("💬 Chat with Local Development Assistant")
        print("Type 'exit', 'quit', or press Ctrl+C to exit")
        print("-" * 50)
        
        history = []
        
        try:
            while True:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                request = MCPRequest(
                    action="chat",
                    parameters={
                        "message": user_input,
                        "history": history
                    }
                )
                
                response = self.mcp.process_request(request)
                
                if response.success:
                    ai_response = response.data["response"]
                    print(f"Assistant: {ai_response}")
                    
                    # Update history
                    history.append({"role": "user", "content": user_input})
                    history.append({"role": "assistant", "content": ai_response})
                    
                    # Keep history manageable (last 10 exchanges)
                    if len(history) > 20:
                        history = history[-20:]
                else:
                    print(f"❌ Error: {response.error}")
                
                print()
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    
    def analyze_file(self, args):
        """Analyze a code file"""
        request = MCPRequest(
            action="analyze_code",
            parameters={"file_path": args.file}
        )
        
        response = self.mcp.process_request(request)
        
        if response.success:
            print(f"🔍 Analysis for: {args.file}")
            print("-" * 50)
            print(response.data["analysis"])
        else:
            print(f"❌ Error: {response.error}")
    
    def suggest_improvements(self, args):
        """Suggest improvements for a project"""
        request = MCPRequest(
            action="suggest_improvements",
            parameters={"project": args.project}
        )
        
        response = self.mcp.process_request(request)
        
        if response.success:
            print(f"💡 Suggestions for project: {args.project}")
            print("-" * 50)
            print(response.data["suggestions"])
        else:
            print(f"❌ Error: {response.error}")
    
    def status(self, args):
        """Show system status"""
        print("🔧 Local Development Assistant Status")
        print("-" * 40)
        print(f"🤖 Ollama Available: {'✅ Yes' if self.mcp.ollama.is_available() else '❌ No'}")
        print(f"📁 Workspace: {self.mcp.file_tools.workspace}")
        
        # List projects
        projects = self.mcp.file_tools.list_projects()
        print(f"📂 Projects: {len(projects)}")
        
        if not self.mcp.ollama.is_available():
            print("\n⚠️  To enable AI features, ensure Ollama is running:")
            print("   ollama serve")
            print("   ollama pull llama3.2")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Local Development Assistant CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s create my_app --type python
  %(prog)s list
  %(prog)s generate "function to read CSV file" --language python
  %(prog)s chat
  %(prog)s analyze src/main.py
  %(prog)s status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create project command
    create_parser = subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('--type', choices=['python', 'web', 'ml', 'basic'], 
                              default='python', help='Project type')
    
    # List projects command
    list_parser = subparsers.add_parser('list', help='List all projects')
    
    # Generate code command
    generate_parser = subparsers.add_parser('generate', help='Generate code')
    generate_parser.add_argument('prompt', help='Code generation prompt')
    generate_parser.add_argument('--language', default='python', help='Programming language')
    generate_parser.add_argument('--save', help='Save generated code to file')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Chat with the assistant')
    
    # Analyze file command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a code file')
    analyze_parser.add_argument('file', help='File path to analyze')
    
    # Suggest improvements command
    suggest_parser = subparsers.add_parser('suggest', help='Suggest project improvements')
    suggest_parser.add_argument('project', help='Project name')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = DevAssistantCLI()
    
    # Route to appropriate handler
    handlers = {
        'create': cli.create_project,
        'list': cli.list_projects,
        'generate': cli.generate_code,
        'chat': cli.chat,
        'analyze': cli.analyze_file,
        'suggest': cli.suggest_improvements,
        'status': cli.status
    }
    
    if args.command in handlers:
        try:
            handlers[args.command](args)
        except KeyboardInterrupt:
            print("\n⏹️  Operation cancelled")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ Unknown command: {args.command}")
        parser.print_help()

if __name__ == "__main__":
    main()
