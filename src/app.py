"""Omega - a financial-advisor chatbot (Streamlit + LlamaIndex ReAct agent).

The agent can pull live data through the Yahoo Finance tools. Run with:
    streamlit run src/app.py
Set OPENAI_API_KEY in the environment or a .env file.
"""

import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "You are Omega, a careful financial assistant. Help the user understand "
    "investment options for their budget and goals. Use the available tools to "
    "look up live market data when relevant. Always remind the user that this "
    "is general information, not personalised financial advice, and that "
    "investments carry risk."
)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


@st.cache_resource(show_spinner="Starting Omega…")
def build_agent():
    # Built lazily and cached so a missing key shows a friendly message
    # instead of crashing the whole app at import time.
    from llama_index.core.agent import ReActAgent
    from llama_index.llms.openai import OpenAI
    from llama_index.tools.yahoo_finance import YahooFinanceToolSpec

    llm = OpenAI(model=MODEL)
    tools = YahooFinanceToolSpec().to_tool_list()
    return ReActAgent.from_tools(tools, llm=llm, verbose=True, context=SYSTEM_PROMPT)


def main():
    st.set_page_config(page_title="Omega · Financial assistant", page_icon="📈")
    st.title("📈 Omega")
    st.caption("A financial assistant. General information only — not personalised advice.")

    if not os.getenv("OPENAI_API_KEY"):
        st.error("Set `OPENAI_API_KEY` in your environment or a `.env` file to start.")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Ask about stocks, funds or budgeting…"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking…"):
                    answer = str(build_agent().chat(user_input))
            except Exception as error:  # network/API/tool failures shouldn't crash the app
                answer = f"Sorry, something went wrong: {error}"
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
