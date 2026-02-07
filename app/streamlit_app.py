from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.components.chat_interface import render_chat  # noqa: E402
from app.components.document_manager import render_document_manager  # noqa: E402


st.set_page_config(page_title="Enterprise Policy Assistant", layout="wide")

st.title("Enterprise Policy Assistant")
st.write(
    "Search internal HR policies, SOPs, and knowledge-base documents with AI-powered "
    "semantic search."
)

with st.sidebar:
    st.header("Navigation")
    view = st.radio("Select view", ["Chat", "Document Manager"], index=0)

if view == "Chat":
    render_chat()
else:
    render_document_manager()
