# HODL Project — RAG/Deep Learning Repo

This repository reorganizes a Colab notebook (`hodl_project.py`) into a clean, modular Python project.
It focuses on retrieval-augmented workflows (LangChain + Weaviate) and a Gradio UI for quick interaction.

## Structure
```
.
├── src/
│   ├── __init__.py
│   ├── app.py            # Gradio UI: index texts and query
│   ├── config.py         # Env + paths
│   ├── prompts.py        # format_docs, contextualized_question, answer
│   ├── rag_pipeline.py   # splitter -> embeddings -> vector store -> retriever
│   ├── text_utils.py     # normalize_text, clean_and_reduce_noise
│   └── legacy/
│       └── hodl_project_notebook.py  # original exported code (for reference)
├── data/
├── assets/
├── notebooks/
├── main.py               # CLI: --index, --serve
├── requirements.txt
└── README.md
```

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

## Notes
- The original notebook code is preserved in `src/legacy/`.
- If your notebook included explicit TensorFlow/Keras training, we can add `src/model.py` and wire it in next.
