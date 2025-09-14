import streamlit as st
import os
# from retriever import chat_engine
# --- Page setup ---
st.set_page_config(page_title="Financial Report Agent", page_icon="💼", layout="centered")

# --- Greeting & purpose ---
st.title("💼 Welcome to the Financial Report Agent")
st.write(
    """
    Hi there! 👋  
    This agent is designed to **analyze financial documenSts** (e.g., annual reports, balance sheets, income statements).  
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
    try:
        dir = "files"
        for uploaded_file in uploaded_files:
            file_content = uploaded_file.read()
            file_name = uploaded_file.name

    
            file_path = os.path.join(dir, file_name)

            # Check and create the directory
            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(file_path, "wb") as f:
                f.write(file_content)

        st.success(f"✅ You uploaded {len(uploaded_files)} file(s).Please wait while we parse and index your files...")

    except Exception as e:
        st.error(f"An error occurred: {e}") 
else:
    st.info("No files uploaded yet. Please add your financial documents above ☝️")