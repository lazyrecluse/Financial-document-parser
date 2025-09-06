import streamlit as st

# --- Page setup ---
st.set_page_config(page_title="Financial Report Agent", page_icon="💼", layout="centered")

# --- Greeting & purpose ---
st.title("💼 Welcome to the Financial Report Agent")
st.write(
    """
    Hi there! 👋  
    This agent is designed to **analyze financial documents** (e.g., annual reports, balance sheets, income statements).  
    Upload your files below, and the agent will help you extract insights, summarize key points, 
    and answer your questions more precisely.
    """
)

# --- Upload section ---
uploaded_files = st.file_uploader(
    "📂 Please upload one or more financial documents (PDF, DOCX, or TXT):",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)


if uploaded_files:
    st.success(f"✅ You uploaded {len(uploaded_files)} file(s).Please wait while we parse and index your files...")
    for file in uploaded_files:
        st.write(f"- {file.name}")
else:
    st.info("No files uploaded yet. Please add your financial documents above ☝️")
