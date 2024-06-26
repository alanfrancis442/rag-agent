# Rag Agent

This RAG LLM App leverages advanced retrieval-augmented generation technology to provide precise and comprehensive answers by accessing multiple sources. With seamless integration to Google Drive,
web search, and YouTube search, the app retrieves the most relevant data to augment its responses, ensuring you get the most accurate and contextually rich information. Whether you need documents from your drive,
the latest web insights, or informative videos, this app has you covered. Experience the next level of AI-powered information retrieval and knowledge generation.

![Screenshot 2024-06-26 182916](https://github.com/alanfrancis442/rag-agent/assets/119670162/70849016-94f9-4f43-adba-4d671a6f95c6)

# Project Demo


https://github.com/alanfrancis442/rag-agent/assets/119670162/55fc20c8-1b8e-46d1-a89e-3de59b48cef9



# Project Architecture


![Screenshot 2024-06-26 195828](https://github.com/alanfrancis442/rag-agent/assets/119670162/080ea4bc-add7-4104-a15b-650f7f36da3d)


# How to Set It Up

1. Install the required packages
    ```shell
    pip intall requirements.txt
    ```

2. Install Ollama
[Download](https://ollama.com/download)

3. Pull the model
   The llms used in this projects are Phi 3 Mini and nomic
    ```shell
    ollama pull [llm name]
    ```

4. Setup GoogleDrive
  [Google Drive Guid](https://pathway.com/developers/user-guide/connect/connectors/gdrive-connector#setting-up-google-drive)

6. Create a text file called note.txt
    ```shell
    touch note.txt
    ```

# How to Run It
  For Windows
  ```shell
  python main.py

  ```

  For Linux
  ```shell
  python3 main.py
  ```
