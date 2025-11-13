---
title: Multi-Source Job Search Assistant
emoji: 💼
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# Multi-Source Job Search Assistant

Interactive Gradio application powered by a LangGraph agent that searches job listings from **FindSGJobs** and **Adzuna** APIs. Search live job openings in Singapore and other regions through a conversational AI interface backed by Google Gemini.

## Features

- **Dual-Source Job Search**: Query both FindSGJobs (Singapore-specific) and Adzuna (global with salary insights)
- **LangGraph Agent**: Advanced AI agent using function tools for intelligent job search
- **Real-time Data**: Direct API integration for up-to-date job listings
- **Market Intelligence**: Get salary distributions, hiring trends, and top companies
- **Smart Formatting**: Clean tables with job titles, companies, locations, and direct links
- **Conversational UI**: Natural language interaction via Gradio chat interface
- **Easy Deployment**: Deploy to Hugging Face Spaces in 5 minutes with free hosting

## Requirements

- Python 3.12 (see `environment.yml` for the exact stack)
- Google API key with access to the Gemini model family
- **Optional**: Adzuna API credentials (app_id and app_key) for Adzuna features
  - Get free credentials at [Adzuna Developer Portal](https://developer.adzuna.com/)
  - FindSGJobs API works without authentication

## Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd adzuna_gradio
   ```

2. **Create the environment (recommended with Conda)**

   ```bash
   conda env create -f environment.yml
   conda activate mcp-env
   ```

   Or install manually with `pip` inside a Python 3.12 virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS / Linux
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   ```bash
   # PowerShell
   $env:GOOGLE_API_KEY = "your_google_api_key"

   # Optional: For Adzuna features
   $env:ADZUNA_APP_ID = "your_adzuna_app_id"
   $env:ADZUNA_APP_KEY = "your_adzuna_app_key"
   ```

   On Unix-like shells use `export GOOGLE_API_KEY=...` and optionally set Adzuna credentials.

   **Note**: FindSGJobs works without API keys. Adzuna features require credentials from [developer.adzuna.com](https://developer.adzuna.com/).

## Running the App

### Local Development

```bash
python app.py
```

Gradio will print a local URL (and optionally a public link) in the console. Open it in the browser to start chatting with the agent.

### Deploy to Hugging Face Spaces

Deploy your app for free with automatic HTTPS and no server management. Below is an integrated quick start plus detailed instructions adapted for this project (replace any reference to `run_adzuna_agent.py` with `app.py`).

---

#### 🚀 Quick Start (5 Minutes)

1. Go to https://huggingface.co/new-space
2. Choose a Space name (e.g., `multi-source-job-assistant`)
3. Select **Gradio** as the SDK
4. Pick **Free CPU** hardware (sufficient for this app)
5. Click **Create Space**
6. Upload files: `app.py`, `requirements.txt`, `README.md` (this file), `function_tool.py`
7. In **Settings → Repository secrets** add: `GOOGLE_API_KEY = <your_google_api_key>`
8. (Optional) Add `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` for Adzuna features
9. Watch the **Logs** tab; app goes live at `https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`

---

#### 📋 Detailed Instructions

##### Prerequisites

- Hugging Face account (sign up: https://huggingface.co/join)
- Google Generative AI API key (https://makersuite.google.com/app/apikey)
- (Optional) Git installed locally for Git-based deployment

##### Deployment Methods

###### Method 1: Web Upload (Easiest)

1. Create Space at https://huggingface.co/new-space
   - Name: `multi-source-job-assistant`
   - SDK: Gradio
   - Hardware: Free CPU
   - Visibility: Public or Private
2. Upload files via **Files → Add file → Upload files**:
   - `app.py`
   - `requirements.txt`
   - `function_tool.py`
   - `README.md`
3. Add secret: **Settings → Repository secrets → New secret**
   - Name: `GOOGLE_API_KEY`
   - Value: your Google API key
4. (Optional) Add Adzuna secrets: `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`
5. Watch **Logs**; Space builds and serves automatically.

###### Method 2: Git Push (Best for Updates)

1. Create the Space (same as Method 1)
2. Clone the Space repo:
   ```powershell
   git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
   cd SPACE_NAME
   ```
3. Copy project files into the cloned folder (adjust source path as needed):
   ```powershell
   Copy-Item ..\multi_jobs_gradio\app.py .
   Copy-Item ..\multi_jobs_gradio\function_tool.py .
   Copy-Item ..\multi_jobs_gradio\requirements.txt .
   Copy-Item ..\multi_jobs_gradio\README.md .
   ```
4. Commit & push:
   ```powershell
   git add .
   git commit -m "Initial deployment"
   git push
   ```
5. Add required secret(s) via web UI: **Settings → Repository secrets**

##### Required Files Summary

- `app.py` (Gradio entrypoint specified by `app_file`)
- `function_tool.py` (API/tooling functions)
- `requirements.txt` (Python dependencies)
- `README.md` (Project documentation + deployment guide)
- `environment.yml` (Optional: for reproducible Conda environment; not required by Spaces build)

##### Required Secrets

- `GOOGLE_API_KEY`: Gemini model access (mandatory)

##### Optional Secrets

- `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`: Enable Adzuna search and salary analytics

##### Notes

- Spaces automatically runs Gradio using the `app_file` defined in the metadata block at the top of this README.
- Keep dependencies lean; large packages can slow cold starts.
- For updates: push changes to the Space repo; build restarts automatically.
- To switch to private mode, toggle visibility in Space settings (secrets remain intact).

## Using the Assistant

### Example Queries

**FindSGJobs (Singapore-specific, no API key needed):**

- "Find data analyst jobs using FindSGJobs"
- "Search for software engineer positions on FindSGJobs"
- "Get job market statistics for marketing roles"

**Adzuna (Global with salary data, requires API credentials):**

- "Search for data science jobs in Singapore using Adzuna"
- "Show me salary distribution"
- "Which companies are hiring the most?"
- "Find remote software developer positions"

**General Usage:**

- Ask for specific roles, locations, or companies
- Request market intelligence and hiring trends
- Get salary insights and top employers
- The agent automatically formats results in clean tables with clickable links

## Project Structure

```
multi_jobs_gradio/
├── app.py             # Main application (Gradio UI + LangGraph agent)
├── function_tool.py   # API integration functions (FindSGJobs & Adzuna)
├── requirements.txt   # Python dependencies
├── environment.yml    # Conda environment specification (optional for Spaces)
└── README.md          # Project documentation & deployment guide (no separate DEPLOYMENT.md)
```

## Development Notes

- **`app.py`**: Contains the LangGraph agent setup, function tool integration, and Gradio UI
- **`function_tool.py`**: Direct API integrations for FindSGJobs and Adzuna with structured response formatting
- **Function Tools**: Five tools available to the agent:
  1. `search_findsgjobs` - Search Singapore jobs on FindSGJobs
  2. `get_findsgjobs_statistics` - Get job market statistics from FindSGJobs
  3. `search_adzuna` - Search jobs globally with salary data
  4. `get_salary_histogram` - Get salary distributions on Adzuna
  5. `get_top_hiring_companies` - Get top employers on Adzuna
- **API Architecture**: Direct REST API calls (no MCP server dependency)
- **Model**: Google Gemini 2.5 Flash for fast, intelligent responses
- **Agent Framework**: LangGraph with ReAct pattern for tool selection and reasoning

## API Credentials

### Google Gemini (Required)

Get your free API key at [Google AI Studio](https://aistudio.google.com)

### Adzuna API (Optional)

1. Sign up at [Adzuna Developer Portal](https://developer.adzuna.com/)
2. Create an app to get your `app_id` and `app_key`

### FindSGJobs API

No authentication required - works out of the box!

## License

MIT License - See LICENSE file for details
