import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from llama_index.core import VectorStoreIndex
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
prompt='''You are a financial advisor who is looking to provide investment advice to a client. Help the client with choosing the right investment option with their budget'''
tool_spec = YahooFinanceToolSpec()
llm = OpenAI(model="gpt-3.5-turbo-instruct")
agent = ReActAgent.from_tools(tool_spec.to_tool_list(), llm=llm, verbose=True,context=prompt)
print(agent.get_prompts())
def main():
    st.title("Omega")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_input = st.text_input("You: ", key="user_input")
    # Submit button
    if st.button("Send"):
        if user_input:
            # Append user input to chat history
            st.session_state.chat_history.append(f"You: {user_input}")
            # Here you can add the logic to get the response from the chatbot
            # For now, we'll just echo the user input as a response
            
            response = agent.chat(user_input)
            
            response = f"Bot: {response}"
            st.session_state.chat_history.append(response)
            # Clear the input box
        

    # Display chat history
    for message in st.session_state.chat_history:
        st.write(message)

if __name__ == "__main__":
    main()