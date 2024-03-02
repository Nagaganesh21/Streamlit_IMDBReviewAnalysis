from bs4 import BeautifulSoup
import re

def clean_text(text):
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    # Get text without HTML tags
    clean_text = soup.get_text()

    # Convert text to lowercase
    clean_text = clean_text.lower()

    # Remove mentions and hashtags
    clean_text = re.sub(r'@\w+|#\w+', ' ', clean_text)

    # Remove URLs
    clean_text = re.sub(r'http?:\S+|https?:\S+', ' ', clean_text)

    # Remove non-alphabetic characters except whitespace
    clean_text = re.sub('[^a-zA-Z\s]', ' ', clean_text)

    # Replace multiple whitespaces with a single whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # Remove leading and trailing whitespaces
    clean_text = clean_text.strip()

    return clean_text
