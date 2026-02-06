import os
import re # This is needed for the parsing logic
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def summarize_transcript(transcript_text):
    if not transcript_text:
        return "No transcript found to summarize."

    try:
        # Initialize Groq Client
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

       # Updated to Llama 3.3 70B (Versatile) - High performance and currently active
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional meeting assistant. Summarize the transcript into: 1. Executive Summary, 2. Key Discussion Points, and 3. Action Items."
                },
                {
                    "role": "user", 
                    "content": f"Transcript: {transcript_text}"
                }
            ],
            temperature=0.5,
            max_tokens=1024,
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"Summarization Error: {str(e)}"
    


def extract_action_items(summary_text):
    """
    Parses the summary text to find a section labeled 'Action Items' 
    and returns them as a list of strings.
    """
    if not summary_text:
        return []

    # 1. Look for the "Action Items" section (case-insensitive)
    # This regex looks for 'Action Items' followed by a colon or newline
    match = re.search(r"(?:Action Items|Next Steps):?\s*(.*)", summary_text, re.IGNORECASE | re.DOTALL)
    
    if match:
        items_block = match.group(1).strip()
        
        # 2. Split the block into individual items
        # It looks for new lines starting with -, *, •, or numbers
        items = re.split(r'\n\s*(?:[-*•]|\d+\.)\s*', "\n" + items_block)
        
        # 3. Clean up the list (remove empty entries)
        clean_items = [item.strip() for item in items if item.strip()]
        
        # Limit to the first 10 items to prevent the UI from getting too long
        return clean_items[:10]
    
    return []