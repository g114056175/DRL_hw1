# DRL HW1 — Grid World Policy Evaluation

> **Course**: Deep Reinforcement Learning HW1  
> **Author**: [g114056175](https://github.com/g114056175)

---

## 📌 Overview

An interactive **nxn Grid World** web application built with **Flask**.

| Feature | Description |
|---------|-------------|
| **HW1-1** | Interactive grid map with start / goal / obstacle placement |
| **HW1-2** | Random policy generation + iterative policy evaluation V(s) |

---

## 🚀 Live Demo

> Run locally (see below), or deploy to a cloud platform.

---

## 🖥️ Features

### HW1-1 — Grid Map
- Slider to select **grid size n** (5 ~ 9)
- Click cells to assign roles:
  - 1st click → **Start** (green 🟢)
  - 2nd click → **Goal** (red 🔴)
  - Further clicks → **Obstacles** (gray, max = n−2)
  - Re-clicking a cell removes it
- Visual feedback: dark-theme UI with smooth animations

### HW1-2 — Policy & Value Evaluation
- Press **Generate Policy & Evaluate** to:
  1. Randomly assign ↑ ↓ ← → to every free cell
  2. Run **iterative policy evaluation** (Bellman equation, γ=0.9)
  3. Display arrow + V(s) value on each cell

---

## 🛠️ Installation & Running

```bash
# 1. Clone repo
git clone https://github.com/g114056175/DRL_hw1.git
cd DRL_hw1

# 2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Flask server
python app.py
```

Open your browser at **http://localhost:5000**

---

## 📂 Project Structure

```
DRL_hw1/
├── app.py            # Flask server + API endpoints
├── policy_eval.py    # Policy generation & evaluation algorithm
├── requirements.txt
├── .gitignore
├── README.md
└── templates/
    └── index.html    # Frontend UI (HTML/CSS/JS)
```

---

## 📐 Algorithm

**Policy Evaluation (Bellman Expectation)**

$$V(s) = r + \gamma \cdot V(s')$$

- Reward per step: **−1**
- Goal cell reward: **0** (terminal)
- Obstacles & walls: cannot enter
- Converges when Δ < 1e−6

---

## 📋 Scoring Criteria

| Item | Weight |
|------|--------|
| HW1-1: Grid functionality | 30% |
| HW1-1: UI friendliness | 15% |
| HW1-1: Code quality | 10% |
| HW1-1: Smoothness | 5% |
| HW1-2: Policy display | 20% |
| HW1-2: Evaluation correctness | 15% |
| HW1-2: Code quality | 5% |
