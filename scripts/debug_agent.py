#!/usr/bin/env python3
"""
Debug Agent Tool - Visualize and validate your agent setup

This script helps you debug your agent by checking:
- Ollama connection and model availability
- Tool registration status
- System configuration
- Import paths
- Message flow

Usage:
    python scripts/debug_agent.py                    # Run all checks
    python scripts/debug_agent.py --tools           # Show registered tools only
    python scripts/debug_agent.py --test "query"    # Test agent with query
"""

import sys
import os
import argparse
from typing import List, Dict, Any

# Add src to path so we can import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_status(check: str, status: bool, details: str = ""):
    """Print a check result with status indicator."""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {check}")
    if details:
        print(f"   {details}")

def check_ollama():
    """Check if Ollama is running and accessible."""
    print_section("Ollama Connection")
    
    try:
        import httpx
        response = httpx.get("http://localhost:11434", timeout=5.0)
        if response.status_code == 200:
            print_status("Ollama server running", True, "http://localhost:11434")
            return True
        else:
            print_status("Ollama server running", False, f"Status code: {response.status_code}")
            return False
    except ImportError:
        print_status("httpx library", False, "Run: pip install httpx")
        return False
    except Exception as e:
        print_status("Ollama server running", False, str(e))
        print("\n  Fix: Run 'ollama serve' in a separate terminal")
        return False

def check_model():
    """Check if the configured model is available."""
    print_section("Model Availability")
    
    try:
        import ollama
        models = ollama.list()
        
        if not models or 'models' not in models:
            print_status("Model list accessible", False, "Could not retrieve models")
            return False
        
        print("Available models:")
        for model in models['models']:
            model_name = model.get('name', 'unknown')
            size = model.get('size', 0) / (1024**3)  # Convert to GB
            print(f"  • {model_name} ({size:.1f}GB)")
        
        # Check for llama3.3 (or 3.1 for backward compatibility)
        llama_models = [m for m in models['models'] if 'llama3.3' in m.get('name', '').lower() or 'llama3.1' in m.get('name', '').lower()]
        if llama_models:
            print_status("llama model available", True, llama_models[0]['name'])
            return True
        else:
            print_status("llama model available", False, "")
            print("\n  Fix: Run 'ollama pull llama3.3:8b'")
            return False
            
    except ImportError:
        print_status("ollama library", False, "Run: pip install ollama")
        return False
    except Exception as e:
        print_status("Model check", False, str(e))
        return False

def check_imports():
    """Check if all required modules can be imported."""
    print_section("Python Imports")
    
    imports_to_check = [
        ("ollama", "pip install ollama"),
        ("pytest", "pip install pytest"),
        ("src.agent.simple_agent", "Check project structure"),
        ("src.agent.tool_registry", "Check project structure"),
        ("src.agent.agent_config", "Check project structure"),
    ]
    
    all_good = True
    for module, fix in imports_to_check:
        try:
            __import__(module)
            print_status(f"Import {module}", True)
        except ImportError as e:
            print_status(f"Import {module}", False, f"Fix: {fix}")
            all_good = False
    
    return all_good

def show_registered_tools():
    """Display all registered tools and their schemas."""
    print_section("Registered Tools")
    
    try:
        from src.agent.tool_registry import registry
        from src.agent import simple_agent  # Trigger side-effect imports
        
        schemas = registry.get_schemas()
        
        if not schemas:
            print_status("Tools registered", False, "No tools found!")
            print("\n  Expected tools: calculate, get_weather")
            print("  If you added custom tools, check imports in simple_agent.py")
            return False
        
        print(f"Found {len(schemas)} registered tool(s):\n")
        
        for schema in schemas:
            func = schema['function']
            name = func['name']
            desc = func.get('description', 'No description')
            params = func.get('parameters', {}).get('properties', {})
            
            print(f"📦 {name}")
            print(f"   Description: {desc}")
            
            if params:
                print(f"   Parameters:")
                for param_name, param_info in params.items():
                    param_type = param_info.get('type', 'unknown')
                    param_desc = param_info.get('description', '')
                    print(f"     - {param_name}: {param_type}")
                    if param_desc:
                        print(f"       {param_desc}")
            else:
                print(f"   Parameters: None")
            
            print()
        
        print_status("Tool registration", True, f"{len(schemas)} tools available")
        return True
        
    except Exception as e:
        print_status("Tool registration check", False, str(e))
        import traceback
        traceback.print_exc()
        return False

