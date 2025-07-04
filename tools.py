from langchain_community.utilities import SerpAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain.tools import Tool
from datetime import datetime
from pydantic import SecretStr
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Save to file tool
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

# SerpAPI-powered Search tool
def safe_serpapi_search(query: str) -> str:
    try:
        time.sleep(1)  # throttle to avoid abuse
        search = SerpAPIWrapper()
        return search.run(query)
    except Exception as e:
        return f"⚠️ SerpAPI Search failed: {str(e)}"

search_tool = Tool(
    name="Search",
    func=safe_serpapi_search,
    description="Search Google using SerpAPI for the latest information on a given topic.",
)

# Wikipedia tool
def safe_wiki_search(query: str) -> str:
    try:
        api_wrapper = WikipediaAPIWrapper(wiki_client=None, top_k_results=1, doc_content_chars_max=1000)
        wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
        return wiki_tool.run(query)
    except Exception as e:
        return f"⚠️ Wikipedia Search failed: {str(e)}"

wiki_tool = Tool(
    name="Wikipedia",
    func=safe_wiki_search,
    description="Search Wikipedia for a summary of the topic.",
)


