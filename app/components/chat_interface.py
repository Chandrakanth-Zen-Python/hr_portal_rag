from __future__ import annotations

import streamlit as st

from src.rag_pipeline import RAGPipeline


def render_chat() -> None:
    st.subheader("Ask the Policy Assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask about HR policies, SOPs, or internal wiki...")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                pipeline = RAGPipeline()
                result = pipeline.answer_query(question)
                answer = result["answer"]
                st.markdown(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
