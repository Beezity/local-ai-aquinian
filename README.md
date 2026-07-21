# BeeAI

Why BeeAI? 'Cuz I'm Beezity

A local retrieval-augmented AI assistant powered by Ollama and custom document indexing. Mainly intended for writing with specific parameters.

Fully offline once set up properly with model and knowledge.

(liam here, i will likely use this and if i do, then the prompt and response will be documented)

---

## Prerequisites

Before getting started, ensure you have the following installed:

* **Python 3.10+**
* **[Ollama](https://ollama.com/)**
* **Git**

---

## Installation

### 1. Clone the Repository
Open your terminal or command prompt, clone the repository, and navigate into the project directory:

```bash
git clone https://github.com/Beezity/local-ai-aquinian.git
cd local-ai-aquinian
```

### 2. Set Up a Virtual Environment
Create and activate an isolated Python environment:

* **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

* **Windows (PowerShell / Command Prompt):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
  *(If using Git Bash on Windows, run `source venv/Scripts/activate` instead.)*

### 3. Install Dependencies
Upgrade `pip` and install the required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Windows Users (PyTorch Fix):** If you experience issues installing or running PyTorch, install the CPU-only version with:
> ```bash
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> ```

---

## Ollama Setup

1. **Start the Ollama Server**  
   Open a **new** terminal window and run:
   ```bash
   ollama serve
   ```
   > **Note:** Keep this terminal window open and running in the background.

2. **Pull a Model**  
   In your primary terminal window, download the recommended model (or another model of your choice):
   ```bash
   ollama pull qwen-3:8b
   ```

---

## Usage

### 1. Prepare Your Knowledge Base
Place any reference files (handbooks, manuals, test documents, etc.) into the `knowledge/` directory.  
*Subfolders within `knowledge/` are fully supported.*

### 2. Index Documents
Run the indexing script to parse your documents for the AI:

```bash
python index.py
```

### 3. Start Chatting
Launch the interactive terminal chat:

```bash
python chat.py
```
Type your prompt, press **Enter**, and the AI will reference your indexed files to generate a response.
