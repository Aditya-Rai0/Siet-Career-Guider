SIET Career Guider 🚀
An AI-powered web application designed to provide personalized career guidance. Built with Streamlit, LangChain, and Google's Gemini models, this tool helps users explore career paths, analyze job markets, and create tailored learning roadmaps.

Features ✨
Personalized User Profile: Input your education, experience, and skills to get tailored advice.

Career Discovery: Explore a curated list of careers across Technology, Healthcare, Business, and Creative fields.

Comprehensive AI Analysis: Leverage Google Gemini and real-time web search to generate in-depth reports on any career, covering:

Role Overview & Responsibilities

Required Technical and Soft Skills

Educational Background

Market Analysis: Get insights on job growth projections, salary ranges by experience level, and key industries.

Personalized Learning Roadmap: Receive a step-by-step learning plan based on your experience level.

Industry Insights: Understand the day-to-day work, workplace culture, and career progression paths.

AI Chat Assistant: Ask follow-up questions about the analyzed career with a RAG-powered chatbot that uses the generated report as its knowledge base.

Tech Stack 🛠️
Frontend: Streamlit

AI Framework: LangChain

Language Model (LLM): Google Gemini Pro

Web Search: Google Serper API

Embeddings: Google Generative AI Embeddings

Vector Store: FAISS (for RAG)

Plotting: Plotly

Environment Management: python-dotenv

Setup and Installation
Follow these steps to get the project running on your local machine.

1. Clone the Repository
Bash

git clone https://github.com/your-username/Siet-Career-Guider.git
cd Siet-Career-Guider
2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

Windows:

Bash

python -m venv .venv
.\.venv\Scripts\activate
macOS / Linux:

Bash

python -m venv .venv
source .venv/bin/activate
3. Install Dependencies
Create a file named requirements.txt with the content below, and then run the installation command.

requirements.txt:

streamlit
pandas
numpy
plotly
langchain
langchain-google-genai
langchain-community
faiss-cpu
python-dotenv
Installation Command:

Bash

pip install -r requirements.txt
Configuration
This application requires API keys to function. The keys are managed securely using a .env file.

1. Create the .env File
Create a file named .env in the root directory of the project.

2. Add Your API Keys
Open the .env file and add your secret keys.

Code snippet

# .env file
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
GOOGLE_SERPER_API_KEY="YOUR_GOOGLE_SERPER_API_KEY_HERE"
3. Secure Your Keys
IMPORTANT: Add the .env file to your .gitignore file to ensure you never accidentally commit your secret keys to GitHub.

.gitignore:

.env
.venv/
__pycache__/
Usage
Once the setup and configuration are complete, run the Streamlit application with the following command:

Bash

streamlit run app.py
Open your web browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).

Project Structure
Siet-Career-Guider/
├── .venv/
├── .gitignore
├── app.py                  # Main Streamlit application file
├── career_guidance_system.py # Backend logic for analysis
├── career_chatbot.py       # RAG chatbot logic and UI
├── requirements.txt        # Project dependencies
├── .env                    # Secret API keys (DO NOT COMMIT)
└── README.md               # This file
License
This project is licensed under the MIT License. See the LICENSE file for details.
