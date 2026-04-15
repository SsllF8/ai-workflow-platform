# ⚡ AI Workflow Automation Platform

> A visual, node-based AI workflow editor that lets you build custom AI pipelines by connecting different processing nodes. Design once, run many times — automate text generation, web scraping, sentiment analysis, code generation, and more.

![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-blue)

![Workflow Editor](screenshots/workflow-editor.png)
![Templates](screenshots/workflow-templates.png)
![Results](screenshots/workflow-result.png)

## 🎯 Use Cases

### Content Creation
- **Translation + Summarization Pipeline** — Input Chinese article → AI translates to English → AI summarizes key points → Export to file
- **Content Repurposing** — Take a long article → Extract key information → Generate social media posts → Sentiment check for brand safety
- **Meeting Notes Processing** — Raw meeting transcript → AI summary → Extract action items → Export structured minutes as TXT

### Data Processing
- **Web Content Analysis** — URL input → Scrape web page → AI summary → Extract keywords → Sentiment analysis
- **Competitor Monitoring** — Scrape competitor pages → Summarize changes → Sentiment analysis on announcements → Export report
- **Review Analysis** — Customer reviews input → Sentiment analysis per review → Extract common keywords → AI summary of trends

### Development
- **Code Review Pipeline** — Paste code → AI code review → AI suggested improvements → Export annotated code
- **Documentation Generator** — Source code or API spec → AI explains functionality → Generate documentation → Export
- **Multi-language Code Translation** — Python code → AI translates to JavaScript → Export

### Key Differentiator
This is a **no-code AI pipeline builder**. Instead of writing scripts to chain multiple AI operations, you visually connect nodes on a canvas. The custom workflow engine handles data passing between nodes, error handling, and sequential execution. Think of it as a lightweight, self-hosted alternative to Zapier/Make, but specifically designed for AI text processing tasks.

## ✨ Features

### Core Capabilities
- 🔧 **Visual Workflow Editor** — Add, configure, reorder, and delete nodes with an intuitive UI
- 🧩 **9 Built-in Node Types** — Cover input, processing, AI, and output operations
- ▶️ **One-Click Execution** — Run the entire workflow and see results from each node
- 📋 **Template Library** — 4 pre-built workflow templates for common use cases
- 💾 **Save Custom Templates** — Save your workflows as reusable templates
- 📥 **Export Results** — Download final output as TXT file
- 📋 **Copy to Clipboard** — One-click copy of any node's output

### Node Types

| Category | Node | Description |
|----------|------|-------------|
| **Input** | 📥 Text Input | User-provided text as workflow starting point |
| **Input** | 🌐 Web Scrape | Fetch and extract text content from a URL |
| **AI** | 🤖 AI Text Generation | General-purpose text generation with custom prompts |
| **AI** | 📝 AI Summary | Condense long text into a concise summary |
| **AI** | 🔑 AI Keyword Extraction | Extract important keywords and topics from text |
| **AI** | 📊 AI Information Extraction | Extract structured data (names, dates, etc.) from text |
| **AI** | 😊 AI Sentiment Analysis | Analyze emotional tone (positive/negative/neutral) |
| **AI** | 💻 AI Code Generation | Generate, review, or explain code |
| **Output** | 📄 File Export | Export node output to a downloadable text file |

### Pre-built Templates

| Template | Pipeline | Use Case |
|----------|----------|----------|
| **Translation + Summary** | Text Input → AI Translate → AI Summary | Translate articles and get a quick summary |
| **Web Content Analysis** | Web Scrape → AI Summary → Keyword Extraction | Analyze any web page automatically |
| **Code Review + Export** | Text Input → AI Code Review → File Export | Review code and save the analysis |
| **Sentiment Analysis Flow** | Text Input → Sentiment → Keywords → Summary | Deep analysis of text sentiment and themes |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                          │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Sidebar  │  │   Workflow   │  │   Results Panel      │ │
│  │  Node     │  │   Editor     │  │   (per-node output)  │ │
│  │  Palette  │  │   + Config   │  │                      │ │
│  └─────┬─────┘  └──────┬───────┘  └──────────┬───────────┘ │
└────────┼────────────────┼──────────────────────┼───────────┘
        │                │                      │
