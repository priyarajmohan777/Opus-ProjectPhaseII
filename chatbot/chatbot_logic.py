"""
Chatbot Logic - Groq API Integration for Career Guidance
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Groq model to use (fast and high quality)
MODEL = "llama-3.3-70b-versatile"  # Best balance of speed and quality

def get_career_guidance(user_message, context):
    """
    Get AI-powered career guidance using Groq API
    
    Args:
        user_message: The user's question
        context: Formatted context from prediction module
    
    Returns:
        AI response as string
    """
    
    # System prompt for career-focused assistant
    system_prompt = f"""You are OPUS Career Assistant, an AI career guidance expert specializing in personalized career advice.

🎯 YOUR ROLE:
- Provide career guidance based on the user's predicted career and skill assessment
- Answer questions about skill gaps, learning paths, and career development
- Suggest specific, actionable steps and resources
- Be encouraging but realistic
- Keep responses concise (2-4 paragraphs max)

⚠️  IMPORTANT RULES:
- ONLY answer career-related questions (career advice, skills, learning, job market, resume tips)
- If asked about unrelated topics (weather, cooking, general knowledge, etc.), politely redirect: 
  "I'm specialized in career guidance. Please ask me about your career path, skills, or professional development!"
- Reference the user's specific situation when relevant
- Suggest concrete resources (online courses, certifications, projects)

{context}"""

    try:
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model=MODEL,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )
        
        # Extract response
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        error_msg = str(e)
        
        # Handle common errors
        if "api_key" in error_msg.lower():
            return "⚠️ API key error. Please check your GROQ_API_KEY in the .env file."
        elif "rate_limit" in error_msg.lower():
            return "⚠️ Rate limit exceeded. Please wait a moment and try again."
        elif "timeout" in error_msg.lower():
            return "⏱️ Request timed out. Please try again."
        else:
            return f"❌ Error: {error_msg}"


def test_groq_connection():
    """Test if Groq API is configured correctly"""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello"}],
            model=MODEL,
            max_tokens=10
        )
        return True, "Groq API connected successfully!"
    except Exception as e:
        return False, f"Groq API error: {str(e)}"