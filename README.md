# General Project Overview
# Welcome to the SuperDataScience Community Project!
Welcome to the AI Travel Companion repository! 🎉

This project is a collaborative initiative brought to you by SuperDataScience, a thriving community dedicated to advancing the fields of data science, machine learning, and AI. We are excited to have you join us in this journey of learning, experimentation, and growth.

# Project Scope of Works:

## Project Overview

This project involves creating an advanced AI-powered travel companion that leverages retrieval-augmented generation (RAG) to provide personalized travel assistance. The project will gather the latest ticket price data from airlines through web scraping, integrate this data with a knowledge base, and deploy the final application on Hugging Face Spaces. The AI Travel Companion will offer users dynamic ticket pricing, travel recommendations, and query-based assistance.

## Objectives

### Data Collection and Storage:
- Gather data on popular travel destinations via web scraping.
- Store the data in a structured database optimized for quick retrieval.

### AI Travel Companion Development:
- Develop a RAG pipeline that combines a travel destinations knowledge base with generative AI.
- Implement functionality to answer user queries and provide personalized travel suggestions based on travel data and other contextual inputs.

### Application Deployment:
- Build an intuitive user interface for the travel companion.
- Deploy the application on Hugging Face Spaces for global accessibility.

## Technical Requirements

### Tools and Libraries:
- **Data Collection:** BeautifulSoup, Selenium, requests.
- **Data Storage:** csv, json or vector database.
- **AI Development:** LangChain, Hugging Face Transformers, OpenAI API, Pinecone/FAISS/ChromaDB for vector search.
- **Application Deployment:** Gradio or Streamlit for user interface development; Hugging Face Spaces for hosting.

### Environment:
- Python 3.8+
- Required Libraries: pandas, langchain, transformers, gradio, openai, beautifulsoup4, selenium.

# Specific content for Gustavo Murad project

## Solution Overview
- This is a prototype of a travel assistant model
- It takes inputs form a user who types a free text with his/her travel wishes
- The UI is a basic HTML interface, and comunicates with the Flask LLM model running in Python
- The whole project was executed for google colab using T4GPU given the demanding processing on LLM Mystral
- The model generate travel alternatiecs based on user inputs
- following the travel proposals, the model goes to Amadeus APIs to gather hotel and flight information
- Google maps API also used to help with getting hotel address using coordinates present in Amadeus database

## Packages, Files used

- Transformers, Hugging face, flask, ngrok, Amadeus, Google
- CSV , JSON files to help with city/IATA data cleaning
- Index HTL: user input
- Results.HTML: present results on model processing
- Selecionar_Cidade.HTML : UI to handle origin city if first insertion in INdex.HTML not gets through
