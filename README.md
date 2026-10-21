# Content Repurposer Agent

An autonomous, multi-tool AI Agent built on the **Google Agent Development Kit (ADK)** and powered by **Gemini 3.8 Flash**. Designed for content creators and marketers to transform raw ideas or web URLs into platform-native social media posts (LinkedIn, X/Twitter, TikTok scripts) while strictly enforcing brand voice and eliminating generic AI clichés.

---

## 🌟 Key Features

1. **Platform-Native Content Repurposing**:
   - **LinkedIn**: Thought-leadership framing, whitespace formatting, professional career/business insights.
   - **X (Twitter)**: Concise hooks, punchy actionable steps, high readability.
   - **Short-form Video Scripts (TikTok/Reels)**: Dynamic retention hooks, visual stage directions `[Visual: ...]`, and spoken pacing.

2. **Real-Action Tools**:
   - 🌐 **Web Content Scraper (`fetch_url_content`)**: Extracts article text directly from public URLs using `httpx` and `BeautifulSoup4`.
   - ✍️ **Anti-Cliché Thesaurus (`find_word_synonyms`)**: Integrates with the Datamuse API to avoid overused corporate AI buzzwords (*"game changer"*, *"in today's fast-paced world"*).
   - 🗄️ **Firestore Persistence (`add_content_draft`, `list_content_drafts`, `update_draft_status`)**: Stores and manages draft lifecycles in Google Cloud Firestore.
   - 🎨 **Image Generation & Cloud Storage Hosting (`generate_marketing_image`)**: Generates 1K social visuals via `gemini-3.1-flash-lite-image` in Vertex AI, saves session artifacts, and uploads directly to a public Cloud Storage bucket for direct embedding.
   - 🔒 **Sandboxed Code Execution (`AgentEngineSandboxCodeExecutor`)**: Executes arbitrary Python code safely inside an isolated Vertex AI Agent Engine Sandbox container.

3. **Cross-Session Long-Term Memory (Vertex AI Memory Bank)**:
   - Features `PreloadMemoryTool` to inject durable user preferences (brand voice, target audience, preferred hashtags) across conversations.
   - Uses an asynchronous turn callback (`generate_memories_callback`) to extract and persist conversation facts automatically to Vertex AI Agent Engine Memory Bank.

---

## 📁 Project Architecture

```
content-repurposer-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py                 # Core agent definition, instructions, tools & Memory Bank
│   ├── fast_api_app.py          # FastAPI application, A2A routes, & runner lifespan
│   ├── tools.py                 # Firestore, Web Scraping, Image Gen, Datamuse tools
│   └── app_utils/
│       ├── a2a.py               # A2A protocol router
│       ├── reasoning_engine_adapter.py
│       └── services.py          # Shared Session, Artifact, & Memory Bank services
├── deployment/                  # Terraform deployment templates
├── tests/                       # Unit, integration, and evaluation suites
├── project_brief.md             # Project specification & guidelines
├── seed_firestore.py            # Firestore database seeding script
├── Dockerfile                   # Production container definition
├── pyproject.toml               # Python project configuration & dependencies
└── agents-cli-manifest.yaml     # Agents CLI project manifest
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **uv**: Fast Python package installer (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Google Cloud SDK (`gcloud`)**: Authenticated with your GCP project:
  ```bash
  gcloud auth application-default login
  gcloud config set project <YOUR_GCP_PROJECT_ID>
  ```

### Installation

Install all project dependencies into the virtual environment:
```bash
uv sync
```

---

## 💻 Local Development

### 1. Seed Initial Firestore Data (Optional)
```bash
uv run python seed_firestore.py
```

### 2. Run ADK Web Playground with Memory Bank
To launch the interactive playground connected to the Vertex AI Memory Bank:
```bash
uv run adk web . --port 8080 --reload_agents --memory_service_uri=agentengine://4737378064546136064
```
Open your browser and navigate to **`http://localhost:8080`**.

---

## 🛡️ Security & Environment Variables

- Sensitive files such as `.env`, `.venv`, credentials (`*-key.json`, `*.pem`), and build artifacts are strictly excluded via `.gitignore`.
- Cloud resource IDs and endpoints are configured to securely use Application Default Credentials (ADC).
