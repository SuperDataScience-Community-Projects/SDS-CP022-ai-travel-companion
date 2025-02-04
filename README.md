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

## Scope 1: (Beginner Friendly)

### Phase 1: Setup (1 Week)
- Setup of GitHub repo and project folders
- Setup of virtual environments and installation of libraries

### Phase 2: Application Logic Development (2 Weeks)
- Choose the LLM you want to use (Either a frontier model or a model from huggingface)
- Integrate it with Tavily to enhance user queries with real-time data
- Model output should be a complete itinerary for the users travel destinations


### Phase 3: Application UI Development (1 Week)
- Build a web UI to interact with the model (Streamlit, Gradio, etc.)

### Phase 4: Deployment (1 Week)
- Deploy application to the cloud (Streamlit, Gradio, etc.)

### Timeline

| Phase          | Task                                 | Duration |
|----------------|--------------------------------------|----------|
| Phase 1: Setup  | Setup of GitHub Repo & environment | Week 1   |
| Phase 2: Data  | Application Logic Dev | Week 2 & 3  |
| Phase 3: RAG   | Application UI Dev                  | Week 4   |
| Phase 4: Deployment | Deploy on Hugging Face Spaces     | Week 5   |

## Scope 1: (Advaced)

### Phase 1: Setup (1 Week)
- Setup of GitHub repo and project folders
- Setup of virtual environments and installation of libraries

### Phase 2: Application Logic Development (2 Weeks)
- What agents will we need?
  - Grab flight data and summarize the best dates to book the cheapest tickets
  - Grab 3 popular destinations for that country
  - Grab weather results for each destination
  - Optimize days to stay and travel time between each city
  - Grab the best hotels to stay in for each city
  - Summarize all details into a complete itinerary.

### Phase 3: Application UI Development (1 Week)
- Build a web UI to interact with the model (Streamlit, Gradio, etc.)

### Phase 4: Deployment (1 Week)
- Deploy application to the cloud (Streamlit, Gradio, etc.)

### Timeline

| Phase          | Task                                 | Duration |
|----------------|--------------------------------------|----------|
| Phase 1: Setup  | Setup of GitHub Repo & environment | Week 1   |
| Phase 2: Data  | Application Logic Dev | Week 2 & 3  |
| Phase 3: RAG   | Application UI Dev                  | Week 4   |
| Phase 4: Deployment | Deploy on Hugging Face Spaces     | Week 5   |

# Getting Started

Follow these steps to set up the project locally:

## 1. Fork the Repository
To work on your own copy of this project:
1. Navigate to the SDS GitHub repository for this project.  
2. Click the **Fork** button in the top-right corner of the repository page.  
3. This will create a copy of the repository under your GitHub account.

---

## 2. Clone the Repository
After forking the repository:
1. Open a terminal on your local machine.  
2. Clone your forked repository by running:
   ```bash
   git clone https://github.com/<your-username>/<repository-name>.git
   ```
3. Navigate to the project directory:
    ```bash
    cd <repository-name>
    ```

## 3. Create a virtual environment
Setup a virtual environment to isolate project dependancies
1. Run the following command in the terminal to create a virtual environment
    ```bash
    python3 -m venv .venv
    ```
2. Activate the virtual environment
  - On a mac/linux:
    ```bash
    source .venv/bin/activate
    ```
  - On a windows:
    ```
    .venv\Scripts\activate
    ```
3. Verify the virtual environment is active (the shell prompt should show (.venv))

## 4. Install dependancies
Install the required libraries for the project
1. Run the following command in the terminal to isntall dependancies from the requirements.txt file:
    ```bash
    pip install -r requirements.txt
    ```
Once the setup is complete, you can proceed with building your project
