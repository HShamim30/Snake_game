# 🐍 Snake Game using Python (Pygame)

## 📌 Project Title
Snake Game – Data Structure Mini Project

---

## 📝 Description
This project is a classic Snake Game developed using **Python** and the **Pygame** library.
The game demonstrates the practical use of **data structures**, real-time game logic,
event handling, and file handling to store the high score.

The player controls the snake using keyboard arrow keys.
The objective is to eat food, increase the score, and avoid collisions with the wall
or the snake’s own body.

---

## 🧠 Data Structure Concepts Used
- **List**: To store snake body segments
- **Queue (FIFO behavior)**: Snake movement logic
- **Loops & Conditions**: Game flow control
- **File Handling**: Saving and loading high score

---

## 🎯 Objectives
- To develop a real-time game using Python
- To apply data structure concepts in a practical project
- To understand collision detection and event handling
- To store and retrieve game data (high score)

---

## 🛠️ Technologies Used
- Python 3.12
- Pygame Library
- PyInstaller (for creating EXE file)

---

## 🎮 Game Features
- Smooth snake movement
- Random food generation
- Score and high score display
- Sound effects on food eat and game over
- Game Over screen

---

## 📂 Project Structure
SNAKE_GAME_DSA/
│
├── Snake_game.py # Main game source code
├── eat.wav # Sound when snake eats food
├── gameover.wav # Sound on game over
├── highscore.txt # File to store high score
├── README.md # Project documentation
└── dist/
└── Snake_game.exe # Executable game file

yaml
Copy code

---

## ▶️ How to Install and Run the Game

### 🔹 Method 1: Run Using Python (Developer Mode)

#### Step 1: Install Python
Download and install **Python 3.12** from:
https://www.python.org/downloads/

✔️ Make sure **Add Python to PATH** is selected during installation.

#### Step 2: Install Pygame
Open Command Prompt or VS Code Terminal and run:
```bash
python -m pip install pygame
Step 3: Run the Game
bash
Copy code
python Snake_game.py
🔹 Method 2: Run Using EXE File (No Python Required)
✔️ Python installation is NOT required
✔️ Suitable for end users and college submission

Steps:
Open the project folder

Navigate to the dist folder

Double-click on:

Copy code
Snake_game.exe
🎉 The game will start automatically.

🎮 Game Controls
⬆️ Arrow Up – Move Up

⬇️ Arrow Down – Move Down

⬅️ Arrow Left – Move Left

➡️ Arrow Right – Move Right

📍 EXE File Location
Copy code
dist/Snake_game.exe
🧪 Output
Snake grows after eating food

Score increases continuously

High score is saved even after restarting the game

Game ends when snake hits the wall or itself
