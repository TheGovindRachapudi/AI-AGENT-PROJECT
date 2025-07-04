from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from functools import partial
from langchain.agents import AgentExecutor, create_tool_calling_agent
from tools import search_tool, wiki_tool, save_tool, chatgpt_tool

print(">>> main.py is running")

print("Loading environment variables...")
load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

print("Getting API key...")
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    print("ERROR: OPENAI_API_KEY environment variable is not set.")
    exit(1)
else:
    print("API key loaded.")

def format_research_response(response: ResearchResponse) -> str:
    """Format the ResearchResponse object into a professional, readable string."""
    output = []
    output.append("\n================ Research Report ================\n")
    output.append(f"Topic: {response.topic}\n")
    output.append(f"Summary:\n{response.summary}\n")
    output.append("Sources:")
    if response.sources:
        for src in response.sources:
            output.append(f"  - {src}")
    else:
        output.append("  (No sources provided)")
    output.append("\nTools Used:")
    if response.tools_used:
        for tool in response.tools_used:
            output.append(f"  - {tool}")
    else:
        output.append("  (No tools listed)")
    output.append("\n=================================================\n")
    return "\n".join(output)

try:
    print("Initializing LLM...")
    llm = ChatOpenAI(
        model="gpt-4o",  # or "gpt-3.5-turbo"
        api_key=SecretStr(api_key)
    )

    print("Testing LLM with a simple query...")
    response = llm.invoke("Who is Playboi Carti?")
    print("LLM response received.")

    parser = PydanticOutputParser(pydantic_object=ResearchResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a helpful assistant that can answer questions and help with tasks. 
                Answer the question based on the information provided.
                Wrap the output in this format and provide nothing else\n(format_instructions)
                """,
            ), 
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    print("Creating agent...")
    tools = [chatgpt_tool, search_tool, wiki_tool, save_tool]
    query = input("What can I help you Research?")

    print("\n================= Research Results =================\n")
    results = {}
    results['ChatGPT'] = chatgpt_tool.run(query)
    results['DuckDuckGo'] = search_tool.run(query)
    results['Wikipedia'] = wiki_tool.run(query)

    for tool_name, result in results.items():
        print(f"--- {tool_name} ---\n{result}\n")
    print("===================================================\n")

    # Prompt user to save results
    save_options = list(results.keys()) + ["All", "None"]
    print("Which result would you like to save?")
    for idx, opt in enumerate(save_options, 1):
        print(f"  {idx}. {opt}")
    choice = input("Enter the number of your choice: ").strip()
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(save_options):
            selected = save_options[choice_idx]
            if selected == "None":
                print("No results saved.")
            elif selected == "All":
                combined = "\n\n".join([f"--- {k} ---\n{v}" for k, v in results.items()])
                save_result = save_tool.run(combined)
                print(save_result)
            else:
                save_result = save_tool.run(results[selected])
                print(save_result)
        else:
            print("Invalid choice. No results saved.")
    except Exception:
        print("Invalid input. No results saved.")

except Exception as e:
    print("An error occurred:", e)