def show_configuration():
    """Display agent configuration."""
    print_section("Agent Configuration")
    
    try:
        from src.agent.agent_config import config
        
        print(f"Model: {config.model_name}")
        print(f"Temperature: {config.temperature}")
        print(f"System Prompt:")
        print("-" * 60)
        print(config.system_prompt)
        print("-" * 60)
        
        print_status("Configuration loaded", True)
        return True
        
    except Exception as e:
        print_status("Configuration check", False, str(e))
        return False

def test_agent(query: str):
    """Test the agent with a sample query."""
    print_section(f"Testing Agent with Query: '{query}'")
    
    try:
        from src.agent.simple_agent import Agent
        
        print("Initializing agent...")
        agent = Agent()
        
        print(f"\nSending query: {query}")
        print("-" * 60)
        
        response = agent.chat(query)
        
        print("\nAgent response:")
        print(response)
        print("-" * 60)
        
        print_status("Agent test", True, "Query completed successfully")
        return True
        
    except Exception as e:
        print_status("Agent test", False, str(e))
        import traceback
        traceback.print_exc()
        return False

def show_file_structure():
    """Display relevant project file structure."""
    print_section("Project Structure")
    
    expected_files = [
        "src/agent/__init__.py",
        "src/agent/simple_agent.py",
        "src/agent/tool_registry.py",
        "src/agent/agent_config.py",
        "src/agent/tools/__init__.py",
    ]
    
    all_exist = True
    for file_path in expected_files:
        exists = os.path.exists(file_path)
        print_status(file_path, exists)
        if not exists:
            all_exist = False
    
    # Check for custom tools
    tools_dir = "src/agent/tools"
    if os.path.exists(tools_dir):
        tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.py') and f != '__init__.py']
        if tool_files:
            print("\nCustom tool files:")
            for tool_file in tool_files:
                print(f"  • {tool_file}")
    
    return all_exist

def show_help_links():
    """Show helpful links for troubleshooting."""
    print_section("Need Help?")
    
    print("📚 Documentation:")
    print("  • Getting Unstuck Guide: lesson-1-fundamentals/lab-1/getting-unstuck.md")
    print("  • Troubleshooting: lesson-1-fundamentals/lab-1/troubleshooting.md")
    print("  • FAQ: lesson-1-fundamentals/lab-1/FAQ.md")
    print()
    print("💡 Quick Fixes:")
    print("  • Ollama not running: ollama serve")
    print("  • Model missing: ollama pull llama3.3:8b")
    print("  • Import errors: Check __init__.py files exist")
    print("  • Tools not found: Check imports in simple_agent.py")
    print()
    print("🤖 Ask Your AI Assistant:")
    print("  @.cursorrules")
    print("  I ran debug_agent.py and got:")
    print("  [paste results]")
    print("  What should I check according to the project setup?")

def main():
    parser = argparse.ArgumentParser(description="Debug your agentic AI agent setup")
    parser.add_argument("--tools", action="store_true", help="Show registered tools only")
    parser.add_argument("--test", type=str, metavar="QUERY", help="Test agent with a query")
    parser.add_argument("--config", action="store_true", help="Show configuration only")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("  🔍 Agent Debug Tool")
    print("="*60)
    
    if args.tools:
        show_registered_tools()
        return
    
    if args.config:
        show_configuration()
        return
    
    if args.test:
        # Run minimal checks before testing
        ollama_ok = check_ollama()
        model_ok = check_model()
        
        if ollama_ok and model_ok:
            test_agent(args.test)
        else:
            print("\n⚠️  Cannot test agent: Ollama or model not ready")
            print("    Fix the issues above and try again")
        return
    
    # Full diagnostic run
    print("\nRunning full diagnostic...\n")
    
    results = []
    
    # Core checks
    results.append(("File Structure", show_file_structure()))
    results.append(("Python Imports", check_imports()))
    results.append(("Ollama Connection", check_ollama()))
    results.append(("Model Availability", check_model()))
    results.append(("Configuration", show_configuration()))
    results.append(("Tool Registration", show_registered_tools()))
    
    # Summary
    print_section("Summary")
    
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}\n")
    
    for check, status in results:
        print_status(check, status)
    
    if passed == total:
        print("\n✅ All checks passed! Your agent is ready to use.")
        print("\nRun the agent:")
        print("  python -m src.agent.simple_agent")
        print("\nOr test with a query:")
        print('  python scripts/debug_agent.py --test "What is 2+2?"')
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. See issues above.")
        show_help_links()

if __name__ == "__main__":
    main()

