#!/usr/bin/env python3
"""
Quick Start & Testing Script for The Adaptive Chef
Run this to verify everything works before submission
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def print_header(text):
    """Pretty print section headers"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_environment():
    """Verify all requirements are met"""
    print_header("🔍 CHECKING ENVIRONMENT")
    
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 10):
        issues.append("❌ Python 3.10+ required")
    else:
        print("✅ Python version:", sys.version.split()[0])
    
    # Check API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        issues.append("❌ GOOGLE_API_KEY not set")
        print("❌ GOOGLE_API_KEY: Not found")
        print("   Set it with: $env:GOOGLE_API_KEY='your-key-here'")
    else:
        print("✅ GOOGLE_API_KEY: Found")
    
    # Check required packages
    try:
        import google.genai
        print("✅ google-genai: Installed")
    except ImportError:
        issues.append("❌ google-genai not installed")
        print("❌ google-genai: Not installed")
        print("   Install with: pip install google-genai")
    
    # Check file structure
    required_files = [
        "agent.py",
        "requirements.txt",
        ".env",
        "README.md",
        "evaluation/meal_planner.evalset.json",
        "evaluation/test_config.json"
    ]
    
    print("\n📁 Checking file structure:")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            issues.append(f"❌ Missing: {file_path}")
            print(f"❌ {file_path}")
    
    if issues:
        print_header("⚠️  ISSUES FOUND")
        for issue in issues:
            print(issue)
        print("\nPlease fix these issues before continuing.")
        return False
    
    print_header("✅ ENVIRONMENT CHECK PASSED")
    return True

async def test_agent_basic():
    """Test basic agent functionality"""
    print_header("🧪 TESTING AGENT - BASIC FUNCTIONALITY")
    
    try:
        # Import agent components
        print("Importing agent modules...")
        import agent
        print("✅ Agent modules imported successfully")
        
        print("\n⚠️  Note: Full agent testing requires google-adk")
        print("   For now, we've verified the code structure is valid.")
        print("   Install ADK with: pip install google-adk")
        
        print_header("✅ BASIC TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\nCheck agent.py for errors")
        import traceback
        traceback.print_exc()
        return False

def generate_checklist():
    """Generate submission checklist"""
    print_header("📋 SUBMISSION CHECKLIST")
    
    checklist = [
        ("Code Implementation", [
            "✅ agent.py with 5 key concepts",
            "✅ Custom tools (pantry management)",
            "✅ Multi-agent system (LoopAgent)",
            "✅ LRO for Human-in-the-Loop",
            "✅ Memory Bank integration",
            "✅ Code comments explaining logic"
        ]),
        ("Documentation", [
            "✅ README.md (comprehensive)",
            "☐ Architecture diagram image",
            "✅ Setup instructions",
            "✅ Evaluation test cases",
        ]),
        ("Testing", [
            "✅ 8 evaluation test cases",
            "☐ All tests passing",
            "✅ test_config.json configured"
        ]),
        ("Deployment", [
            "☐ .agent_engine_config.json",
            "✅ requirements.txt",
            "✅ .env file"
        ]),
        ("Submission Materials", [
            "☐ GitHub repository (PUBLIC)",
            "☐ Demo video (< 3 min, YouTube)",
            "☐ Video link in README",
            "☐ All files committed"
        ]),
        ("Bonus Points", [
            "✅ Uses Gemini model (5 pts)",
            "☐ Deployment evidence (5 pts)",
            "☐ Demo video (10 pts)"
        ])
    ]
    
    for category, items in checklist:
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")
    
    print("\n" + "=" * 70)
    print("Complete all ☐ items before submitting to Kaggle!")
    print("=" * 70)

