# Personalized Study Podcast Generator

## Overview

This project aims to create a multimodal AI agent that transforms user-provided study materials (PDFs, text documents) into engaging audio podcasts. The podcast will feature two distinct voices discussing and explaining the content, making study more accessible and versatile.

This agent is designed for a B2C audience, focusing on ease of use and practical learning benefits.

## Features

-   Accepts PDF and plain text files as input.
-   Processes input materials to extract key information.
-   Generates a podcast script with a dialogue between two distinct voices.
-   Converts the script into an audio file (e.g., MP3).
-   Allows users to save and listen to their personalized study podcasts.

## Architecture

The agent is built using Python and the Flask web framework. It operates based on an **Orchestrator-workers** model:

1.  **Flask App (`app.py`) - Orchestrator:** Manages user interactions (file uploads), orchestrates the workflow, and serves the generated podcast.
2.  **File Parser (`core/file_parser.py`) - Worker:** Responsible for reading and extracting text content from uploaded files (PDF, TXT).
3.  **Content Processor (`core/content_processor.py`) - Worker:** Analyzes the extracted text, identifies key concepts, and structures the information. This stage is ideal for incorporating an LLM to summarize, simplify, or identify discussion points from the text.
4.  **Podcast Script Generator (`core/podcast_generator.py`) - Worker:** Creates a dialogue script for two distinct voices based on the processed content. An LLM could also be used here to make the dialogue more natural and engaging.
5.  **TTS Handler (`core/tts_handler.py`) - Worker:** Uses Text-to-Speech (TTS) technology (currently gTTS) to convert the generated script into an audio file. For true distinct voices, this module would need enhancement with more advanced TTS or by combining audio segments from different voice configurations.
6.  **Main Orchestrator (`app.py`):** Ties all components together, manages the user interaction flow via web routes, and handles input/output operations.

### Data Flow (Web App)

1.  User uploads a study material file via the web interface.
2.  Flask app (`app.py`) receives the file.
3.  `File Parser` worker extracts text.
4.  `Content Processor` worker analyzes text and prepares structured content.
5.  `Podcast Generator` worker creates a two-voice script.
6.  `TTS Handler` worker converts the script to an audio file.
7.  The Flask app serves the audio file and script to the user on a results page.

## Anthropic's Principles Integration

This project is designed with Anthropic's principles of Helpfulness, Honesty, and Harmlessness (HHH) in mind:

-   **Helpful:** The agent aims to provide genuine assistance in learning by transforming dense text into an easy-to-consume audio format. The explanations will be clear and focused on the core material.
-   **Honest:** The podcast content will be derived strictly from the user-provided materials. The agent will not introduce external information or misrepresent the source.
-   **Harmless:** The agent will avoid generating biased, inappropriate, or misleading content. It will process data responsibly.

*(Specific implementation details reflecting these principles will be documented as development progresses.)*

## Agent Recipe Integration

This project implements the **Orchestrator-workers** recipe from `agentrecipes.com`.

-   **Orchestrator:** The Flask application (`app.py`) acts as the central orchestrator. It receives user input (file uploads), initiates the processing pipeline, and coordinates the different worker modules.
-   **Workers:**
    -   `core/file_parser.py`: Worker responsible for text extraction.
    -   `core/content_processor.py`: Worker for analyzing and structuring content. This is a prime candidate for an LLM to act as a specialized worker for understanding and summarizing the material.
    -   `core/podcast_generator.py`: Worker for generating the dialogue script. This could also involve an LLM to create more natural and engaging conversational flow between the two voices.
    -   `core/tts_handler.py`: Worker for converting text to speech.

The orchestrator (`app.py`) calls these workers sequentially, passing the output of one as the input to the next, which also incorporates elements of **Prompt Chaining**. This modular design allows for clear separation of concerns and makes it easier to upgrade or replace individual worker components (e.g., swapping out a basic text processor for a sophisticated LLM, or changing the TTS engine).

## Getting Started

### Prerequisites

-   Python 3.x
-   Flask
-   PyPDF2
-   gTTS
-   pydub
-   (Ensure all dependencies from `requirements.txt` are installed)

### Installation

1.  Clone the repository (or create the project structure).
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  The necessary directories (`input_materials`, `output_podcasts`, `templates`, `static`, `core`) will be created automatically by the scripts or should be present from the project setup.

### Usage

Run the Flask application:
```bash
python app.py
```
Then, open your web browser and navigate to `http://127.0.0.1:5000/`.

The script will prompt you for the path to your study material.

## Future Enhancements

-   Support for more input formats (e.g., DOCX, web URLs).
-   User interface (Web UI or Desktop GUI).
-   Customizable voice options.
-   Advanced summarization and topic extraction.
-   Interactive elements (e.g., Q&A generation). 