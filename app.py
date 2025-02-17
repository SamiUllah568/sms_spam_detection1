from flask import Flask, render_template, request
import os
import pandas as pd
import numpy as np
import pickle
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import sklearn
import re

# Download necessary NLTK data
# nltk.download('stopwords')
# nltk.download('punkt')


app = Flask(__name__)

# Load Machine Learning Models
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open("BOW.pkl", 'rb') as file2:
    bow = pickle.load(file2)

with open('encode.pkl', 'rb') as file3:
    encode = pickle.load(file3)

# Initialize Stemmer and Stopwords
stemming = PorterStemmer()
stop_words = set(stopwords.words('english'))


# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')
# Preprocessing Function
def preprocessing_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-z\s]', '', text)  # Remove non-alphabetic characters   
    # Process text with SpaCy
    doc = nlp(text)
    
    # Tokenize, remove stopwords, and lemmatize
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    
    return " ".join(tokens).strip()


@app.route('/', methods=["GET", "POST"])
def index():
    prediction = None  # Default prediction value

    if request.method == "POST":
        sms_text = request.form.get("text_area")  # Get input text
        if sms_text:
            cleaned_text = preprocessing_text(sms_text)  # Preprocess text
            vectorized_text = bow.transform([cleaned_text])  # Convert to BOW features
            prediction = model.predict(vectorized_text)[0] # Predict spam or not spam
            prediction = encode.inverse_transform([prediction])[0]  # Decode label
    
    return render_template('index.html', prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
