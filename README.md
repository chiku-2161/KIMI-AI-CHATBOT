🤖 KIMI-AI-CHATBOTKIMI is a high-performance Python-based AI Desktop Assistant powered by Google’s Gemini API. It bridges the gap between LLM intelligence and local system automation, handling everything from email management to complex system tasks through a sleek web interface.⚡ Key FeaturesGemini-Powered Intelligence: Leverages advanced LLM capabilities for natural language understanding and generation.System Automation: Control local system tasks and file management via voice or text commands.Communication Hub: Seamlessly manages emails and calendar events.Hybrid Interface: Dual-mode execution via main.py (CLI/Desktop) and server.py (Web Dashboard).Async Processing: Built for speed and responsiveness.📊 System WorkflowBelow is the logic flow of how KIMI processes your requests:Code snippetgraph TD
    A[User Input: Text/Voice] --> B{Interface Type}
    B -->|CLI/Main| C[main.py Logic]
    B -->|Web Dashboard| D[server.py / Flask]
    C --> E[Gemini API Engine]
    D --> E
    E --> F{Task Classification}
    F -->|Query| G[Information Retrieval]
    F -->|Action| H[System/API Execution]
    G --> I[User Response]
    H --> I
🚀 Getting Started1. PrerequisitesPython 3.10+Google Gemini API Key2. InstallationClone the repository and install the dependencies:Bashgit clone https://github.com/chiku-2161/KIMI-AI-CHATBOT.git
cd KIMI-AI-CHATBOT
pip install -r requirements.txt
3. ConfigurationCreate a .env file in the root directory and add your API key:Code snippetGEMINI_API_KEY=your_api_key_here
4. Running the AssistantTo start the web server:Bashpython server.py
To run the desktop version:Bashpython main.py
🛠 Tech StackComponentTechnologyLanguagePythonAI EngineGoogle Gemini APIWeb FrameworkFlask (Templates included)EnvironmentProcfile (Heroku ready)📂 Project Structuremain.py: Core logic for desktop operations.server.py: Handles web-based requests and UI rendering.templates/: HTML/CSS files for the web interface.requirements.txt: List of necessary Python packages.[!IMPORTANT]Ensure you do not commit your .env file to public repositories to protect your API credentials.
