"""
Gradio app to index texts and query the retriever.
"""
import gradio as gr
from .rag_pipeline import RAGConfig, build_vector_store, get_retriever
from .prompts import format_docs

VECTOR_STORE = None
RETRIEVER = None

def index_texts(texts):
    global VECTOR_STORE, RETRIEVER
    cfg = RAGConfig()
    VECTOR_STORE = build_vector_store(texts, cfg)
    RETRIEVER = get_retriever(VECTOR_STORE, k=5)
    return "Index built successfully."

def ask(query):
    if RETRIEVER is None:
        return "Please index texts first."
    docs = RETRIEVER.get_relevant_documents(query)
    context = format_docs(docs)
    return context[:2000]

def launch():
    with gr.Blocks() as demo:
        gr.Markdown("# HODL Project — RAG Demo")
        with gr.Tab("Index"):
            input_texts = gr.Textbox(lines=6, placeholder="Paste documents here (one per line)")
            index_btn = gr.Button("Build Index")
            status = gr.Markdown()
            index_btn.click(fn=lambda s: index_texts([t for t in s.splitlines() if t.strip()]), inputs=input_texts, outputs=status)
        with gr.Tab("Ask"):
            q = gr.Textbox(label="Question")
            a = gr.Textbox(label="Answer / Retrieved Context")
            ask_btn = gr.Button("Ask")
            ask_btn.click(fn=ask, inputs=q, outputs=a)
    demo.launch()

if __name__ == "__main__":
    launch()
