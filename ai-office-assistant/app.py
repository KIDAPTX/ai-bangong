"""
AI智能办公助手 - 主程序入口
基于Streamlit构建Web交互界面，使用DeepSeek Function Calling驱动办公自动化
"""

import streamlit as st
from agent_core import run_agent

st.set_page_config(page_title="AI办公助手", page_icon="📊", layout="wide")
st.title("🤖 AI智能办公助手")
st.caption("用自然语言驱动Excel、Word、邮件自动化操作")

with st.sidebar:
    st.header("📋 使用说明")
    st.markdown("""
    1. **准备文件**：将要处理的Excel/Word文件放入 `data` 文件夹
    2. **输入需求**：用自然语言描述你的办公任务
    3. **开始执行**：点击按钮，AI自动完成操作
    
    **支持的操作：**
    - 📊 Excel表格合并汇总
    - 📝 Word文档批量生成
    - 📧 邮件批量发送
    - 🔗 多步骤任务自动串联
    
    **示例指令：**
    - "把data文件夹里的所有Excel文件合并"
    - "用data文件夹里的模板.docx和填充数据.xlsx生成文档"
    - "把data文件夹里的通讯录.xlsx里的联系人都发一份邮件，附件用合并总表.xlsx"
    - "把data文件夹里的所有Excel合并，然后用data里的模板.docx和填充数据.xlsx生成文档，最后把合并总表.xlsx作为附件发送给data里的通讯录.xlsx里的联系人"
    """)

st.subheader("📥 输入任务需求")
user_input = st.text_area(
    "请用自然语言描述您的办公任务：",
    placeholder="例如：帮我把data文件夹里的销售表合并，然后用模板.docx生成报告，最后发给通讯录.xlsx里的联系人",
    height=100
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    execute_btn = st.button("🚀 开始执行", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ 清空", use_container_width=True)

if clear_btn:
    st.rerun()

st.divider()
st.subheader("📤 执行结果")

if execute_btn:
    if user_input.strip() == "":
        st.warning("⚠️ 请先输入任务描述")
    else:
        with st.spinner("🤔 AI正在分析您的需求并执行操作..."):
            try:
                result = run_agent(user_input)
                st.success("✅ 任务完成！")
                st.info(result)
            except Exception as e:
                st.error(f"❌ 执行出错：{str(e)}")
                st.info("💡 提示：请检查文件路径是否正确、API密钥是否有效、网络是否正常")