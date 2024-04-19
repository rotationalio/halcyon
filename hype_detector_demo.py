import pickle
import streamlit as st

from halcyon.hype_detector import HypeDetector

st.title("Hype Detector: spot promotional and hyped content online")

# Load the model from disk
with open("models/hype_detector.pkl", "rb") as f:
    model = pickle.load(f)

# Initialize the HypeDetector scorer
scorer = HypeDetector(model)

# Get user input
text = st.text_area("Enter some text")
button = st.button("Score")

# Score the text
if button:
    scores = scorer.score(text)
    st.write(scores)
