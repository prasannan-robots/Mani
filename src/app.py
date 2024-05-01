import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
#from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
#import chromadb
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.readers.file import PDFReader
import tempfile
import json
def main():
    st.title("AI Application")

    # Upload button for file
    uploaded_file = st.file_uploader("Upload File")
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(uploaded_file.getvalue())
        
        # Now you can use fp.name as the file path
        documents = PDFReader().load_data(fp.name)
        index = VectorStoreIndex.from_documents(
        documents
        )
        query_engine = index.as_query_engine()
        rs = query_engine.query("List the overall Categories in the form of list with a json key categories and list of columns in the file with a json key columns").response
        ai_output = query_engine.query("Analyse of source data for stakeholders").response
        # Multi selection for selecting columns
        rs = json.loads(rs)
        selected_columns = st.multiselect("Select Columns", rs['columns'])

        # Selection for categories
        selected_category = st.selectbox("Select Category", rs['columns'])

        # Text area for AI output
        st.subheader("AI Output:")
        
        st.write(ai_output)

        # Text area for user questions
        user_question = st.text_area("Ask a question")

        # Download button
        if st.button("Download"):
            # Code for downloading file
            pass

if __name__ == "__main__":
    main()
