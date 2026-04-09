# 🌍 Reality Simulator Engine

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18.x-blue.svg)
![Groq](https://img.shields.io/badge/Groq-AI_Integration-orange.svg)

**Reality Simulator Engine** is an advanced, multi-agent AI simulation environment powered by **Groq**. It features a robust Python/FastAPI backend simulating complex emergent behaviors—including economic models, agent relationships, and dynamic memory reflection—visualized in real-time through a beautiful, glassmorphism React dashboard.

## ✨ Features

- **🧠 Groq AI Hybrid Architecture**: Day-to-day actions rely on highly optimized algorithms, while critical events (crises, traumas, deep reflections) seamlessly escalate to an LLM for complex decision-making.
- **💼 Dynamic Economy System**: Agents interact with a fluctuating job market, variable inflation rates, and dynamically priced basic/luxury goods.
- **🤝 Relationship Networks**: Advanced graph tracking of friendships, rivalries, and compatibility across varied personality archetypes.
- **💭 Long-Term Memory & Goals**: Agents record critical life events, reflect on their past, and dynamically update their overarching life goals based on LLM abstractions.
- **⚡ Real-Time Telemetry Dashboard**: A stunning, lightweight React/Vite dashboard leveraging FastAPI streams for real-time surveillance of the world ledger.
- **🚀 Ultra-Optimized**: Smart backend throttling reduces expensive API calls by up to 95%, seamlessly running local logic for most ticks.

## 🏗️ Architecture

```text
reality-simulator/
├── backend/                  # Python & FastAPI Engine Core
│   ├── api/                  # REST server endpoints & routers
│   ├── simulation/           # Tick loop & Global World/Time variables
│   ├── agents/               # Entity data models & execution routing
│   ├── decisions/            # Hybrid Action-Scoring system (Groq/Math)
│   ├── economy/              # Fiscal and Inflation logic
│   └── memory/               # Short/Long term event and bond storage
└── frontend/                 # React GUI & Real-Time Dashboard
    ├── src/components/       # UI Components (Glassmorphism layout)
    └── src/api.js            # Axios/Fetch backend integrations
```

## 🚀 Getting Started

### Prerequisites
- NodeJS (v18+)
- Python (3.9+)
- A Groq API Key (Free tier works perfectly)

### 1. Backend Setup

1. Open a terminal and navigate to the `backend` directory.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your environment variables:
   - Make sure you have a `.env` file containing your key (copy `.env.example` if it doesn't exist).
   - Expected structure: `GROQ_API_KEY=your_key_here`
4. Start the engine server:
   ```bash
   python main.py --server
   ```
   *The simulation will begin ticking and broadcasting to `localhost:8000`.*

### 2. Frontend Setup

1. Open a **second terminal** and navigate to the `frontend` directory.
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. 🎉 Open your browser to `http://localhost:5173` to view your world!

## 🛠️ Configuration
You can tweak the simulation laws of physics in `backend/config.py`:
- `tick_delay_seconds`: Speed up or slow down time.
- `initial_agents`: Modify the starting population size.
- `use_groq`: Toggle the LLM logic on or off entirely.

## 🤝 Contributing
Pull requests are welcome! If you want to add new LLM models, expand agent behaviors, or improve the React dashboard, feel free to submit an issue or PR.

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
