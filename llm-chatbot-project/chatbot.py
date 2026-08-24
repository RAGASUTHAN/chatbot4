"""
DataMate chatbot logic: talks to the Gemini API.

This file handles:
- Gemini API communication
- Data Science / Data Analytics domain validation
- Conversation history

This file does not know about Flask or Firebase.
It simply receives a message and optional history,
then returns a text response.
"""

from google import genai
from google.genai import types

import config


# --------------------------------------------------
# Gemini API validation
# --------------------------------------------------

if not config.GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it to your .env file, e.g.\n"
        "GEMINI_API_KEY=your_key_here"
    )


# One shared Gemini client for the whole application
client = genai.Client(
    api_key=config.GEMINI_API_KEY
)


# --------------------------------------------------
# Data Science / Analytics keywords
# --------------------------------------------------

DATA_KEYWORDS = [

    # General Data Science
    "data science",
    "data science project",
    "data analytics",
    "data analysis",
    "data analyst",
    "data scientist",
    "dataset",
    "data set",
    "data mining",
    "big data",

    # Python Data Science
    "python for data science",
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "scipy",
    "jupyter",
    "jupyter notebook",
    "google colab",

    # Data Processing
    "data cleaning",
    "data preprocessing",
    "data preparation",
    "data transformation",
    "missing values",
    "outlier",
    "outliers",
    "feature engineering",
    "normalization",
    "standardization",
    "encoding",

    # Exploratory Data Analysis
    "eda",
    "exploratory data analysis",
    "data exploration",
    "correlation",
    "covariance",
    "data profiling",

    # Statistics
    "statistics",
    "statistical analysis",
    "mean",
    "median",
    "mode",
    "variance",
    "standard deviation",
    "probability",
    "distribution",
    "normal distribution",
    "hypothesis testing",
    "p value",
    "confidence interval",
    "regression analysis",

    # Data Visualization
    "data visualization",
    "visualization",
    "chart",
    "graph",
    "plot",
    "histogram",
    "bar chart",
    "line chart",
    "scatter plot",
    "box plot",
    "heatmap",
    "dashboard",

    # SQL / Databases
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "database",
    "dbms",
    "query",
    "sql query",
    "joins",
    "group by",
    "aggregate",
    "aggregation",

    # Machine Learning
    "machine learning",
    "ml",
    "supervised learning",
    "unsupervised learning",
    "semi supervised learning",
    "reinforcement learning",
    "regression",
    "classification",
    "clustering",
    "decision tree",
    "random forest",
    "linear regression",
    "logistic regression",
    "knn",
    "k nearest neighbors",
    "support vector machine",
    "svm",
    "naive bayes",
    "k means",
    "neural network",

    # ML concepts
    "training data",
    "test data",
    "validation data",
    "train test split",
    "model training",
    "model evaluation",
    "accuracy",
    "precision",
    "recall",
    "f1 score",
    "confusion matrix",
    "overfitting",
    "underfitting",
    "cross validation",
    "hyperparameter",

    # Deep Learning / AI data topics
    "deep learning",
    "tensorflow",
    "pytorch",
    "keras",
    "cnn",
    "rnn",
    "transformer",

    # File formats
    "csv",
    "excel",
    "xlsx",
    "xls",
    "json",
    "parquet",

    # BI tools
    "power bi",
    "powerbi",
    "tableau",
    "looker",
    "business intelligence",
    "bi",

    # Data Engineering related
    "data engineering",
    "data pipeline",
    "etl",
    "elt",
    "data warehouse",
    "data lake",
    "apache spark",
    "spark",
    "hadoop",

    # Data career
    "data analyst career",
    "data scientist career",
    "data science career",
    "data analyst roadmap",
    "data science roadmap",
    "data science interview",
    "data analyst interview",
]


# --------------------------------------------------
# Personal memory patterns
# --------------------------------------------------

PERSONAL_MEMORY_PATTERNS = [
    "what is my name",
    "what's my name",
    "do you know my name",
    "do you remember my name",
    "remember my name",
    "my name is",
    "who am i",
    "what do you know about me",
    "do you remember me",
]


def is_personal_memory_question(message):
    """
    Check whether the user is asking about
    personal information or saved memory.
    """

    message_lower = message.lower().strip()

    return any(
        pattern in message_lower
        for pattern in PERSONAL_MEMORY_PATTERNS
    )


def is_data_related(message):
    """
    Check whether the user's message is related
    to Data Science, Data Analytics, Statistics,
    Machine Learning, or related data topics.
    """

    message_lower = message.lower().strip()

    return any(
        keyword in message_lower
        for keyword in DATA_KEYWORDS
    )


# --------------------------------------------------
# DataMate chatbot
# --------------------------------------------------

class Chatbot:
    """
    Wraps the Gemini API and provides a simple
    interface for DataMate.
    """

    def get_response(self, message, history=None):
        """
        Generate a DataMate response.

        Parameters:
            message:
                New user message.

            history:
                Optional list of previous conversations.

        Expected history format:

            {
                "user_message": "...",
                "bot_reply": "..."
            }
        """

        # --------------------------------------------------
        # Domain protection
        # --------------------------------------------------

        if (
            not is_data_related(message)
            and not is_personal_memory_question(message)
        ):
            return (
                "📊 I'm DataMate, your Data Science & "
                "Analytics Assistant.\n\n"
                "I specialize in Data Science, Data Analytics, "
                "Python for Data Science, Pandas, NumPy, SQL, "
                "Statistics, Data Visualization, Machine Learning, "
                "and related data topics.\n\n"
                "Please ask me a data-related question! 📈"
            )

        # --------------------------------------------------
        # Build conversation history
        # --------------------------------------------------

        contents = []

        if history:

            for turn in history[-config.MAX_HISTORY_TURNS:]:

                user_message = turn.get(
                    "user_message",
                    ""
                )

                bot_reply = turn.get(
                    "bot_reply",
                    ""
                )

                if user_message:

                    contents.append(
                        types.Content(
                            role="user",
                            parts=[
                                types.Part(
                                    text=user_message
                                )
                            ],
                        )
                    )

                if bot_reply:

                    contents.append(
                        types.Content(
                            role="model",
                            parts=[
                                types.Part(
                                    text=bot_reply
                                )
                            ],
                        )
                    )

        # --------------------------------------------------
        # Add current user message
        # --------------------------------------------------

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=message
                    )
                ],
            )
        )

        # --------------------------------------------------
        # Call Gemini
        # --------------------------------------------------

        try:

            response = client.models.generate_content(
                model=config.MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=config.SYSTEM_INSTRUCTION,
                ),
            )

            if not response or not response.text:
                return (
                    "⚠️ Sorry, I couldn't generate a response. "
                    "Please try again."
                )

            return response.text

        except Exception as e:

            print(
                f"[Gemini] API call failed: {e}"
            )

            raise


# --------------------------------------------------
# Simple CLI testing
# --------------------------------------------------

if __name__ == "__main__":

    bot = Chatbot()

    chat_history = []

    print("DataMate ready 📊")
    print("Type 'quit' to exit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "quit":
            break

        reply = bot.get_response(
            user_input,
            chat_history
        )

        print(f"DataMate: {reply}")

        chat_history.append(
            {
                "user_message": user_input,
                "bot_reply": reply
            }
        )