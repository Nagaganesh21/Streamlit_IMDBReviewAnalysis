import streamlit as st
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from bs4 import BeautifulSoup
import re


# Function to clean text
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

# Load tokenizer
tokenizer = pickle.load(open("IMDBTokenizer.pkl", "rb"))

# Load model
model = load_model('IMDBSentimentAnalysisModel.h5')

#load max_len
max_len = pickle.load(open("max_len.pkl", "rb"))

# Function to predict sentiment
def predict_sentiment(review):
    review = clean_text(review)
    review = tokenizer.texts_to_sequences([review])
    review = pad_sequences(review, maxlen=max_len)
    prediction = model.predict(review)
    return prediction[0][0]

# Streamlit app
def main():
    st.title("Movie Review Sentiment Analysis")
    st.write("This app predicts the sentiment of movie reviews.")

    # Input text area for user to input their review
    review = st.text_area("Enter your movie review here:")

    if st.button("Predict"):
        if review.strip() == "":
            st.error("Please enter a movie review.")
        else:
            sentiment = predict_sentiment(review)
            if sentiment > 0.5:
                st.success("Positive sentiment!")
            else:
                st.error("Negative sentiment!")

if __name__ == "__main__":
    main()
