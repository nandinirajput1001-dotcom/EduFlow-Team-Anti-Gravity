🎓 EduFlow AI - Smart Student Onboarding Platform
Hackathon Prototype | Track: EdTech / AI Automation
EduFlow AI is an intelligent, full-stack onboarding platform designed to streamline the chaotic admission-to-activation journey for universities. It bridges the gap between students and administration using real-time tracking, risk analytics, and an AI-powered assistant.
🔐 Quick Demo Credentials
You can use these pre-configured accounts to test the platform immediately:
Role
Email
Password
Student
student@eduflow.edu
password
Admin
admin@eduflow.edu
adminpass2024

💡 Note: You can also use the "Sign Up" button on the login page to create a fresh Student account and test the onboarding flow from scratch.
🚀 Key Features
👨‍🎓 For Students
Smart Dashboard: Visual tracking of onboarding progress and health score.
Interactive Checklist: Step-by-step guidance (Fees, Documents, LMS).
Document Vault: Secure upload interface for identity and academic proofs.
EduFlow AI Bot: Context-aware chatbot for instant queries (Fees, Hostel, Docs).
👮‍♂️ For Admins
Command Center: Real-time overview of total students, pending verifications, and at-risk candidates.
Verification Queue: One-click Approve/Reject workflow for uploaded documents.
AI Risk Analytics: Auto-detects students falling behind (<40% progress) to prevent dropouts.
Bottleneck Analysis: Visual insights into where students are getting stuck (e.g., Fees vs. Docs).
🛠️ Tech Stack
Frontend: HTML5, Tailwind CSS (CDN), Vanilla JavaScript (ES6+), Lucide Icons.
Backend: Python (Flask).
Database: SQLite3 (Lightweight & Serverless).
AI/Logic: Python-based Heuristics for Health Scores & Rule-based Chatbot.
📂 Project Structure
eduflow-onboarding/
│
├── server/
│   ├── app.py              # Main Flask Application (Routes & Logic)
│   ├── init_db.py          # Database Initialization Script
│   ├── schema.sql          # Database Schema & Seed Data
│   ├── requirements.txt    # Python Dependencies
│   └── templates/
│       └── index.html      # Single-Page Frontend Application
│
└── README.md               # Project Documentation


⚡ Getting Started (Local Setup)
Follow these steps to run the project locally.
Prerequisites
Python 3.x installed.
Git installed.
1. Clone the Repository
git clone [https://github.com/your-username/eduflow-ai.git](https://github.com/your-username/eduflow-ai.git)
cd eduflow-ai


2. Backend Setup
Navigate to the server folder and install dependencies.
cd server
pip install -r requirements.txt


3. Initialize Database
Run this script once to create the SQLite database and seed demo users.
python init_db.py



4. Run the Application
Start the Flask server.
python app.py


5. Access the Platform
Open your browser and visit:
👉 https://www.google.com/search?q=http://127.0.0.1:5000
🧠 AI Logic & Heuristics
Health Score Algorithm: * Base Score: 100
Penalty: -20 if progress < 30%.
Penalty: -15 if "Fee Payment" task is pending.
Risk Analysis (Admin):
Students are flagged as HIGH RISK if their onboarding progress is below 40%.
Chatbot:
Uses keyword mapping to provide instant context-specific answers regarding university processes.
🔮 Future Roadmap
OCR Integration: Auto-extract details from uploaded Aadhaar/Marksheets.
LLM Integration: Replace rule-based bot with Gemini/OpenAI API for conversational guidance.
Email Notifications: Automated reminders for pending deadlines.

