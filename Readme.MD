<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
</head>
<body>
  <h1>🚀 Naukri AI Helper</h1>
  <p>
    This project automates interactions with the <b>Naukri chatbot</b> using
    <b>Selenium</b> and integrates with <b>Ollama</b> for AI-powered responses.
    It also includes a job search & auto-apply feature.
  </p>

  <h2>📂 Project Structure</h2>
  <pre>
  .
  ├── ai_helper.py        # Functions for AI integration (Ollama, prompt handling)
  ├── selenium_helper.py  # Selenium helpers for interacting with chatbot
  ├── user_profile.py     # User profile & configuration
  ├── main.py             # Entry point to run the Naukri chatbot automation
  ├── search_apply.py     # Script to search & apply for jobs (by keyword & experience)
  ├── requirements.txt    # Python dependencies
  └── README.md           # Setup & usage guide
  </pre>

  <h2>🛠️ Setup Instructions</h2>

  <h3>1. Clone the Repository</h3>
  <pre>
  git clone https://github.com/udaysk3/Job-Apply-Automation.git
  cd Job-Apply-Automation
  </pre>

  <h3>2. Create & Activate Virtual Environment</h3>
  <b>Linux / macOS:</b>
  <pre>
  python3 -m venv venv
  source venv/bin/activate
  </pre>
  <b>Windows (PowerShell):</b>
  <pre>
  python -m venv venv
  venv\Scripts\activate
  </pre>

  <h3>3. Install Dependencies</h3>
  <pre>
  pip install -r requirements.txt
  </pre>

  <h3>4. Install Ollama</h3>
  <p>Ollama is required to run local AI models.</p>

  <b>macOS (Homebrew):</b>
  <pre>brew install ollama/tap/ollama</pre>

  <b>Linux:</b>
  <pre>curl -fsSL https://ollama.com/install.sh | sh</pre>

  <b>Windows:</b>
  <p>
    Download and install from 👉
    <a href="https://ollama.com/download" target="_blank">Ollama for Windows</a>
  </p>

  <h3>5. Install ChromeDriver</h3>
  <p>Selenium requires <b>Google Chrome</b> and the matching <b>ChromeDriver</b>.</p>
  <ul>
    <li>🔗 <a href="https://googlechromelabs.github.io/chrome-for-testing/#stable" target="_blank">Download ChromeDriver</a> (official site)</li>
    <li>🔗 <a href="https://chromedriver.chromium.org/downloads" target="_blank">Alternative ChromeDriver Downloads</a></li>
  </ul>
  <p>
    Make sure the ChromeDriver version matches your installed Chrome browser.  
    Once downloaded, extract it and update the path in
    <code>selenium_helper.py</code>:
  </p>
  <pre>
  # selenium_helper.py (line 15)
  from selenium.webdriver.chrome.service import Service
  service = Service(r"C:\chromedriver-win64\chromedriver.exe")  # 🔑 update path
  </pre>
  <p>
    Replace <code>C:\chromedriver-win64\chromedriver.exe</code> with the actual
    path where you saved ChromeDriver on your system.
  </p>

  <h3>6. Pull the Required AI Model</h3>
  <p>Example: pulling <b>Llama 3.1</b></p>
  <pre>ollama pull llama3.1</pre>
  <p>You can also try other supported models (e.g., <code>mistral</code>, <code>gemma</code>, etc.).</p>

  <h3>7. Run the Chatbot Automation</h3>
  <pre>python main.py</pre>

  <h3>8. Run the Job Search & Apply Script</h3>
  <p>
    The <code>search_apply.py</code> script allows you to search and auto-apply
    for jobs on Naukri based on keywords and experience.
  </p>
  <pre>
  python search_apply.py 
  </pre>

  <h2>⚙️ Configuration</h2>
  <ul>
    <li>Update <b>user_profile.py</b> with your personal details (username, password, skills, experience, preferences, etc.).</li>
    <li>Adjust <b>ai_helper.py</b> rules and prompts if you want the AI to respond differently.</li>
    <li>Update <b>selenium_helper.py</b> if the chatbot’s HTML changes.</li>
    <li>Update <b>search_apply.py</b> to customize job application filters.</li>
  </ul>

  <h2>✅ Example Workflow</h2>
  <ol>
    <li>Launches <b>Naukri chatbot</b> in Selenium.</li>
    <li>Waits for new chatbot questions.</li>
    <li>Uses <b>Ollama AI</b> to generate answers.</li>
    <li>Submits responses automatically.</li>
    <li>Optionally, <b>search_apply.py</b> searches & applies for jobs.</li>
  </ol>

  <h2>📌 Requirements</h2>
  <ul>
    <li>Python <b>3.9+</b></li>
    <li>Google Chrome + ChromeDriver (for Selenium)</li>
    <li>Ollama installed locally with at least one AI model pulled</li>
  </ul>

  <h2>🤝 Contributing</h2>
  <p>
    Pull requests are welcome. For major changes, please open an issue first to
    discuss what you’d like to change.
  </p>
</body>
</html>
