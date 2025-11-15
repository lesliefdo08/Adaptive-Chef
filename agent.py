#!/usr/bin/env python3
"""
The Adaptive Chef - AI-Powered Meal Planning Agent
Capstone Project for Google AI Agents Intensive Course

This agent demonstrates 5 key concepts from the course:
1. Multi-agent system (LoopAgent with specialized sub-agents)
2. Custom tools (pantry management)
3. Long-running operations (Human-in-the-Loop meal approval)
4. Memory Bank (user preferences and history)
5. Sessions & State Management

Architecture:
    User Input → Sequential Agent (Coordinator)
        ├── Preferences Agent (manages dietary restrictions)
        ├── Pantry Agent (tracks ingredients)
        └── Meal Planning Loop Agent
            ├── Planner Agent (generates meal plans)
            ├── Critic Agent (evaluates plans)
            └── Refiner Agent (improves plans)
        → LRO (Human Approval) → Final Meal Plan
"""

import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from google import genai
from google.genai import types
from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.memory_bank import MemoryBank
from google.adk.sessions import InMemorySessionService
from google.adk.lro import LongRunningOperation


# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

# Initialize Gemini client with API key
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
MODEL_NAME = "gemini-2.0-flash-exp"  # Using Gemini for bonus points!


# ============================================================================
# CUSTOM TOOLS - Pantry Management System
# ============================================================================

class PantryManager:
    """
    Custom tool for managing user's pantry inventory.
    Demonstrates custom tool implementation from the course.
    """
    
    def __init__(self):
        self.pantry: Dict[str, Dict[str, Any]] = {}
    
    def add_items(self, items: List[str], quantities: Optional[List[str]] = None) -> str:
        """Add items to pantry inventory"""
        if quantities is None:
            quantities = ["1"] * len(items)
        
        for item, qty in zip(items, quantities):
            self.pantry[item.lower()] = {
                "quantity": qty,
                "added_date": datetime.now().isoformat()
            }
        
        return f"✅ Added {len(items)} items to pantry: {', '.join(items)}"
    
    def remove_items(self, items: List[str]) -> str:
        """Remove items from pantry"""
        removed = []
        for item in items:
            if item.lower() in self.pantry:
                del self.pantry[item.lower()]
                removed.append(item)
        
        if removed:
            return f"✅ Removed from pantry: {', '.join(removed)}"
        return "⚠️ No matching items found in pantry"
    
    def list_items(self) -> str:
        """List all pantry items"""
        if not self.pantry:
            return "🔍 Your pantry is empty"
        
        items_list = "\n".join([
            f"  • {item}: {data['quantity']}" 
            for item, data in self.pantry.items()
        ])
        return f"📦 Your Pantry ({len(self.pantry)} items):\n{items_list}"
    
    def get_available_ingredients(self) -> List[str]:
        """Get list of available ingredients for meal planning"""
        return list(self.pantry.keys())


# Global pantry instance (in production, this would be per-user via sessions)
pantry_manager = PantryManager()


# Tool function declarations for the agent
PANTRY_TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="add_to_pantry",
                description="Add food items to the user's pantry inventory",
                parameters={
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of food items to add"
                        },
                        "quantities": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Quantities for each item (optional)"
                        }
                    },
                    "required": ["items"]
                }
            ),
            types.FunctionDeclaration(
                name="list_pantry",
                description="List all items currently in the pantry",
                parameters={"type": "object", "properties": {}}
            ),
            types.FunctionDeclaration(
                name="remove_from_pantry",
                description="Remove items from the pantry",
                parameters={
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of items to remove"
                        }
                    },
                    "required": ["items"]
                }
            )
        ]
    )
]


def execute_pantry_tool(function_name: str, arguments: Dict[str, Any]) -> str:
    """Execute pantry management functions"""
    if function_name == "add_to_pantry":
        return pantry_manager.add_items(
            arguments.get("items", []),
            arguments.get("quantities")
        )
    elif function_name == "list_pantry":
        return pantry_manager.list_items()
    elif function_name == "remove_from_pantry":
        return pantry_manager.remove_items(arguments.get("items", []))
    else:
        return f"Unknown function: {function_name}"


# ============================================================================
# MEMORY BANK - User Preferences & History
# ============================================================================

