# Demo Video Script

**Duration:** 2:58  
**Target Audience:** Kaggle judges & AI enthusiasts  
**Objective:** Showcase technical excellence & real-world value

---

## 🎬 Video Structure

### Opening (00:00 - 00:30) - THE PROBLEM

**Visual:** Screen recording with voiceover

**Script:**
```
"Hi, I'm [Your Name], and I'm solving a problem that affects millions 
of people every day: meal planning.

The average person spends 2-3 hours every week figuring out what to 
cook, checking what's in their pantry, and worrying about dietary 
restrictions.

30% of groceries go unused, costing families $1,500 per year in food 
waste. And let's be honest - we've all stared into the fridge at 6 PM 
asking 'What's for dinner?'

This is where The Adaptive Chef comes in."
```

**Visual Elements:**
- Stock footage of frustrated person looking at fridge
- Infographic: "$1,500/year wasted"
- Timer showing "2-3 hours weekly"

---

### Why Agents? (00:30 - 01:00)

**Visual:** Architecture diagram animation

**Script:**
```
"Traditional meal planning apps just give you static recipes. But The 
Adaptive Chef uses AI agents that LEARN, ADAPT, and REFINE.

Here's the architecture:

A sequential agent coordinates three specialized sub-agents:
1. Preferences Agent - learns your dietary restrictions
2. Pantry Agent - tracks what you actually have
3. Loop Agent - this is the magic...

The Loop Agent uses THREE agents working together:
- A Planner generates meal plans
- A Critic evaluates them for nutrition and preferences
- A Refiner improves them based on feedback

Just like a professional chef would refine a recipe, our agents 
iterate until the plan is perfect."
```

**Visual Elements:**
- Animated architecture diagram
- Highlight each agent as mentioned
- Show Loop Agent iteration (Plan → Critique → Refine)

---

### Live Demo (01:00 - 02:30) - THE STAR OF THE SHOW

**Visual:** Screen recording of terminal/UI

**Script:**
```
"Let me show you it in action.

First, I'll set my preferences:
[Type] 'I'm vegan and allergic to peanuts'

The agent confirms and stores this in its Memory Bank.

Now let's add some pantry items:
[Type] 'Add rice, black beans, tomatoes, and spinach to my pantry'

Great! Now for the exciting part - generating a meal plan:
[Type] 'Create a 3-day meal plan using my pantry items'

Watch what happens:

The Planner generates an initial plan...
The Critic evaluates it - checking for allergens, nutrition, variety...
The Refiner makes improvements...

And here's something special - the Long-Running Operation!

The agent PAUSES execution and requests human approval.
[Show pause icon/message]

In a production app, you'd get a notification on your phone. 
I can review the plan, request changes, or approve it.

Let's approve it.
[Click/type approval]

The agent resumes and delivers the final meal plan!

Look at this - detailed recipes, prep times, calorie counts, and 
it's all using ingredients I already have. No more food waste!"
```

**Visual Elements:**
- Split screen: terminal on left, diagram on right
- Highlight each step in the architecture as it executes
- Zoom in on the LRO pause screen (BIG MOMENT!)
- Show final meal plan clearly

**Critical: SHOW THE LRO PAUSE - This demonstrates Human-in-the-Loop!**

---

### Technical Highlights (02:30 - 02:58)

**Visual:** Code snippets & GitHub repo

**Script:**
```
"So what makes this capstone-worthy?

The Adaptive Chef demonstrates 5 key concepts from the course:

1. Multi-agent system with Loop Agent for iterative refinement
2. Custom tools for pantry management
3. Long-running operations for human approval
4. Memory Bank for preferences and history
5. Session management for multi-user support

It's built with Google's Agent Development Kit and powered by 
Gemini 2.0 Flash.

The code is fully open source on GitHub, with comprehensive 
documentation, evaluation tests, and deployment configs.

And best of all? It solves a real problem that saves people time, 
money, and reduces food waste.

Thanks for watching! Check out the GitHub repo for all the code, 
and let me know what you'd cook with this!"
```

**Visual Elements:**
- Quick code snippets showing:
  - LoopAgent definition
  - Custom tool implementation
  - LRO class
  - Memory Bank usage
- GitHub repo overview
- Evaluation test results
- Architecture diagram one more time

**Ending Frame:**
```
THE ADAPTIVE CHEF
AI-Powered Meal Planning

GitHub: github.com/YOUR_USERNAME/adaptive-chef
Built for: Google AI Agents Capstone 2025

Powered by Gemini 2.0 & Google ADK
```

---

## 🎥 Recording Tips

### Tools
1. **Screen Recording:**
   - Windows: OBS Studio (free)
   - Mac: QuickTime or ScreenFlow
   - Resolution: 1920x1080 minimum

2. **Video Editing:**
   - DaVinci Resolve (free)
   - Camtasia (paid)
   - CapCut (mobile-friendly)

3. **Voiceover:**
   - Use good microphone (or phone in quiet room)
   - Clear, enthusiastic delivery
   - Speak slightly slower than normal

### Best Practices

✅ **Do:**
- Practice script 3-4 times before recording
- Use clear, simple language
- Show actual code execution (not fake/static)
- Emphasize the LRO pause moment
- Keep energy high!
- Add background music (low volume)
- Use smooth transitions

❌ **Don't:**
- Rush through technical parts
- Use technical jargon without explanation
- Have messy/cluttered screens
- Include long loading times (edit them out)
- Forget to show your face (optional but adds personality)

### Timing Breakdown

| Section | Duration | Content Type |
|---------|----------|--------------|
| Intro | 30s | Voiceover + B-roll |
| Architecture | 30s | Diagram animation |
| Demo | 90s | Screen recording |
| Tech | 28s | Code + repo |

**Total: 2:58** (allows 2s buffer)

---

## 📤 Upload & Submission

### YouTube Upload
1. Upload as "Unlisted" (not Private, not Public)
2. Title: "The Adaptive Chef - AI Meal Planning Agent | Google Capstone 2025"
3. Description:
```
The Adaptive Chef is an AI-powered meal planning agent built for 
the Google AI Agents Intensive Capstone Project.

Features:
- Multi-agent system with Loop Agent
- Custom pantry management tools
- Long-running operations for approval
- Memory Bank for user preferences
- Powered by Gemini 2.0

GitHub: [your-link]
Capstone: kaggle.com/competitions/[link]

Built with Google's Agent Development Kit (ADK)
```

4. Tags: AI, Agents, Google, Gemini, Meal Planning, ADK, Kaggle, Capstone
5. Thumbnail: Create custom thumbnail with logo + "The Adaptive Chef"

### Add to README
```markdown
🎥 **[Watch Demo Video](https://youtu.be/YOUR_VIDEO_ID)** _(2:58)_
```

### Kaggle Submission
- Add YouTube URL to "Media Gallery" section
- Reference video in project description
- Ensure video is accessible (Unlisted, not Private!)

---

## ✅ Pre-Upload Checklist

- [ ] Video under 3 minutes
- [ ] Clear audio (no background noise)
- [ ] Shows LRO pause/resume flow
- [ ] All 5 key concepts mentioned
- [ ] Live demo (not static screenshots)
- [ ] GitHub link visible at end
- [ ] YouTube set to "Unlisted"
- [ ] Link added to README
- [ ] Tested link works in incognito mode

---

Good luck with your recording! Remember: enthusiasm and clarity matter more than perfection. Show your passion for the project! 🎬🚀
