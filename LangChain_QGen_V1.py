
import streamlit as st
from PyPDF2 import PdfReader
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import QAGenerationChain


st.set_page_config(page_title='Ask PDF to generate questions',layout="wide")
st.write("""
    <style>
        footer {visibility: hidden;}
        body {
            font-family: Arial, sans-serif;
        }
    </style>
""", unsafe_allow_html=True)
st.write(f"<h1 style='font-size: 36px; coor: #00555e; font-family: Arial;text-align: center;'>Ask your PDF to generate questions</h1>", unsafe_allow_html=True)
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
file=st.file_uploader("Upload your PDF",type="pdf")

if file is not None:
    pdf_file=PdfReader(file)
    text=""
    for page in pdf_file.pages:
        text+= page.extract_text()
    chain = QAGenerationChain.from_llm(ChatOpenAI(model_name="gpt-3.5-turbo",temperature = 0.3,openai_api_key=OPENAI_API_KEY))
    qa=chain.run(text)
    if qa:
        st.write(f"<h1 style='font-size: 16px; color: #00555e; font-family: Arial;text-align: left;'>Below questions are generated from this file:</h1>", unsafe_allow_html=True)   
        for item in qa:
            question = item["question"]
            st.write(question)



