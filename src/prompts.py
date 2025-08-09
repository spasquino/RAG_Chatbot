"""
Prompt helpers for retrieval-augmented QA.
"""
def format_docs(docs):

        return "\n\n".join(doc.page_content for doc in docs)

    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import AIMessage, HumanMessage

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )
    contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

    qa_system_prompt = """You are an assistant for question-answering tasks for students of a class called Hands-on Deep Learning.\
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use five sentences maximum and keep the answer concise.\

    {context}"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

def contextualized_question(input, **kwargs):

        if input.get("chat_history"):
            return contextualize_q_chain
        else:
            return input["question"]

    contextualize_q_chain.invoke(
        {
            "chat_history": [
                HumanMessage(content="What does LLM stand for?"),
                AIMessage(content="Large language model"),
            ],
            "question": "What is meant by large",
        }
    )

    rag_chain = (
        RunnablePassthrough.assign(
            context=contextualized_question | retriever | format_docs
        )
        | qa_prompt
        | llm
    )

    chat_history = []

    question = "What is a tartiflette ?"
    ai_msg = rag_chain.invoke({"question": question, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=question), ai_msg])
    ai_msg.content

    second_question = "And LLMs ?"
    rag_chain.invoke({"question": second_question, "chat_history": chat_history}).content

    """## User interface"""

    !pip install gradio

    import gradio as gr

def answer(context, question, **kwargs):


      history_langchain_format = []

      for message in chat_history:
          history_langchain_format.extend([HumanMessage(content=message[0]),AIMessage(content=message[1])])

      rag_chain = (
          RunnablePassthrough.assign(
              context=contextualized_question | retriever | format_docs
          )
          | qa_prompt
          | llm
      )
      result = rag_chain.invoke({"question": query, "chat_history": history_langchain_format})
      return result.content

    gr.ChatInterface(fn=answer,
                     chatbot=gr.Chatbot(height=600),
                     theme="soft").launch(debug=True)
