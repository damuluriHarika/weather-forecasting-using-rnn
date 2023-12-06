import streamlit as st
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Function to identify synonyms for a word
def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

# Function to detect and correct ambiguities in text
def detect_and_correct_ambiguities(text):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Part-of-speech tagging
    pos_tags = nltk.pos_tag(tokens)

    corrected_text = []

    for token, pos in pos_tags:
        # Check if the word has multiple senses (ambiguous)
        if len(wordnet.synsets(token)) > 1:
            # Get synonyms for the word
            synonyms = get_synonyms(token)

            # Find the most common synonym based on frequency
            most_common_synonym = max(set(synonyms), key=synonyms.count)

            # Use the most common synonym as the replacement
            corrected_text.append(most_common_synonym)
        else:
            corrected_text.append(token)

    # Reconstruct the corrected text
    corrected_text = ' '.join(corrected_text)

    return corrected_text

# Streamlit app
st.title("Text Ambiguity Correction")

# Input text box
input_text = st.text_area("Enter a text with ambiguities", "")

# Change the button color to orange using CSS
button_css = """
    <style>
    div.stButton > button {
        background-color: orange;
        color: white;
    }
    </style>
"""
st.markdown(button_css, unsafe_allow_html=True)

if st.button("Correct Ambiguities"):
    # Detect and correct ambiguities
    corrected_text = detect_and_correct_ambiguities(input_text)

    # Display the original and corrected text
    st.subheader("Original Text:")
    st.write(input_text)
    st.subheader("Corrected Text:")
    st.write(corrected_text)