import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_feedback(feedback_list, analysis_focus):
    feedback_list = [str(feedback).strip() for feedback in feedback_list if str(feedback).strip()]

    if not feedback_list:
        return "No valid feedback provided for analysis."

    if analysis_focus == 'Sentiment Analysis':
        prompt = (
            "Analyze the following customer feedback for sentiment (Positive, Neutral, Negative):\n"
        )
    elif analysis_focus == 'Theme Identification':
        prompt = (
            "Analyze the following customer feedback and identify key themes (e.g., pricing, service, product quality):\n"
        )
    elif analysis_focus == 'Improvement Suggestions':
        prompt = (
            "Analyze the following customer feedback and suggest improvements based on the feedback provided:\n"
        )
    elif analysis_focus == 'All of the Above':
        prompt = (
            "Analyze the following customer feedback and provide:\n"
            "1. Overall sentiment (Positive, Neutral, Negative).\n"
            "2. Key themes (e.g., pricing, service, product quality).\n"
            "3. Suggested improvements to address concerns.\n\n"
        )
    else:
        return "Invalid analysis focus selected."

    prompt += "\n".join(feedback_list)


    model = genai.GenerativeModel("gemini-2.0-flash-exp")#select Modles based on your intrest 
    response = model.generate_content(prompt)

    return response.text.strip()