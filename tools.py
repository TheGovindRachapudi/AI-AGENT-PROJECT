from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from pydantic import SecretStr

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)


search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="Search the web for the latest information on a given topic",
)

api_wrapper = WikipediaAPIWrapper(wiki_client=None, top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

def chatgpt_answer(query: str) -> str:
    """Return a direct answer from the LLM (ChatGPT) for the given query."""
    from langchain_openai import ChatOpenAI
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "ERROR: OPENAI_API_KEY environment variable is not set."
    llm = ChatOpenAI(model="gpt-4o", api_key=SecretStr(str(api_key)))
    response = llm.invoke(query)
    # Extract content if response is a BaseMessage
    if hasattr(response, 'content'):
        return str(response.content)
    if isinstance(response, (list, dict)):
        return str(response)
    return str(response)

chatgpt_tool = Tool(
    name="ChatGPT",
    func=chatgpt_answer,
    description="Get a direct answer from ChatGPT (LLM) for the given query.",
)