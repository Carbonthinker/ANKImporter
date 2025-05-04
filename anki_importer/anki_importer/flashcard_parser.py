import re

def extract_flashcards(text):
    """
    Extract flashcards from text in the format:
    Question: [question]
    Answer: [answer]
    
    Args:
        text (str): The text containing flashcards
        
    Returns:
        list: List of tuples (question, answer)
    """
    return re.findall(r"Question:\s*(.*?)\s*Answer:\s*(.*?)(?:\n|$)", text, re.DOTALL) 