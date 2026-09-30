# Arm Wrestle Showdown Lab

This project is a tug-of-war button mashing game using **Pygame**. It introduces students to vector interpolation, resource/stamina management, alternating key-stroke detection, and simple AI pressure modeling inside an object-oriented codebase.

---

## What's Provided

A working Arm Wrestling game with:

- An arm wrestling table arena rendering procedural arms, elbows, shoulders, and clasping hands
- An alternating input mechanism requiring rhythmic pressing of Left and Right arrow keys
- A stamina bar that depletes during rapid pressing and recovers naturally over time
- Continuous computer AI force pushing toward the player's side
- Win/loss boundary detection and a post-game rematch screen

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Rapidly alternate Left Arrow and Right Arrow to push, R to restart after a match.   


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the inverted arm push bug

To win the match, the player needs to pull arm_position toward negative values (<= -self.target_limit). In the current build, when the player alternates Left and Right arrow keys, the input handler adds +4.2 to self.arm_position instead of subtracting it. This helps the computer pin the player instead of resisting. Correct the sign operation so player inputs push the arm toward the player's winning threshold.

### Task 2: Implement dynamic AI surge / difficulty spikes

Currently, the AI applies force at a constant average rate using static math (self.ai_strength * ai_variance). Implement an AI stamina or surge mechanism in game_engine.update() where the computer builds up energy, periodically triggers a "power surge" with increased force for 1–2 seconds, and then enters an exhausted state with reduced resistance, creating a dynamic back-and-forth rhythm.

### Task 3: Implement an exhaustion warning indicator

When the player drops below 10 stamina, button inputs are disabled until stamina regenerates. However, there is no immediate visual cue explaining why inputs stopped working. Add visual feedback—such as flashing the stamina bar red, displaying an "EXHAUSTED!" label, or causing the player's arm to tremble—whenever stamina is below the usable threshold of 10.

### Task 4: Implement an exhaustion warning indicator

When the player drops below 10 stamina, button inputs are disabled until stamina regenerates. However, there is no immediate visual cue explaining why inputs stopped working. Add visual feedback—such as flashing the stamina bar red, displaying an "EXHAUSTED!" label, or causing the player's arm to tremble—whenever stamina is below the usable threshold of 10.

---

## Expected Behavior

- Rapidly alternating between Left Arrow and Right Arrow pulls the hands toward the player's side.
- Rapid pushing drains stamina; falling below 10 stamina temporarily halts input until it recovers.
- Reaching -100.0 awards victory to the player, while reaching +100.0 triggers a computer win.
- Pressing R on the Game Over screen resets stamina, arm position, and game states for a rematch.
---

## Folder Structure

```
arm_wrestle/
├── game/
│   └── game_engine.py
├── main.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
