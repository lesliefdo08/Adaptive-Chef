# Architecture Diagram Placeholder

Create your architecture diagram using one of these tools:

## Recommended Tools:
1. **Draw.io** (https://app.diagrams.net/)
   - Free, web-based
   - Professional templates

2. **Lucidchart** (https://www.lucidchart.com/)
   - Beautiful diagrams
   - Free tier available

3. **Canva** (https://www.canva.com/)
   - Easy drag-and-drop
   - Modern designs

## What to Include:

### Main Components:
```
┌─────────────────────────────────────┐
│         USER INTERFACE              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    ADAPTIVE CHEF ROOT AGENT         │
│      (Sequential Agent)             │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  Context Injection Layer       │ │
│  │  • User Preferences            │ │
│  │  • Pantry Inventory            │ │
│  │  • Meal History                │ │
│  └───────────────────────────────┘ │
└─────┬───────┬────────┬──────────────┘
      │       │        │
      ▼       ▼        ▼
┌──────────┐ ┌──────────┐ ┌─────────────────┐
│Preferences│ │ Pantry   │ │ Meal Planning   │
│  Agent   │ │  Agent   │ │   Loop Agent    │
│          │ │          │ │                 │
│          │ │ Custom   │ │  ┌──────────┐  │
│          │ │ Tools    │ │  │ Planner  │  │
│          │ │          │ │  └────┬─────┘  │
│          │ │          │ │       ▼        │
│          │ │          │ │  ┌──────────┐  │
│          │ │          │ │  │ Critic   │  │
│          │ │          │ │  └────┬─────┘  │
│          │ │          │ │       ▼        │
│          │ │          │ │  ┌──────────┐  │
│          │ │          │ │  │ Refiner  │  │
│          │ │          │ │  └──────────┘  │
└──────────┘ └──────────┘ └────────┬────────┘
                                   │
                                   ▼
                          ┌────────────────┐
                          │  LRO (Human    │
                          │  Approval)     │
                          │  ⏸️ Pause/Resume│
                          └────────┬───────┘
                                   │
                                   ▼
                          ┌────────────────┐
                          │ Final Meal Plan│
                          │ + Save History │
                          └────────────────┘
```

### Supporting Systems:
- Memory Bank (preferences, history)
- Session Service (state management)
- Custom Tools (pantry CRUD)
- Observability (logging, tracing)

## Color Scheme Suggestions:
- **User Interface**: Light Blue (#E3F2FD)
- **Root Agent**: Purple (#9C27B0)
- **Sub-Agents**: Orange (#FF9800)
- **Loop Agent**: Green (#4CAF50)
- **LRO**: Red (#F44336)
- **Memory/Storage**: Gray (#9E9E9E)

## Export:
Save as: `docs/architecture_diagram.png`
Recommended size: 1920x1080 or 1200x800

## Tips:
1. Keep it clean and readable
2. Use arrows to show data flow
3. Label all components clearly
4. Show the 5 key concepts visually:
   - Multi-agent system (multiple boxes)
   - Custom tools (toolkit icon)
   - LRO (pause/play icons)
   - Memory Bank (database icon)
   - Sessions (state management icon)

Once created, update README.md to include:
```markdown
![Architecture Diagram](docs/architecture_diagram.png)
```
