import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import datetime

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


def generate_booking_summary(bookings: list) -> str:
    """
    Uses GPT to summarize a user's bookings.
    'bookings' is a list of dictionaries.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OPENAI_API_KEY not set."

    # Convert datetime objects to strings for the AI
    # and determine if they are 'upcoming' or 'past'
    today = datetime.datetime.utcnow()
    formatted_bookings = []
    for booking in bookings:
        booking_time = booking['event']['date_time']
        status = "upcoming" if booking_time > today else "past"
        formatted_bookings.append({
            "event_title": booking['event']['title'],
            "event_date": booking_time.strftime('%B %d, %Y'),
            "seats": booking['number_of_seats'],
            "status": status
        })

    if not formatted_bookings:
        return "You have no bookings to summarize."

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly dashboard assistant for 'EventEase'. "
                        "A user has requested a summary of their bookings. "
                        "You will receive a JSON list of their bookings. "
                        "Summarize them in a friendly, concise paragraph. "
                        "Clearly distinguish between 'upcoming' and 'past' events. "
                        "Today's date is " + today.strftime('%B %d, %Y')
                    )
                },
                {
                    "role": "user",
                    "content": f"Here are my bookings: {json.dumps(formatted_bookings)}"
                }
            ]
        )
        summary = completion.choices[0].message.content
        return summary.strip()

    except Exception as e:
        return f"Error from AI service: {str(e)}"

def get_event_chat_response(query: str, events: list) -> str:
    """
    Uses GPT to answer a user's question based on a list of events.
    'events' is a list of event dictionaries.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OPENAI_API_KEY not set."

    # Format the event data for the AI
    formatted_events = []
    for event in events:
        formatted_events.append({
            "title": event['title'],
            "description": event['description'],
            "location": event['location'],
            "date_time": event['date_time'].strftime('%B %d, %Y at %I:%M %p'),
            "available_seats": event['available_seats']
        })
    
    system_prompt = (
        "You are a helpful chat assistant for an event booking site called 'EventEase'. "
        "You will answer user questions about available events. "
        "Your knowledge is strictly limited to the following list of events. "
        "Do not make up events or answer questions about other topics. "
        "If the answer is not in the list, politely say you don't have that information. "
        "Today's date is " + datetime.datetime.now(datetime.timezone.utc).strftime('%B %d, %Y') +
        "\n\n--- AVAILABLE EVENTS ---\n" +
        json.dumps(formatted_events)
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        response = completion.choices[0].message.content
        return response.strip()

    except Exception as e:
        return f"Error from AI service: {str(e)}"