┌───────▼────────────────▼──────────────────────▼───────────┐
│                    Workflow Engine                          │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  1. Parse workflow JSON                               │ │
│  │  2. Topologically sort nodes                          │ │
│  │  3. Execute each node sequentially                    │ │
│  │  4. Pass output of node N as input to node N+1        │ │
│  │  5. Collect results from all nodes                    │ │
│  └──────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
        │                              │
        ▼                              ▼
┌───────────────┐              ┌──────────────────┐
│  Node Modules │              │  DeepSeek API    │
│  (9 plugins)  │              │  (AI Processing) │
└───────────────┘              └──────────────────┘
```

### Workflow Engine Design

The core engine (`workflow_engine.py`) implements a **sequential node execution model**:

```
Node Registry (singleton)
  └── Each node type registers itself with: name, category, config_schema, execute()

Workflow Execution:
  1. Build ordered list of nodes
  2. For each node:
     a. Resolve input (user input for first node, previous node's output for others)
     b. Merge with node's custom config (prompt template, parameters, etc.)
     c. Call node.execute(input_data, config)
     d. Store result (output text + metadata)
  3. Return all results
```

## 📁 Project Structure

```
ai-workflow-platform/
├── app.py                      # Streamlit web interface (main entry)
├── workflow_engine.py          # Core workflow execution engine
├── nodes/                      # Node plugin system
│   ├── __init__.py             # Node registry & base classes
│   ├── input_node.py           # Text input node
│   ├── web_scrape_node.py      # Web scraping node
│   ├── ai_text_node.py         # AI text generation node
│   ├── ai_summary_node.py      # AI summarization node
│   ├── ai_keywords_node.py     # AI keyword extraction node
│   ├── ai_extract_node.py      # AI information extraction node
│   ├── ai_sentiment_node.py    # AI sentiment analysis node
│   ├── ai_code_node.py         # AI code generation node
│   └── file_export_node.py     # File export node
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── screenshots/                # UI screenshots
│   ├── workflow-editor.png
│   ├── workflow-templates.png
│   └── workflow-result.png
└── 启动应用.bat                 # Windows quick start
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- DeepSeek API Key ([Get one here](https://platform.deepseek.com))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/SsllF8/ai-workflow-platform.git
cd ai-workflow-platform

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and fill in your DEEPSEEK_API_KEY

# 5. Run the application
streamlit run app.py
```

Or simply double-click `启动应用.bat` on Windows.

### How to Use

**Option A: Use a Template**
1. Click "📁 模板库" tab
2. Choose a pre-built template
3. Click "使用" to load it into the editor
4. Enter your input text/URL, then click "▶️ 运行工作流"

**Option B: Build from Scratch**
1. In "🔧 创建工作流" tab, use the sidebar to add nodes
2. Configure each node's parameters (prompt templates, settings)
3. Reorder nodes by clicking ⬆️/⬇️ buttons
4. Enter input text, then click "▶️ 运行工作流"
5. View each node's output in the results panel
6. Optionally save as a custom template for reuse

## ⚙️ Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | ✅ | Your DeepSeek API key |

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | Streamlit | Interactive workflow editor UI |
| AI | DeepSeek API | Text processing, analysis, and generation |
| Web Scraping | Requests + BeautifulSoup | Fetch and parse web page content |
| Workflow Engine | Custom Python | Node registry, execution pipeline, data passing |
| Plugin System | Custom Python | Extensible node architecture with auto-registration |

## 🔧 Extending with Custom Nodes

The platform uses a plugin-based node system. To add a new node type:

```python
# nodes/my_custom_node.py
from nodes import BaseNode, NodeResult, register_node

class MyCustomNode(BaseNode):
    name = "My Custom Node"
    category = "AI"
    description = "Does something custom"
    
    def get_config_schema(self):
        return {"param1": {"type": "text", "label": "Parameter"}}
    
    def execute(self, input_data, config):
        # Your processing logic here
        result = process(input_data, config["param1"])
        return NodeResult(success=True, output=result)

register_node(MyCustomNode)
```

Then import it in `app.py` to register it:
```python
import nodes.my_custom_node
```

## 📄 License

This project is licensed under the MIT License.
