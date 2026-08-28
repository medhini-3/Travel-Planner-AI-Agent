Website Link : https://travel-planner-ai-agent-6bem.onrender.com/
# 🌍 AI Travel Agent

[![CI/CD Pipeline](https://github.com/YOUR-USERNAME/Travel-Planner-AI-Agent/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR-USERNAME/Travel-Planner-AI-Agent/actions)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Available_Here-blue?style=for-the-badge)](https://travel-planner-ai-agent-6bem.onrender.com)

An intelligent, full-stack travel planning application built with **FastAPI** and the **Google GenAI SDK**. This application leverages the `gemini-3.5-flash-lite` model to generate highly personalized, multi-day itineraries streamed in real-time to a modern, glassmorphism UI.

## ✨ Features

* **Real-Time Streaming:** Implements HTTP chunked transfer encoding (`StreamingResponse`) via FastAPI to stream text directly to the UI, bypassing traditional LLM latency wait-times.
* **Modern Frontend:** A fully responsive, glassmorphism UI built with **Tailwind CSS**, animated background effects, and vanilla asynchronous JavaScript (`TextDecoder` & `ReadableStream`).
* **Robust Backend Routing:** Utilizes absolute path resolution to reliably serve static assets across different Linux container environments.
* **Automated Testing Suite:** Comprehensive integration tests using `pytest` and `unittest.mock` to intercept the Google GenAI SDK, ensuring API reliability without hitting live external network limits.
* **CI/CD Pipeline:** Fully automated GitHub Actions workflow that runs the test suite on every code push, ensuring code quality before deployment.
* **Cloud Deployment:** Containerized and hosted live on Render.

## 🚀 Tech Stack

**Backend:**
* Python 3.11+
* FastAPI (Async API framework)
* Uvicorn (ASGI web server)
* Google GenAI SDK (`google-genai`)
* Pydantic (Data validation)

**Frontend:**
* HTML5 / Vanilla JS
* Tailwind CSS (Styling & Animations)
* Marked.js (Markdown parsing)
* FontAwesome (Icons)

**DevOps & QA:**
* Pytest (Automated testing & mocking)
* GitHub Actions (Continuous Integration)
* Render (Production Deployment)

## ⚙️ Local Setup & Installation

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR-USERNAME/Travel-Planner-AI-Agent.git](https://github.com/YOUR-USERNAME/Travel-Planner-AI-Agent.git)
cd Travel-Planner-AI-Agent
2. Set up the virtual environment
Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add your Google Gemini API key:

Plaintext
GEMINI_API_KEY=your_actual_api_key_here
5. Run the Application
Start the FastAPI server locally:

Bash
uvicorn main:app --reload
Navigate to http://127.0.0.1:8000 in your browser to view the application.

🧪 Testing
This project uses pytest for automated integration testing. The tests utilize unittest.mock to intercept the send_message_stream method of the Google GenAI SDK, simulating streaming responses to validate API contracts and parsing logic without making live network calls.

To run the test suite locally:

Bash
pytest -v
🏗️ Project Structure
Plaintext
├── main.py                  # FastAPI application instance and static mounts
├── routers/
│   └── trip_router.py       # API routing and streaming generator logic
├── static/
│   └── index.html           # Frontend UI (Tailwind, Glassmorphism, JS Streams)
├── tests/
│   └── test_integration.py  # Pytest suite with SDK mocking
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (Git-ignored)
└── .gitignore               # Ignored files and directories
📝 License
Distributed under the MIT License.


Remember to replace `YOUR-USERNAME` in the two badge URLs at the very top with your actual GitHub username. 

Are you planning to add this repository link directly to your resume, or are you prepari