class UserPreferencesMemory:
    """
    Memory Bank implementation for storing user preferences and meal history.
    Demonstrates long-term memory concepts from the course.
    """
    
    def __init__(self):
        self.preferences = {
            "dietary_restrictions": [],
            "allergies": [],
            "favorite_cuisines": [],
            "disliked_foods": [],
            "calorie_target": None,
            "meal_history": []
        }
    
    def update_preferences(self, **kwargs) -> str:
        """Update user preferences"""
        updated = []
        for key, value in kwargs.items():
            if key in self.preferences:
                if isinstance(self.preferences[key], list):
                    self.preferences[key].extend(value if isinstance(value, list) else [value])
                else:
                    self.preferences[key] = value
                updated.append(key)
        
        return f"✅ Updated preferences: {', '.join(updated)}"
    
    def get_preferences_context(self) -> str:
        """Get formatted preferences for context injection"""
        prefs = []
        
        if self.preferences["dietary_restrictions"]:
            prefs.append(f"Dietary: {', '.join(self.preferences['dietary_restrictions'])}")
        
        if self.preferences["allergies"]:
            prefs.append(f"Allergies: {', '.join(self.preferences['allergies'])}")
        
        if self.preferences["favorite_cuisines"]:
            prefs.append(f"Likes: {', '.join(self.preferences['favorite_cuisines'])}")
        
        if self.preferences["disliked_foods"]:
            prefs.append(f"Dislikes: {', '.join(self.preferences['disliked_foods'])}")
        
        if not prefs:
            return "No preferences set"
        
        return "👤 User Preferences:\n" + "\n".join(f"  • {p}" for p in prefs)
    
    def add_to_history(self, meal_plan: str):
        """Add meal plan to history"""
        self.preferences["meal_history"].append({
            "date": datetime.now().isoformat(),
            "plan": meal_plan
        })
        
        # Keep only last 10 meal plans
        if len(self.preferences["meal_history"]) > 10:
            self.preferences["meal_history"] = self.preferences["meal_history"][-10:]


# Global memory instance
user_memory = UserPreferencesMemory()


# ============================================================================
# SUB-AGENTS - Specialized Agent Components
# ============================================================================

# 1. PREFERENCES AGENT - Manages user dietary requirements
preferences_agent = LlmAgent(
    model=MODEL_NAME,
    name="PreferencesAgent",
    instruction="""You are a dietary preferences specialist.

Your responsibilities:
- Extract dietary restrictions (vegan, vegetarian, gluten-free, etc.)
- Identify food allergies and intolerances
- Note favorite cuisines and disliked foods
- Store preferences in memory for future meal planning

Always confirm what you've learned and ask clarifying questions if needed.

Format your responses clearly with sections:
✅ Dietary Restrictions: [list]
⚠️ Allergies: [list]
❤️ Preferences: [list]
""",
    client=client
)


# 2. PANTRY AGENT - Manages ingredient inventory
pantry_agent = LlmAgent(
    model=MODEL_NAME,
    name="PantryAgent",
    instruction="""You are a pantry inventory manager.

Your responsibilities:
- Help users add items to their pantry
- Track what ingredients are available
- Remove items as they're used
- Suggest what to buy based on meal plans

Use the pantry tools to manage inventory. Always confirm actions taken.

Be helpful and organized in your responses.
""",
    tools=PANTRY_TOOLS,
    client=client
)


# 3. MEAL PLANNER AGENT - Generates meal plans
planner_agent = LlmAgent(
    model=MODEL_NAME,
    name="MealPlannerAgent",
    instruction="""You are an expert meal planning chef.

Your responsibilities:
- Generate creative, balanced meal plans
- Consider available pantry ingredients
- Respect dietary restrictions and allergies
- Provide recipes with ingredients and instructions
- Estimate calories and prep time

Format meal plans clearly:

DAY 1:
🍳 Breakfast: [Name] (XX min, XXX cal)
   Ingredients: [list]
   Instructions: [brief steps]

🥗 Lunch: [Name] (XX min, XXX cal)
   Ingredients: [list]
   Instructions: [brief steps]

🍽️ Dinner: [Name] (XX min, XXX cal)
   Ingredients: [list]
   Instructions: [brief steps]

Always use available pantry items when possible.
""",
    client=client
)


# 4. CRITIC AGENT - Evaluates meal plans
critic_agent = LlmAgent(
    model=MODEL_NAME,
    name="CriticAgent",
    instruction="""You are a nutrition and meal plan critic.

Your responsibilities:
- Evaluate meal plans for nutritional balance
- Check adherence to dietary restrictions
- Verify use of available pantry ingredients
- Assess variety and practicality
- Identify potential improvements

Provide constructive feedback in this format:

✅ STRENGTHS:
- [positive points]

⚠️ CONCERNS:
- [issues found]

💡 SUGGESTIONS:
- [specific improvements]

VERDICT: [APPROVED / NEEDS REVISION]

Be thorough but constructive.
""",
    client=client
)


# 5. REFINER AGENT - Improves meal plans based on feedback
refiner_agent = LlmAgent(
    model=MODEL_NAME,
    name="RefinerAgent",
    instruction="""You are a meal plan improvement specialist.

Your responsibilities:
- Take original meal plans and critic feedback
- Make specific improvements addressing concerns
- Maintain the good aspects of the original plan
- Ensure all dietary requirements are met

Always explain what changes you made and why.

Keep the same format as the original meal plan.
""",
    client=client
)


# ============================================================================
# LOOP AGENT - Iterative Meal Plan Refinement
# ============================================================================

def meal_planning_loop_condition(state: Dict[str, Any]) -> bool:
    """
    Loop termination condition: stop when plan is approved or max iterations reached.
    This demonstrates the LoopAgent concept from the course.
    """
    # Check if critic approved the plan
    if state.get("critic_verdict") == "APPROVED":
        return False  # Stop loop
    
    # Check iteration count
    if state.get("iteration_count", 0) >= 3:
        return False  # Stop after 3 iterations max
    
    return True  # Continue loop


