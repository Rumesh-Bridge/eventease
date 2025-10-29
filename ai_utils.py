import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_event_description(prompt: str) -> str:
    """
    Uses GPT to expand a short prompt into a full event description.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OPENAI_API_KEY not set. Please add it to your .env file."

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use a fast and cost-effective model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional event coordinator. "
                        "A user will provide a brief note, and you will "
                        "expand it into an exciting, professional event description "
                        "of about 2-3 sentences. Focus on attracting attendees."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        description = completion.choices[0].message.content
        return description.strip()
        
    except Exception as e:
        # Handle potential API errors
        return f"Error from AI service: {str(e)}"