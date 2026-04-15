# ⚡ AI 工作流自动化平台

> 可视化编排 AI 工作流，将多个 AI 能力串联组合，一键运行。

## ✨ 功能特性

- 🔗 **可视化工作流编辑** — 添加、配置、排序节点，搭建自动化流程
- 🧩 **9 种智能节点** — 文本输入、网页抓取、AI 翻译/摘要/关键词/情感分析/代码助手、文件导出
- 📁 **模板库** — 内置 4 个预置模板，一键加载使用
- 💾 **自定义模板** — 创建好的工作流可保存为模板复用
- 📊 **实时结果展示** — 每个节点的执行状态、耗时和输出一目了然
- 📋 **结果导出** — 一键复制或下载为 TXT 文件

## 🖥 系统截图

### 工作流编辑器

![工作流编辑器](screenshots/workflow-editor.png)

### 运行结果

![运行结果](screenshots/workflow-result.png)

### 模板库

![模板库](screenshots/workflow-templates.png)

## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| DeepSeek API | AI 文本处理核心 |
| Streamlit | Web 界面框架 |
| 自研工作流引擎 | 节点注册、编排、执行 |
| Python-dotenv | 环境变量管理 |

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/SsllF8/ai-workflow-platform.git
cd ai-workflow-platform
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`，填入 DeepSeek API Key：

```bash
copy .env.example .env
```

### 4. 运行

```bash
streamlit run app.py
```

或者双击 `启动应用.bat`。

## 📖 节点说明

| 节点 | 类型 | 功能 |
|------|------|------|
| 📝 文本输入 | 输入 | 输入起始文本 |
| 🌐 网页抓取 | 输入 | 抓取网页正文内容 |
| 🤖 AI 文本处理 | AI | 翻译/润色/改写/续写 |
| 📋 AI 摘要总结 | AI | 生成文本摘要 |
| 🏷️ 关键词提取 | AI | 提取关键词标签 |
| 📊 AI 数据提取 | AI | 提取结构化信息 |
| 😎 AI 情感分析 | AI | 分析情感倾向 |
| 💻 AI 代码助手 | AI | 解释/生成/审查代码 |
| 📤 导出文件 | 输出 | 保存为 TXT/Markdown |

## 🏗 项目架构

```
ai-workflow-platform/
├── app.py              # Streamlit 主界面
├── workflow_engine.py  # 工作流引擎核心
├── nodes/              # 节点模块
│   ├── __init__.py     # 节点注册表
│   ├── input_node.py   # 文本输入
│   ├── web_scrape_node.py
│   ├── ai_text_node.py
│   ├── ai_summary_node.py
│   ├── ai_keywords_node.py
│   ├── ai_extract_node.py
│   ├── ai_sentiment_node.py
│   ├── ai_code_node.py
│   └── file_export_node.py
├── requirements.txt
├── .env.example
└── 启动应用.bat
```

## 📄 License

MIT