meal_planning_loop = LoopAgent(
    name="MealPlanningLoop",
    instruction="""You coordinate the meal planning refinement process.

Process:
1. Generate initial meal plan (Planner)
2. Evaluate the plan (Critic)
3. If not approved, refine and repeat
4. If approved or max iterations reached, present final plan

Track iteration count and ensure continuous improvement.
""",
    agents=[planner_agent, critic_agent, refiner_agent],
    condition=meal_planning_loop_condition,
    max_iterations=3
)


# ============================================================================
# LONG-RUNNING OPERATION - Human-in-the-Loop Approval
# ============================================================================

class MealApprovalLRO(LongRunningOperation):
    """
    Long-Running Operation for getting human approval on meal plans.
    Demonstrates LRO and Human-in-the-Loop concepts from the course.
    
    In production, this would integrate with a UI or messaging system
    to pause execution and wait for user approval.
    """
    
    def __init__(self, meal_plan: str):
        super().__init__()
        self.meal_plan = meal_plan
        self.approved = False
        self.feedback = ""
    
    async def execute(self) -> Dict[str, Any]:
        """
        Pause execution and wait for human approval.
        In production, this would send notification and wait for response.
        """
        # For demonstration, we'll simulate approval
        # In real implementation, this would pause and resume based on user input
        
        print("\n" + "="*70)
        print("🔔 MEAL PLAN APPROVAL REQUIRED")
        print("="*70)
        print(self.meal_plan)
        print("="*70)
        print("⏸️  Agent paused, waiting for approval...")
        print("   (In production, user would approve via UI/API)")
        print("="*70)
        
        # Simulate approval (in real app, this waits for actual user input)
        self.approved = True
        self.feedback = "Looks great! Approved."
        
        return {
            "approved": self.approved,
            "feedback": self.feedback,
            "meal_plan": self.meal_plan
        }


# ============================================================================
# ROOT AGENT - Sequential Orchestration
# ============================================================================

root_agent = SequentialAgent(
    name="AdaptiveChefAgent",
    instruction="""You are The Adaptive Chef, an AI meal planning assistant.

You help users:
1. Set dietary preferences and track allergies
2. Manage their pantry inventory
3. Generate personalized meal plans
4. Get cooking instructions and recipes

Process flow:
1. Understand user needs (Preferences Agent)
2. Check pantry inventory (Pantry Agent)
3. Generate and refine meal plans (Loop Agent)
4. Get human approval (LRO)
5. Deliver final meal plan

Always be friendly, clear, and helpful. Explain what you're doing at each step.

Context injection:
- Use user preferences from memory
- Consider available pantry items
- Remember past meal plans to avoid repetition

Welcome users warmly and ask what they need help with!
""",
    agents=[
        preferences_agent,
        pantry_agent,
        meal_planning_loop
    ],
    client=client
)


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

# Initialize session service for state management
session_service = InMemorySessionService()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def inject_context(prompt: str) -> str:
    """
    Inject user preferences and pantry context into prompts.
    Demonstrates context engineering from the course.
    """
    context_parts = [
        user_memory.get_preferences_context(),
        pantry_manager.list_items(),
        f"\n📝 User Request: {prompt}"
    ]
    
    return "\n\n".join(context_parts)


async def process_user_request(user_input: str, session_id: str = "default") -> str:
    """
    Main entry point for processing user requests.
    Handles context injection, agent execution, and LRO coordination.
    """
    
    # Inject context into user input
    contextualized_input = inject_context(user_input)
    
    # Get or create session
    session = session_service.get_or_create_session(session_id)
    
    # Execute agent
    response = await root_agent.execute(
        input_text=contextualized_input,
        session=session
    )
    
    # Check if meal plan was generated (trigger LRO)
    if "meal plan" in user_input.lower() or "generate" in user_input.lower():
        # Create and execute LRO for approval
        lro = MealApprovalLRO(meal_plan=response)
        approval_result = await lro.execute()
        
        if approval_result["approved"]:
            # Add to history
            user_memory.add_to_history(response)
            response += "\n\n✅ Meal plan approved and saved to your history!"
        else:
            response += f"\n\n❌ Meal plan needs revision: {approval_result['feedback']}"
    
    return response


# ============================================================================
# MAIN EXECUTION (for testing)
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                                 ║
║           🍳 THE ADAPTIVE CHEF - AI MEAL PLANNER               ║
║                                                                 ║
║               Powered by Google Gemini & ADK                    ║
║                                                                 ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    async def demo():
        # Demo conversation
        demos = [
            "Hi! I'm vegan and allergic to peanuts.",
            "Add rice, beans, tomatoes, and spinach to my pantry",
            "Create a 3-day meal plan using my pantry items"
        ]
        
        for demo_input in demos:
            print(f"\n👤 User: {demo_input}")
            response = await process_user_request(demo_input)
            print(f"\n🍳 Chef: {response}\n")
            print("-" * 70)
    
    # Run demo
    asyncio.run(demo())
