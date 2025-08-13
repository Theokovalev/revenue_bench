#!/usr/bin/env python3
"""
Test script to verify the public repository structure
"""

import os
import json
from pathlib import Path


def check_file(path, description):
    """Check if a file exists and is readable"""
    if path.exists():
        try:
            if path.suffix == '.json':
                with open(path, 'r') as f:
                    json.load(f)
            else:
                with open(path, 'r') as f:
                    content = f.read()
                    # Basic check for yaml files
                    if path.suffix == '.yaml' and not content.strip():
                        raise ValueError("Empty YAML file")
            print(f"✅ {description}: {path.name}")
            return True
        except Exception as e:
            print(f"❌ {description}: {path.name} - Error: {e}")
            return False
    else:
        print(f"❌ {description}: {path.name} - File not found")
        return False


def check_directory(path, description):
    """Check if a directory exists"""
    if path.exists() and path.is_dir():
        print(f"✅ {description}: {path.name}/")
        return True
    else:
        print(f"❌ {description}: {path.name}/ - Directory not found")
        return False


def main():
    root = Path(__file__).parent
    
    print("🔍 Verifying Revenue Bench Public Repository Structure")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check root files
    print("\n📁 Root Files")
    print("-" * 40)
    all_checks_passed &= check_file(root / "README.md", "README")
    all_checks_passed &= check_file(root / "requirements.txt", "Requirements")
    all_checks_passed &= check_file(root / ".env.example", "Environment example")
    all_checks_passed &= check_file(root / ".gitignore", "Git ignore")
    all_checks_passed &= check_file(root / "config.yaml", "Configuration")
    all_checks_passed &= check_file(root / "run_evaluation.py", "Main runner")
    
    # Check directories
    print("\n📂 Directory Structure")
    print("-" * 40)
    all_checks_passed &= check_directory(root / "benchmark", "Benchmark code")
    all_checks_passed &= check_directory(root / "benchmark" / "tasks", "Tasks")
    all_checks_passed &= check_directory(root / "benchmark" / "judges", "Judges")
    all_checks_passed &= check_directory(root / "benchmark" / "tools", "Tools")
    all_checks_passed &= check_directory(root / "benchmark" / "tasks" / "prompts", "Task prompts")
    all_checks_passed &= check_directory(root / "benchmark" / "judges" / "prompts", "Judge prompts")
    all_checks_passed &= check_directory(root / "docs", "Documentation")
    all_checks_passed &= check_directory(root / "results", "Results")
    all_checks_passed &= check_directory(root / "examples", "Examples")
    
    # Check benchmark files
    print("\n🔧 Benchmark Implementation")
    print("-" * 40)
    all_checks_passed &= check_file(root / "benchmark" / "__init__.py", "Benchmark init")
    all_checks_passed &= check_file(root / "benchmark" / "tasks" / "homebase.py", "Homebase task")
    all_checks_passed &= check_file(root / "benchmark" / "judges" / "multi_judge_scorer.py", "Multi-judge scorer")
    all_checks_passed &= check_file(root / "benchmark" / "tools" / "tavily_search.py", "Tavily search")
    all_checks_passed &= check_file(root / "benchmark" / "tools" / "tavily_extract.py", "Tavily extract")
    
    # Check prompts
    print("\n📝 Prompts (Transparent)")
    print("-" * 40)
    all_checks_passed &= check_file(root / "benchmark" / "tasks" / "prompts" / "homebase_prompt.md", "Homebase prompt")
    all_checks_passed &= check_file(root / "benchmark" / "judges" / "prompts" / "judge_prompt.md", "Judge prompt")
    
    # Check documentation
    print("\n📚 Documentation")
    print("-" * 40)
    all_checks_passed &= check_file(root / "docs" / "SETUP.md", "Setup guide")
    all_checks_passed &= check_file(root / "docs" / "METHODOLOGY.md", "Methodology")
    
    # Check results
    print("\n📊 Results")
    print("-" * 40)
    all_checks_passed &= check_file(root / "results" / "leaderboard.json", "Leaderboard")
    
    # Check examples
    print("\n💡 Examples")
    print("-" * 40)
    all_checks_passed &= check_file(root / "examples" / "run_single_model.py", "Single model example")
    all_checks_passed &= check_file(root / "examples" / "compare_models.py", "Compare models example")
    
    # Summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✅ All checks passed! Repository is ready for publication.")
        print("\nNext steps:")
        print("1. Review all files for sensitive information")
        print("2. Test with: python run_evaluation.py --list-models")
        print("3. Create GitHub repository")
        print("4. Push to GitHub")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    
    return all_checks_passed


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)