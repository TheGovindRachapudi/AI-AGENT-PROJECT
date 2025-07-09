# TriFacta

A user-friendly research assistant that leverages ChatGPT, Google, and Wikipedia to answer your questions, compare results, and save findings—all from a simple web interface.

## Features
- Query ChatGPT, Google, and Wikipedia in parallel
- Compare answers from multiple sources
- Save your preferred results to a text file
- Clean, interactive web UI powered by Streamlit
- Download Research Output from Text File

## Demo
Application URL: https://thegovindrachapudi-ai-agent-project-app-dd43ri.streamlit.app/


1. Enter your research question in the input box.
2. Click **Search** to get answers from all sources.
3. Review the results from ChatGPT, Google Search, and Wikipedia.
4. Select which result(s) to save and click **Save Selected Result**.

---

## Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd AI-AGENT-PROJECT
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Streamlit app
```bash
streamlit run app.py
```

---

## File Structure
- `app.py` — Streamlit web interface
- `main.py` — Command-line version
- `tools.py` — Tool definitions (ChatGPT, Google Search, Wikipedia, Save)
- `requirements.txt` — Python dependencies
- `research_output.txt` — Saved research results

---

## License
MIT 
