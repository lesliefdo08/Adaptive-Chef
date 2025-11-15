#!/usr/bin/env python3
"""
Interactive Chat with The Adaptive Chef
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Simple chat interface
print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                                 ║
║           🍳 THE ADAPTIVE CHEF - INTERACTIVE CHAT              ║
║                                                                 ║
║               AI-Powered Meal Planning Assistant                ║
║                                                                 ║
╚═══════════════════════════════════════════════════════════════╝

Welcome! I'm The Adaptive Chef, your AI meal planning assistant.

I can help you:
• Set dietary preferences and track allergies
• Manage your pantry inventory
• Generate personalized meal plans
• Get cooking instructions and recipes

Type 'quit' or 'exit' to end the conversation.

""")

# Initialize Gemini client
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# Simple memory storage
user_preferences = {
    "dietary_restrictions": [],
    "allergies": [],
    "pantry": {}
}

# System prompt
SYSTEM_PROMPT = """You are The Adaptive Chef, an AI meal planning assistant.

You help users:
1. Set dietary preferences (vegan, vegetarian, gluten-free, etc.)
2. Track food allergies
3. Manage pantry inventory
4. Generate personalized meal plans
5. Provide cooking instructions

Current user context:
- Dietary restrictions: {dietary_restrictions}
- Allergies: {allergies}
- Pantry items: {pantry}

Be friendly, helpful, and conversational. When generating meal plans:
- Consider dietary restrictions and allergies
- Use available pantry items when possible
- Include prep time and basic calorie estimates
- Provide clear, step-by-step instructions

Format meal plans nicely with emojis (🍳 🥗 🍽️) for readability.
"""

def chat():
    """Main chat loop"""
    
    # Conversation history
    history = []
    
    while True:
        # Get user input
        try:
            user_input = input("\n👤 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Thanks for chatting! Happy cooking!")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n👋 Thanks for chatting! Happy cooking!")
            break
        
        # Update memory based on input (simple keyword matching)
        if any(word in user_input.lower() for word in ['vegan', 'vegetarian', 'gluten-free', 'dairy-free', 'keto']):
            for diet in ['vegan', 'vegetarian', 'gluten-free', 'dairy-free', 'keto']:
                if diet in user_input.lower() and diet not in user_preferences["dietary_restrictions"]:
                    user_preferences["dietary_restrictions"].append(diet)
        
        if 'allergic' in user_input.lower() or 'allergy' in user_input.lower():
            # Simple extraction - in production would use NLP
            words = user_input.lower().split()
            for i, word in enumerate(words):
                if word in ['allergic', 'allergy'] and i + 2 < len(words):
                    allergen = words[i + 2].strip('.,!?')
                    if allergen not in user_preferences["allergies"]:
                        user_preferences["allergies"].append(allergen)
        
        if 'add' in user_input.lower() and 'pantry' in user_input.lower():
            # Extract items
            words = user_input.replace(',', ' ').split()
            for word in words:
                cleaned = word.strip('.,!?')
                if len(cleaned) > 3 and cleaned.lower() not in ['pantry', 'items', 'please', 'could', 'would', 'add']:
                    user_preferences["pantry"][cleaned.lower()] = "1"
        
        # Build context
        context = SYSTEM_PROMPT.format(
            dietary_restrictions=", ".join(user_preferences["dietary_restrictions"]) or "None",
            allergies=", ".join(user_preferences["allergies"]) or "None",
            pantry=", ".join(user_preferences["pantry"].keys()) or "Empty"
        )
        
        try:
            # Generate response
            print("\n🍳 Chef: ", end="", flush=True)
            
            # Build full prompt with context
            full_prompt = f"{context}\n\nConversation:\n"
            for msg in history[-6:]:
                full_prompt += f"{msg}\n"
            full_prompt += f"User: {user_input}\nAssistant:"
            
            # Generate response
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                )
            )
            
            # Print response
            print(response.text)
            
            # Add to history
            history.append(f"User: {user_input}")
            history.append(f"Assistant: {response.text}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Please try again or rephrase your question.")

if __name__ == "__main__":
    chat()
