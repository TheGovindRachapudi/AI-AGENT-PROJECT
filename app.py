import streamlit as st
from tools import chatgpt_tool, search_tool, wiki_tool, save_tool

st.set_page_config(page_title="AI Research Agent", layout="centered")
st.title("🤖 AI Research Agent")
st.write("Enter a topic or question and get answers from ChatGPT, Google Search, and Wikipedia!")

query = st.text_input("What can I help you research?", "")

# Check if results are in session_state
if "chatgpt_result" not in st.session_state:
    st.session_state.chatgpt_result = ""
if "search_result" not in st.session_state:
    st.session_state.search_result = ""
if "wiki_result" not in st.session_state:
    st.session_state.wiki_result = ""

if st.button("Search") and query.strip():
    with st.spinner("Querying all sources..."):
        st.session_state.chatgpt_result = chatgpt_tool.run(query)
        st.session_state.search_result = search_tool.run(query)
        st.session_state.wiki_result = wiki_tool.run(query)
    st.success("Results ready!")

# Display results if available
if st.session_state.chatgpt_result or st.session_state.search_result or st.session_state.wiki_result:
    st.subheader("ChatGPT")
    st.write(st.session_state.chatgpt_result)

    st.subheader("Google Search")
    st.markdown(st.session_state.search_result)

    st.subheader("Wikipedia")
    st.write(st.session_state.wiki_result)

    st.markdown("---")
    st.write("**Save Results**")
    save_options = ["ChatGPT", "Google Search", "Wikipedia", "All"]
    save_choice = st.selectbox("Which result would you like to save?", save_options)

    if st.button("Save Selected Result"):
        if save_choice == "All":
            combined = (
                f"--- ChatGPT ---\n{st.session_state.chatgpt_result}\n\n"
                f"--- Google Search ---\n{st.session_state.search_result}\n\n"
                f"--- Wikipedia ---\n{st.session_state.wiki_result}"
            )
            save_msg = save_tool.run(combined)
        elif save_choice == "ChatGPT":
            save_msg = save_tool.run(st.session_state.chatgpt_result)
        elif save_choice == "Google Search":
            save_msg = save_tool.run(st.session_state.search_result)
        elif save_choice == "Wikipedia":
            save_msg = save_tool.run(st.session_state.wiki_result)
        else:
            save_msg = "⚠️ No result selected."
        st.info(save_msg)

        # ⬇️ Add download button after saving
        try:
            with open("research_output.txt", "r", encoding="utf-8") as f:
                file_contents = f.read()

            st.download_button(
                label="📥 Download Saved File",
                data=file_contents,
                file_name="research_output.txt",
                mime="text/plain"
            )
        except FileNotFoundError:
            st.warning("⚠️ Could not find saved file to download.")
else:
    st.info("Enter a query and click Search to begin.")

