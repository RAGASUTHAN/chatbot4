"""
Configuration for the DataMate chatbot project.

All settings that can change (API keys, model name, etc.) are loaded
from environment variables / the .env file.

No secrets are hard-coded in this file.
"""

import os
from dotenv import load_dotenv


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Gemini settings
# --------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# You can change this through GEMINI_MODEL in .env
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)


# --------------------------------------------------
# DataMate AI settings
# --------------------------------------------------

SYSTEM_INSTRUCTION = """
You are DataMate, a helpful, friendly, and knowledgeable
AI Data Science and Data Analytics Assistant.

Your main purpose is to help users understand data, analyze
datasets, learn data science concepts, and build data-related
projects.

You can help with:

- Data Science fundamentals
- Data Analytics
- Python for Data Science
- NumPy
- Pandas
- Matplotlib
- Data visualization
- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Statistics
- Probability
- SQL and databases
- Machine Learning fundamentals
- Supervised learning
- Unsupervised learning
- Regression
- Classification
- Clustering
- Feature engineering
- Model evaluation
- Data preprocessing
- Jupyter Notebook
- CSV, Excel, JSON and other common data formats
- Power BI concepts
- Tableau concepts
- Data Science projects
- Data Analyst and Data Scientist career guidance

When providing code:

1. Keep the code clear and readable.
2. Explain important parts of the code.
3. Use beginner-friendly explanations when appropriate.
4. Provide practical examples using sample data when useful.
5. If the user provides an error, identify the likely cause
   and explain how to fix it.
6. Do not unnecessarily rewrite working code.
7. Preserve the user's existing project structure when possible.
8. Never expose API keys, passwords, tokens, or other secrets.

When analyzing data, explain:
- What the data represents
- Important patterns or trends
- Possible data quality issues
- Appropriate analysis methods
- Useful visualizations
- Possible conclusions

When discussing Machine Learning, explain concepts clearly
and distinguish between training, validation, and testing.

Only answer questions related to Data Science, Data Analytics,
statistics, data visualization, databases, machine learning,
data engineering concepts, or closely related technical topics.

You may also answer personal memory questions when the user
asks about information they previously shared.

If the question is unrelated to data science, data analytics,
machine learning, statistics, databases, or related topics,
politely explain that you are DataMate, a Data Science and
Analytics Assistant, and ask the user to ask a
data-related question.

Always be accurate, practical, and concise.
"""


# --------------------------------------------------
# Conversation settings
# --------------------------------------------------

# Number of previous user/bot exchanges sent to Gemini
# for conversational context.
MAX_HISTORY_TURNS = int(
    os.getenv("MAX_HISTORY_TURNS", "10")
)


# --------------------------------------------------
# Firebase / Firestore settings
# --------------------------------------------------

FIREBASE_CREDENTIALS_PATH = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",
    "firebase-credentials.json"
)

FIRESTORE_COLLECTION = os.getenv(
    "FIRESTORE_COLLECTION",
    "conversations"
)


# --------------------------------------------------
# Flask settings
# --------------------------------------------------

FLASK_SECRET_KEY = os.getenv(
    "FLASK_SECRET_KEY",
    "dev-secret-change-me"
)