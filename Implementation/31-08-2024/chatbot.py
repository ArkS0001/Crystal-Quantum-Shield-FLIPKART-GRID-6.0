import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
import io

# Load the pre-trained T5 model and tokenizer
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Function to generate responses with T5
def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Function to process CSV
def process_csv(file):
    df = pd.read_csv(io.StringIO(file.getvalue().decode('utf-8')))
    summary = df.describe(include='all').to_string()
    return summary

# Streamlit App
st.title("Chatbot with T5 and CSV Analysis")

# User input for chatbot
user_input = st.text_area("Enter your message:")

# File uploader for CSV
csv_file = st.file_uploader("Upload a CSV file", type="csv")

if st.button("Send"):
    if csv_file:
        csv_summary = process_csv(csv_file)
        st.write("CSV Analysis:")
        st.text(csv_summary)
    if user_input:
        response = generate_response(user_input)
        st.write("T5 Response:")
        st.text(response)
    else:
        st.write("Please enter a message or upload a CSV file.")