def show_next_steps():
    """Show next steps for submission"""
    print_header("🚀 NEXT STEPS FOR SUBMISSION")
    
    steps = """
1. CREATE GITHUB REPOSITORY
   - Go to: https://github.com/new
   - Name: "adaptive-chef-meal-planner"
   - Make it PUBLIC
   - Upload all files from this folder

2. CREATE ARCHITECTURE DIAGRAM
   - Use draw.io, Lucidchart, or Canva
   - Show: Sequential Agent → LoopAgent → Memory Bank
   - Include all 5 sub-agents
   - Save as: docs/architecture_diagram.png
   - Add to GitHub and README

3. INSTALL ADK & RUN FULL TESTS
   pip install google-adk
   
   Then test with:
   python agent.py
   
   Run evaluation:
   adk eval . evaluation/meal_planner.evalset.json `
     --config_file_path=evaluation/test_config.json

4. RECORD DEMO VIDEO (< 3 minutes)
   Structure:
   00:00-00:30 → Problem: "Meal planning takes hours..."
   00:30-01:00 → Why Agents: "Multi-agent system learns & refines..."
   01:00-02:30 → Live Demo:
                 • Set preferences
                 • Add pantry items
                 • Generate meal plan
                 • Show LRO approval! ⏸️
   02:30-03:00 → Tech: "Google ADK, Gemini 2.0, 5 key concepts"
   
   Upload to YouTube (Unlisted)
   Add link to README

5. DEPLOY (OPTIONAL +5 pts)
   Create .agent_engine_config.json:
   {
     "agent_id": "adaptive-chef",
     "model": "gemini-2.0-flash-exp",
     "region": "us-central1"
   }
   
   Deploy:
   adk deploy agent_engine --project=YOUR_PROJECT .

6. FINAL CHECKS
   ✓ README has video link
   ✓ All code commented
   ✓ GitHub repo is PUBLIC
   ✓ .env file in .gitignore (no API keys exposed!)

7. SUBMIT TO KAGGLE
   - Go to: https://www.kaggle.com/competitions/[competition-url]
   - Click "New Writeup"
   - Fill in:
     • Title: "The Adaptive Chef - AI Meal Planning Agent"
     • Track: Concierge Agents
     • Description: Copy from README
     • GitHub Link: https://github.com/YOUR_USERNAME/adaptive-chef
     • Video Link: YouTube URL
   - Submit before Dec 1, 11:59 AM PT

🎯 TARGET SCORE: 100/100 points

Category 1 (Pitch): 30 points
Category 2 (Implementation): 50 points
Documentation: 20 points
BONUS: Gemini (5) + Deployment (5) + Video (10) = 20 points
─────────────────────────────────────────────────────
TOTAL: 100 points ✨
"""
    
    print(steps)

def create_deployment_config():
    """Create deployment configuration file"""
    print_header("🚀 CREATING DEPLOYMENT CONFIG")
    
    config_content = """{
  "agent_id": "adaptive-chef",
  "display_name": "The Adaptive Chef",
  "description": "AI-powered meal planning agent with multi-agent system",
  "model": "gemini-2.0-flash-exp",
  "region": "us-central1",
  "entry_point": "agent.py",
  "agent_name": "root_agent",
  
  "runtime": {
    "python_version": "3.10",
    "requirements_file": "requirements.txt"
  },
  
  "scaling": {
    "min_instances": 0,
    "max_instances": 10,
    "concurrency": 5
  },
  
  "environment": {
    "GOOGLE_API_KEY": "${SECRET:google_api_key}"
  },
  
  "endpoints": {
    "rest_api": true,
    "websocket": false
  }
}
"""
    
    try:
        with open(".agent_engine_config.json", "w") as f:
            f.write(config_content)
        print("✅ Created .agent_engine_config.json")
        print("   Use this for deployment with: adk deploy agent_engine")
    except Exception as e:
        print(f"❌ Failed to create config: {e}")

def main():
    """Main execution flow"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                                 ║
║           🍳 THE ADAPTIVE CHEF - QUICK START SCRIPT            ║
║                                                                 ║
║               AI-Powered Meal Planner • Capstone Project        ║
║                                                                 ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check environment
    if not check_environment():
        print("\n💡 QUICK FIXES:")
        print("   1. Install Python 3.10+")
        print("   2. Set API key: $env:GOOGLE_API_KEY='your-key'")
        print("   3. pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 2: Test agent
    print("\n🎯 Ready to test the agent code? (y/n): ", end="")
    if input().lower() == 'y':
        if not asyncio.run(test_agent_basic()):
            print("\n⚠️  Fix agent errors before continuing")
            print("   Check Python version and dependencies")
    
    # Step 3: Create deployment config
    print("\n🎯 Create deployment configuration? (y/n): ", end="")
    if input().lower() == 'y':
        create_deployment_config()
    
    # Step 4: Show checklist
    generate_checklist()
    
    # Step 5: Show next steps
    show_next_steps()
    
    print_header("✅ SETUP COMPLETE!")
    print("""
Your Adaptive Chef project is ready! 🚀

IMMEDIATE NEXT STEPS:
1. Install ADK: pip install google-adk
2. Test agent: python agent.py
3. Create GitHub repo (PUBLIC)
4. Create architecture diagram
5. Record demo video (< 3 min)
6. Submit to Kaggle

DEADLINE: December 1, 2025, 11:59 AM PT

Good luck! You've got this! 🎯

Need help? Check README.md for detailed instructions.
    """)

if __name__ == "__main__":
    main()
