# YouTube Search Application

This Streamlit application leverages OpenAI's powerful language models, alongside LangChain's integration tools, to provide a custom interface for searching YouTube videos. With plans for enhancing research capabilities in future versions, this application stands as a starting point for academic and exploratory search endeavors on YouTube without relying on its heavily rate-limited API.

## Features

- **YouTube Search:** Utilizes a custom YouTube search tool to query videos without the YouTube API.
- **Streamlit Interface:** Offers a user-friendly interface powered by Streamlit for interaction with the application.
- **Future Research Integration:** Plans to incorporate research functionalities, making it a powerful tool for academic and exploratory purposes.


## Getting Started

To run this application, you'll need Python installed on your system, alongside Streamlit and other dependencies specified in the project's `requirements.txt` file.

### Installation

1. Clone the repository to your local machine:
2. Install the required Python packages (it's recommended to use a virtual environment):

### Running the Application

Open your terminal, navigate to the project directory, and execute:
```bash
streamlit run app.py
```


### Usage
Upon launching the application, you'll be greeted by the Streamlit interface. Follow these steps to search for YouTube videos:

Enter your OpenAI API key: Use the sidebar to input your OpenAI API key securely.
Search Query: In the chat input box, type your search query or question related to YouTube videos and press enter.
View Results: The application will process your query and display the search results as messages in the chat interface.