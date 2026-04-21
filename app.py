"""
AI 工作流自动化平台 - 主界面
"""
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import json
import time
from workflow_engine import WorkflowEngine
from nodes import NODE_REGISTRY

# 导入所有节点模块以触发注册
import nodes.input_node
import nodes.web_scrape_node
import nodes.file_upload_node
import nodes.ai_text_node
import nodes.ai_summary_node
import nodes.ai_keywords_node
import nodes.ai_extract_node
import nodes.ai_sentiment_node
import nodes.ai_code_node
import nodes.file_export_node

st.set_page_config(
    page_title="AI 工作流平台",
    page_icon="⚡",
    layout="wide"
)

# ==================== 全局样式 ====================
st.markdown("""
<style>
    /* ===== 隐藏 Streamlit 自带白条/装饰 ===== */
    header[data-testid="stHeader"] {
        background: rgba(245,247,250,0) !important;
    }
    [data-testid="stToolbar"] {
        background: rgba(245,247,250,0) !important;
    }
    footer[data-testid="stFooter"] {
        background: rgba(245,247,250,0) !important;
    }
    footer[data-testid="stFooter"] > div {
        min-height: 0 !important;
        padding: 0 !important;
    }
    /* 去掉 Streamlit 默认的顶部汉堡菜单和部署按钮的白色背景条 */
    [data-testid="stDecoration"] {
        display: none !important;
    }
    /* 去掉侧边栏底部的空白 */
    [data-testid="stSidebar"] > div:last-child {
        min-height: 0 !important;
    }
    
    /* ===== 强制浅色主题：覆盖所有 Streamlit 原生组件 ===== */
    
    /* 整体背景 */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f0 100%);
        color: #1e293b;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: white;
        color: #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
    
    /* ===== 按钮统一改浅色 ===== */
    
    /* 主内容区按钮（非 primary） */
    .stButton > button[kind="secondary"],
    .stButton > button:not([kind]) {
        background: #f1f5f9 !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px;
        transition: all 0.2s;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button:not([kind]):hover {
        background: #e2e8f0 !important;
        color: #1e293b !important;
        border-color: #cbd5e1 !important;
    }
    
    /* Primary 按钮 */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px;
    }
    .stButton > button[kind="primary"]:hover {
        opacity: 0.9;
    }
    
    /* 侧边栏按钮 */
    [data-testid="stSidebar"] .stButton > button {
        background: #f1f5f9 !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #e8edf5 !important;
        color: #1e293b !important;
        border-color: #667eea !important;
        transform: translateX(4px);
    }
    
    /* ===== Radio（Tab 导航）===== */
    .stRadio > div > label > div {
        background: #f1f5f9 !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
    }
    .stRadio > div > label > div:hover {
        background: #e8edf5 !important;
        border-color: #667eea !important;
    }
    .stRadio > div > label > div[data-checked="true"],
    .stRadio > div[aria-checked="true"] > label > div,
    .stRadio > div > label > div.pxcVml {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: transparent !important;
    }
    
    /* ===== 全局 Label 文字强制深色 ===== */
    .stSelectbox label, .stTextInput label, .stTextArea label,
    .stNumberInput label, .stCheckbox label, .stRadio label,
    .stSlider label, .stFileUploader label {
        color: #1e293b !important;
    }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: #1e293b !important;
    }
    .stSelectbox > div > div > label,
    .stTextInput > div > div > label,
    .stTextArea > div > div > label {
        color: #1e293b !important;
    }
    /* 确保所有小标题、caption、标签都是深色 */
    h2, h3, h4, h5, h6, p, span, div, li, td, th, label {
        color: #1e293b;
    }
    st-markdown p, st-markdown span, st-markdown li {
        color: #1e293b !important;
    }
    
    /* ===== Selectbox / Dropdown 美化 ===== */
    [data-testid="stSelectbox"] > div > div {
        background: white !important;
        color: #334155 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSelectbox"] > div > div:hover {
        border-color: #a5b4fc !important;
        box-shadow: 0 2px 12px rgba(102,126,234,0.1) !important;
    }
    [data-testid="stSelectbox"] svg {
        fill: #64748b !important;
    }
    /* Selectbox 下拉选项面板 - 终极覆盖 */
    [data-testid="stSelectbox"] + div,
    [data-testid="stSelectbox"] + div > div,
    [data-testid="stSelectbox"] + div > div > div,
    [data-testid="stSelectbox"] ~ div,
    [data-testid="stSelectbox"] ~ div > div,
    [data-testid="stSelectbox"] ~ div > div > div {
        background-color: white !important;
        background: white !important;
    }
    /* BaseWeb 下拉菜单容器 */
    .stSelectbox [class*="popover"],
    .stSelectbox [class*="menu"],
    .stSelectbox [class*="listbox"],
    .stSelectbox [class*="dropdown"] {
        background-color: white !important;
        color: #1e293b !important;
    }
    .stSelectbox [class*="menu"] [class*="option"],
    .stSelectbox [class*="menu"] li {
        background-color: white !important;
        color: #1e293b !important;
    }
    .stSelectbox [class*="menu"] [class*="option"]:hover,
    .stSelectbox [class*="menu"] li:hover {
        background-color: #f1f5f9 !important;
    }
    /* BaseWeb Select 内部文字 */
    [data-testid="stSelectbox"] span {
        color: #1e293b !important;
    }
    
    /* ===== Text Input 美化 ===== */
    [data-testid="stTextInput"] > div > div {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stTextInput"] > div > div:hover {
        border-color: #a5b4fc !important;
    }
    [data-testid="stTextInput"] > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.15) !important;
    }
    [data-testid="stTextInput"] input {
        background: transparent !important;
        color: #1e293b !important;
        font-size: 14px !important;
    }
    
    /* ===== Text Area 美化 ===== */
    [data-testid="stTextArea"] > div > div {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stTextArea"] > div > div:hover {
        border-color: #a5b4fc !important;
    }
    [data-testid="stTextArea"] > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.15) !important;
    }
    [data-testid="stTextArea"] textarea {
        background: transparent !important;
        color: #1e293b !important;
        font-size: 14px !important;
        min-height: 150px !important;
    }
    [data-testid="stTextArea"] textarea::placeholder {
        color: #94a3b8 !important;
    }
    [data-testid="stTextInput"] input::placeholder {
        color: #94a3b8 !important;
    }
    
    /* ===== Expander ===== */
    [data-testid="stExpander"] {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }
    [data-testid="stExpander"] > div > summary,
    [data-testid="stExpander"] > div > summary > p,
    [data-testid="stExpander"] > div > summary > span {
        color: #1e293b !important;
    }
    
    /* ===== Info / Success / Warning / Error 框 ===== */
    [data-testid="stAlert"] {
        background: #f0f7ff !important;
        color: #1e293b !important;
        border-left-color: #667eea !important;
    }
    
    /* ===== 滚动条美化 ===== */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* ===== 自定义组件样式 ===== */
    
    /* 主内容区 */
    .main-content {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }
    
    /* 节点卡片 */
    .workflow-node {
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        transition: all 0.3s ease;
    }
    .workflow-node:hover {
        border-left-color: #764ba2;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.12);
        transform: translateY(-1px);
    }
    
    /* 节点类型标签 */
    .node-type-input {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .node-type-ai {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .node-type-output {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    /* 连接箭头 */
    .arrow-down {
        text-align: center;
        font-size: 24px;
        margin: 4px 0;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* 结果卡片 */
    .result-card-success {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border: 1px solid #a5d6a7;
        border-radius: 12px;
        padding: 20px;
    }
    .result-card-error {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border: 1px solid #ef9a9a;
        border-radius: 12px;
        padding: 20px;
    }
    .result-card-node {
        background: #f8f9fa;
        border-left: 3px solid #667eea;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    
    /* 模板卡片 */
    .template-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s;
        margin-bottom: 12px;
        color: #1e293b;
    }
    .template-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
    }
    
    /* 隐藏默认 padding */
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* 运行进度条 */
    .progress-step {
        display: flex;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .progress-step:last-child {
        border-bottom: none;
    }
    
    /* 表格文字颜色 */
    [data-testid="stTable"] td,
    [data-testid="stTable"] th {
        color: #1e293b !important;
    }
    
    /* Markdown 区域文字 */
    .stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown div {
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 初始化 session state ====================
if "workflow" not in st.session_state:
    st.session_state.workflow = WorkflowEngine()
if "run_result" not in st.session_state:
    st.session_state.run_result = None
if "saved_workflows" not in st.session_state:
    st.session_state.saved_workflows = [
        {
            "name": "翻译 + 摘要",
            "description": "将文本翻译成英文，然后生成摘要",
            "nodes": [
                {"type": "text_input", "config": {"text": ""}},
                {"type": "ai_text", "config": {"task_type": "翻译成英文", "custom_prompt": ""}},
                {"type": "ai_summary", "config": {"style": "简洁摘要（3-5句话）"}},
            ]
        },
        {
            "name": "网页内容分析",
            "description": "抓取网页正文，提取摘要和关键词",
            "nodes": [
                {"type": "web_scrape", "config": {"url": "https://"}},
                {"type": "ai_summary", "config": {"style": "要点列表"}},
                {"type": "ai_keywords", "config": {"max_count": "10"}},
            ]
        },
        {
            "name": "代码解释 + 优化",
            "description": "审查代码并提供改进建议，导出报告",
            "nodes": [
                {"type": "text_input", "config": {"text": ""}},
                {"type": "ai_code", "config": {"code_task": "代码审查", "language": "Python"}},
                {"type": "file_export", "config": {"format": "TXT", "filename": "code_review"}},
            ]
        },
        {
            "name": "情感分析流程",
            "description": "分析文本情感，提取关键词并生成总结",
            "nodes": [
                {"type": "text_input", "config": {"text": ""}},
                {"type": "ai_sentiment", "config": {"detail_level": "详细（含情绪分析）"}},
                {"type": "ai_keywords", "config": {"max_count": "5"}},
                {"type": "ai_summary", "config": {"style": "简洁摘要（3-5句话）"}},
            ]
        },
    ]

# ==================== 顶部 Header ====================
header_col1, header_col2 = st.columns([1, 4])
with header_col1:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:36px;">⚡</span>
        <div>
            <h1 style="margin:0;font-size:24px;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">AI 工作流平台</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
with header_col2:
    st.markdown("""
    <p style="color:#64748b;margin-top:24px;">可视化编排 AI 工作流 · 10 种智能节点 · 模板一键加载 · 实时运行预览</p>
    """, unsafe_allow_html=True)

# ==================== Tab 导航 ====================
active_tab = st.session_state.get("active_tab", 0)
tab_names = ["🔧 创建工作流", "📁 模板库", "📖 使用指南"]
tab_icons = ["🔧", "📁", "📖"]

# 用 CSS 自定义 tab 样式
selected = st.radio(
    "", tab_names, index=active_tab, horizontal=True, label_visibility="collapsed"
)

tab_create = selected == tab_names[0]
tab_templates = selected == tab_names[1]
tab_guide = selected == tab_names[2]

# ==================== Tab 1: 创建工作流 ====================
if tab_create:
    # 侧边栏：节点选择
    with st.sidebar:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:16px;border-radius:12px;margin-bottom:16px;">
            <h3 style="margin:0;font-size:16px;">📦 可用节点</h3>
            <p style="margin:4px 0 0;font-size:12px;opacity:0.85;">点击添加到工作流</p>
        </div>
        """, unsafe_allow_html=True)
        
        node_categories = {
            "📥 输入源": ("node-type-input", ["text_input", "web_scrape", "file_upload"]),
            "🤖 AI 处理": ("node-type-ai", ["ai_text", "ai_summary", "ai_keywords", "ai_extract", "ai_sentiment", "ai_code"]),
            "📤 输出": ("node-type-output", ["file_export"]),
        }
        
        for category, (badge_class, node_types) in node_categories.items():
            st.markdown(f"**{category}**")
            for node_type in node_types:
                node_class = NODE_REGISTRY.get(node_type)
                if node_class:
                    node = node_class()
                    if st.button(f"{node.icon} {node.name}", key=f"add_{node_type}", use_container_width=True):
                        default_config = {}
                        for field in node.config_fields:
                            default_config[field["key"]] = field.get("default", "")
                        st.session_state.workflow.add_node({"type": node_type, "config": default_config})
                        st.rerun()
            st.markdown('<div style="margin:4px 0;"></div>', unsafe_allow_html=True)
    
    # 主内容区：上下布局（透明包裹，不显示白条）
    st.markdown('<div style="display:none">', unsafe_allow_html=True)
    
    # ---- 上半部分：工作流编辑 + 运行结果 ----
    workflow_col, result_col = st.columns([1.2, 1])
    
    with workflow_col:
        # 操作栏
        bar1, bar2, bar3, bar4 = st.columns([1, 1, 1, 1])
        with bar1:
            if st.button("🗑️ 清空", use_container_width=True):
                st.session_state.workflow.clear()
                st.session_state.run_result = None
                st.rerun()
        with bar2:
            if st.button("⬆️ 上移节点", use_container_width=True, disabled=len(st.session_state.workflow.nodes) < 2):
                n = len(st.session_state.workflow.nodes)
                st.session_state.workflow.nodes[-1], st.session_state.workflow.nodes[-2] = \
                    st.session_state.workflow.nodes[-2], st.session_state.workflow.nodes[-1]
                st.rerun()
        with bar3:
            if st.button("⬇️ 下移节点", use_container_width=True, disabled=len(st.session_state.workflow.nodes) < 2):
                n = len(st.session_state.workflow.nodes)
                st.session_state.workflow.nodes[0], st.session_state.workflow.nodes[1] = \
                    st.session_state.workflow.nodes[1], st.session_state.workflow.nodes[0]
                st.rerun()
        with bar4:
            if st.button("💾 存为模板", use_container_width=True, disabled=len(st.session_state.workflow.nodes) == 0):
                        st.session_state.show_save_dialog = True
        
        st.markdown('<div style="margin:8px 0;"></div>', unsafe_allow_html=True)
        
        # 工作流节点
        nodes = st.session_state.workflow.nodes
        if not nodes:
            st.markdown("""
            <div style="text-align:center;padding:40px 20px;color:#94a3b8;">
                <p style="font-size:48px;margin-bottom:12px;">🔗</p>
                <p style="font-size:16px;">从左侧选择节点添加到工作流</p>
                <p style="font-size:13px;">或从「模板库」加载预置模板</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 工作流统计
            st.markdown(f"**工作流** · {len(nodes)} 个节点")
            
            for i, node_config in enumerate(nodes):
                node_type = node_config.get("type")
                node_class = NODE_REGISTRY.get(node_type)
                if not node_class:
                    continue
                node = node_class()
                
                # 节点类型分类
                if node_type in ["text_input", "web_scrape", "file_upload"]:
                    badge = '<span class="node-type-input">输入</span>'
                elif node_type == "file_export":
                    badge = '<span class="node-type-output">输出</span>'
                else:
                    badge = '<span class="node-type-ai">AI</span>'
                
                # 节点头部
                header_cols = st.columns([1, 8, 1])
                with header_cols[0]:
                    st.markdown(f"<p style='font-size:28px;margin:0;text-align:center;'>{node.icon}</p>", unsafe_allow_html=True)
                with header_cols[1]:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;">
                        <strong style="font-size:15px;">节点 {i+1}：{node.name}</strong>
                        {badge}
                    </div>
                    <p style="color:#94a3b8;font-size:13px;margin:2px 0 0;">{node.description}</p>
                    """, unsafe_allow_html=True)
                with header_cols[2]:
                    if st.button("❌", key=f"del_{i}", help="删除节点"):
                        st.session_state.workflow.remove_node(i)
                        st.session_state.run_result = None
                        st.rerun()
                
                # 节点配置（更大的输入框）
                if node.config_fields:
                    config = node_config.get("config", {})
                    for j, field in enumerate(node.config_fields):
                        key = field["key"]
                        label = field["label"]
                        field_type = field.get("type", "text")
                        
                        if field_type == "select":
                            options = field.get("options", [])
                            current = config.get(key, options[0] if options else "")
                            idx = options.index(current) if current in options else 0
                            new_val = st.selectbox(
                                label, options, index=idx, key=f"cfg_{i}_{key}"
                            )
                        elif field_type == "text":
                            # 根据字段决定高度
                            if key in ["text", "content", "custom_prompt"]:
                                h = 200
                            else:
                                h = 120
                            new_val = st.text_area(
                                label, value=config.get(key, ""), 
                                key=f"cfg_{i}_{key}", height=h,
                                placeholder=f"请输入{label}..."
                            )
                        else:
                            new_val = st.text_input(
                                label, value=config.get(key, ""),
                                key=f"cfg_{i}_{key}"
                            )
                        
                        node_config["config"][key] = new_val
                
                # 文件上传节点特殊处理
                if node_type == "file_upload":
                    accept_types = node.accept_types
                    accept_str = ",".join(accept_types)
                    uploaded_file = st.file_uploader(
                        "选择文件",
                        type=[t.replace(".", "") for t in accept_types],
                        key=f"upload_{i}",
                        label_visibility="visible"
                    )
                    if uploaded_file:
                        file_bytes = uploaded_file.read()
                        node_config["config"]["file_bytes"] = file_bytes
                        node_config["config"]["filename"] = uploaded_file.name
                        ext = os.path.splitext(uploaded_file.name.lower())[1]
                        type_name = nodes.file_upload_node.EXTRACTORS.get(ext, ("未知", None))[0]
                        size_kb = len(file_bytes) / 1024
                        st.success(f"已加载: {uploaded_file.name} ({type_name}, {size_kb:.1f} KB)")
                    else:
                        # 清除之前的文件数据
                        node_config["config"].pop("file_bytes", None)
                        node_config["config"].pop("filename", None)
                
                # 连接箭头
                if i < len(nodes) - 1:
                    st.markdown('<div class="arrow-down">↓</div>', unsafe_allow_html=True)
    
    with result_col:
        st.markdown("**📊 运行结果**")
        
        result = st.session_state.run_result
        if result is None:
            st.markdown("""
            <div style="text-align:center;padding:40px 20px;color:#94a3b8;">
                <p style="font-size:48px;margin-bottom:12px;">📋</p>
                <p style="font-size:16px;">运行工作流后这里会显示结果</p>
                <p style="font-size:13px;">每个节点的执行状态和输出都会展示</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            if result["success"]:
                st.markdown("""
                <div class="result-card-success">
                    <p style="margin:0;font-size:15px;"><strong>✅ 工作流执行成功！</strong></p>
                    <p style="margin:4px 0 0;font-size:13px;color:#2e7d32;">所有节点均已成功运行</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-card-error">
                    <p style="margin:0;font-size:15px;"><strong>❌ 工作流执行失败</strong></p>
                    <p style="margin:4px 0 0;font-size:13px;color:#c62828;">部分节点执行出错，请检查配置</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 节点执行详情
            with st.expander("📋 节点执行详情", expanded=True):
                for nr in result.get("node_results", []):
                    if nr["success"]:
                        st.markdown(f"""
                        <div class="result-card-node">
                            <strong>{nr['icon']} {nr['name']}</strong> 
                            <span style="color:#667eea;font-size:12px;">✓ {nr['elapsed']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-card-node" style="border-left-color:#f44336;">
                            <strong>{nr['icon']} {nr['name']}</strong> 
                            <span style="color:#f44336;font-size:12px;">✗ 失败</span>
                            <br><span style="color:#f44336;font-size:12px;">{nr.get('error', '未知错误')}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            # 最终输出（更大的展示区域）
            st.markdown("**最终输出：**")
            output_text = result['output']
            st.text_area("输出结果", value=output_text, height=400, label_visibility="collapsed", key="final_output")
            
            if len(output_text) > 2000:
                st.caption(f"共 {len(output_text)} 字符")
            
            # 操作按钮
            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("📋 复制结果", use_container_width=True):
                    st.clipboard_copy(output_text)
                    st.success("已复制到剪贴板！")
            with btn2:
                if st.button("📥 导出为 TXT", use_container_width=True):
                    st.download_button(
                        label="点击下载",
                        data=output_text.encode("utf-8"),
                        file_name="workflow_result.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ---- 下半部分：输入与运行 ----
    st.markdown('<div style="display:none">', unsafe_allow_html=True)
    
    nodes = st.session_state.workflow.nodes
    if nodes:
        first_type = nodes[0].get("type") if nodes else None
        
        run_col1, run_col2, run_col3 = st.columns([3, 1, 1])
        
        with run_col1:
            if first_type != "text_input":
                initial_input = st.text_area(
                    "📥 工作流输入",
                    placeholder="输入工作流的起始内容...",
                    height=150,
                    label_visibility="visible"
                )
            else:
                initial_input = ""
                st.info("💡 第一个节点是「文本输入」，请直接在节点中填写内容")
        
        with run_col2:
            if st.button("🚀 运行工作流", type="primary", use_container_width=True):
                with st.spinner("正在执行工作流..."):
                    st.session_state.run_result = st.session_state.workflow.run(initial_input)
                st.rerun()
        
        with run_col3:
            if st.session_state.run_result:
                if st.button("🔄 清除结果", use_container_width=True):
                    st.session_state.run_result = None
                    st.rerun()
    else:
        st.info("请先添加节点到工作流")
    
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== Tab 2: 模板库 ====================
if tab_templates:
    if "active_tab" in st.session_state:
        del st.session_state.active_tab
    
    st.markdown("""
    <div style="margin-bottom:20px;">
        <h2 style="margin:0;">📁 工作流模板库</h2>
        <p style="color:#64748b;margin:4px 0 0;">选择一个模板快速开始，也可以在「创建工作流」中保存自己的模板</p>
    </div>
    """, unsafe_allow_html=True)
    
    for idx, wf in enumerate(st.session_state.saved_workflows):
        # 构建节点流程图
        node_steps = []
        for n in wf["nodes"]:
            nc = NODE_REGISTRY.get(n.get("type"))
            if nc:
                node = nc()
                node_steps.append(f"{node.icon} {node.name}")
        
        flow_text = " → ".join(node_steps)
        desc = wf.get("description", "")
        
        st.markdown(f"""
        <div class="template-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <strong style="font-size:17px;">{wf['name']}</strong>
                    {f'<p style="color:#64748b;font-size:13px;margin:4px 0 8px;">{desc}</p>' if desc else ''}
                    <p style="font-size:13px;color:#667eea;">{flow_text}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 使用此模板", key=f"use_template_{idx}", use_container_width=True):
            st.session_state.workflow.clear()
            st.session_state.run_result = None
            for n in wf["nodes"]:
                st.session_state.workflow.add_node(dict(n))
            st.session_state.active_tab = 0
            st.rerun()


# ==================== Tab 3: 使用指南 ====================
if tab_guide:
    if "active_tab" in st.session_state:
        del st.session_state.active_tab
    
    st.markdown("""
    <div style="margin-bottom:20px;">
        <h2 style="margin:0;">📖 使用指南</h2>
        <p style="color:#64748b;margin:4px 0 0;">了解如何使用 AI 工作流平台</p>
    </div>
    """, unsafe_allow_html=True)
    
    guide1, guide2 = st.columns(2)
    
    with guide1:
        st.markdown("""
        <div class="main-content">
            <h3>🚀 快速上手</h3>
            <ol style="line-height:2.2;color:#1e293b;">
                <li><strong>添加节点</strong> — 从左侧面板点击节点按钮</li>
                <li><strong>配置参数</strong> — 设置每个节点的处理选项</li>
                <li><strong>输入内容</strong> — 在底部输入起始内容</li>
                <li><strong>运行</strong> — 点击「运行工作流」</li>
                <li><strong>查看结果</strong> — 右侧显示执行状态和输出</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with guide2:
        st.markdown("""
        <div class="main-content">
            <h3>💡 小技巧</h3>
            <ul style="line-height:2.2;color:#1e293b;">
                <li>不知道怎么搭配？试试「模板库」里的预置模板</li>
                <li>创建好的工作流可以「存为模板」方便复用</li>
                <li>结果支持一键复制或导出为 TXT 文件</li>
                <li>支持上下移动节点调整执行顺序</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-content">
        <h3>🧩 节点说明</h3>
        <table style="width:100%;border-collapse:collapse;color:#1e293b;">
            <tr style="background:#f8f9fa;">
                <th style="text-align:left;padding:12px;border-radius:8px 0 0 0;">节点</th>
                <th style="text-align:left;padding:12px;">功能</th>
                <th style="text-align:left;padding:12px;">示例用途</th>
            </tr>
            <tr style="border-bottom:1px solid #eee;">
                <td style="padding:10px 12px;">📝 文本输入</td>
                <td style="padding:10px 12px;">输入起始文本</td>
                <td style="padding:10px 12px;">作为工作流的起点</td>
            </tr>
            <tr style="background:#fafafa;border-bottom:1px solid #eee;">
                <td style="padding:10px 12px;">🌐 网页抓取</td>
                <td style="padding:10px 12px;">抓取网页正文</td>
                <td style="padding:10px 12px;">获取新闻、文章内容</td>
            </tr>
            <tr style="border-bottom:1px solid #eee;">
                <td style="padding:10px 12px;">🤖 AI 文本处理</td>
                <td style="padding:10px 12px;">翻译/润色/改写</td>
                <td style="padding:10px 12px;">多语言翻译、文案优化</td>
            </tr>
            <tr style="background:#fafafa;border-bottom:1px solid #eee;">
                <td style="padding:10px 12px;">📋 AI 摘要总结</td>
                <td style="padding:10px 12px;">生成文本摘要</td>
                <td style="padding:10px 12px;">长文精读、会议纪要</td>
            </tr>
            <tr style="border-bottom:1px solid #eee;">
                <td style="padding:10px 12px;">🏷️ 关键词提取</td>
                <td style="padding:10px 12px;">提取关键词标签</td>
                <td style="padding:10px 12px;">SEO 优化、内容分类</td>
            </tr>
            <tr style="background:#fafafa;border-bottom:1px solid #eee;">
                <td style="padding:10px 12px;">📊 AI 数据提取</td>
                <td style="padding:10px 12px;">提取结构化信息</td>
                <td style="padding:10px 12px;">从文章中提取人名、数字</td>
            </tr>
            <tr style="border-bottom:1px solid #eee;">
                <td style="padding:10px 12px;">😎 AI 情感分析</td>
                <td style="padding:10px 12px;">分析情感倾向</td>
                <td style="padding:10px 12px;">评论分析、舆情监控</td>
            </tr>
            <tr style="background:#fafafa;border-bottom:1px solid #eee;">
                <td style="padding:10px 12px;">💻 AI 代码助手</td>
                <td style="padding:10px 12px;">解释/生成/审查代码</td>
                <td style="padding:10px 12px;">代码学习、Code Review</td>
            </tr>
            <tr>
                <td style="padding:10px 12px;border-radius:0 0 0 8px;">📤 导出文件</td>
                <td style="padding:10px 12px;">保存为文件</td>
                <td style="padding:10px 12px;">归档工作流结果</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
