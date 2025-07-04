import streamlit as st
from tools import chatgpt_tool, search_tool, wiki_tool, save_tool

st.set_page_config(page_title="AI Research Agent", layout="centered")
st.title("🤖 AI Research Agent")
st.write("Enter a topic or question and get answers from ChatGPT, Google Search, and Wikipedia!")

query = st.text_input("What can I help you research?", "")

if st.button("Search") and query.strip():
    with st.spinner("Querying all sources..."):
        chatgpt_result = chatgpt_tool.run(query)
        search_result = search_tool.run(query)  # Formerly DuckDuckGo
        wiki_result = wiki_tool.run(query)
    st.success("Results ready!")

    st.subheader("ChatGPT")
    st.write(chatgpt_result)
    st.subheader("Google Search")
    st.write(search_result)
    st.subheader("Wikipedia")
    st.write(wiki_result)

    st.markdown("---")
    st.write("**Save Results**")
    save_options = ["ChatGPT", "Google Search", "Wikipedia", "All"]
    save_choice = st.selectbox("Which result would you like to save?", save_options)
    if st.button("Save Selected Result"):
        if save_choice == "All":
            combined = (
                f"--- ChatGPT ---\n{chatgpt_result}\n\n"
                f"--- Google Search ---\n{search_result}\n\n"
                f"--- Wikipedia ---\n{wiki_result}"
            )
            save_msg = save_tool.run(combined)
        elif save_choice == "ChatGPT":
            save_msg = save_tool.run(chatgpt_result)
        elif save_choice == "Google Search":
            save_msg = save_tool.run(search_result)
        elif save_choice == "Wikipedia":
            save_msg = save_tool.run(wiki_result)
        else:
            save_msg = "No result selected."
        st.info(save_msg)
else:
    st.info("Enter a query and click Search to begin.")
