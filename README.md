# HODL Project — RAG/Deep Learning Repo

This repository creates a retrieval-augmented workflow (LangChain + Weaviate) for a student Q&A chatbot for the Hands on Deep Learning (15.773) class at MIT. It includes the generation of a Gradio UI for quick interaction.


## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
```

## Usage
- **Serve the UI** (default if no args):
  ```bash
  python main.py --serve
  ```
- **Index texts via CLI**:
  ```bash
  python main.py --index "Doc one" "Doc two" --serve
  ```

Open your browser at the URL printed by Gradio.
