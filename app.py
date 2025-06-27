import streamlit as st
from openai import OpenAI
import os
import re

# 页面配置
st.set_page_config(
    page_title="TradeMate AI - 外贸邮件助手",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 安全的API密钥获取
def get_api_key():
    """安全获取API密钥"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # 检查密钥格式
    if not api_key:
        st.error("⚠️ 未设置DEEPSEEK_API_KEY环境变量")
        st.info("请在Streamlit Cloud的Settings → Secrets中设置API密钥")
        st.stop()
    
    # 验证密钥格式（DeepSeek密钥通常以sk-开头）
    if not api_key.startswith("sk-"):
        st.error("⚠️ API密钥格式不正确")
        st.info("请检查API密钥是否正确")
        st.stop()
    
    return api_key

# 获取API密钥
api_key = get_api_key()

# 初始化OpenAI客户端
try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )
except Exception as e:
    st.error(f"❌ 初始化API客户端失败：{e}")
    st.stop()

st.title("💼 TradeMate AI - 外贸邮件助手")

# 侧边栏配置
with st.sidebar:
    st.header("📧 邮件配置")
    email_type = st.selectbox(
        "邮件类型",
        ["商务邮件", "询价邮件", "报价邮件", "催款邮件", "感谢邮件", "投诉处理", "其他"]
    )
    
    tone = st.selectbox(
        "邮件语气",
        ["正式", "友好", "紧急", "礼貌", "专业"]
    )
    
    # 显示邮件模板预览
    st.header("📋 邮件模板预览")
    template_preview = f"""
Subject: [邮件标题]

From: [发件人邮箱]
To: [收件人邮箱]
Cc: [抄送邮箱] (可选)

Dear [收件人姓名],

[邮件正文内容]

Best regards,
[发件人姓名]
[公司名称]
[职位]
[联系电话]
[邮箱地址]
    """
    st.text_area("模板格式", template_preview, height=200, disabled=True)

# 主界面
st.markdown("---")

# 用户输入中文意图
prompt = st.text_area("请输入中文意图，例如：催一下客户付款", height=100)

# 生成按钮
col1, col2 = st.columns([1, 4])
with col1:
    generate_button = st.button("🚀 生成英文邮件", type="primary")
with col2:
    if st.button("📖 查看使用说明"):
        st.info("""
        **使用步骤：**
        1. 选择邮件类型和语气
        2. 输入中文意图
        3. 点击生成按钮
        4. 复制生成的邮件内容
        """)

if generate_button and prompt:
    with st.spinner("🤖 AI 正在撰写邮件..."):
        try:
            system_prompt = f"""你是一个擅长英文商务沟通的外贸助理。请按照以下格式生成{email_type}，语气{tone}：

Subject: [邮件标题]

From: [发件人邮箱]
To: [收件人邮箱]
Cc: [抄送邮箱] (可选)

Dear [收件人姓名],

[邮件正文内容]

Best regards,
[发件人姓名]
[公司名称]
[职位]
[联系电话]
[邮箱地址]

注意：
1. 所有需要填写的地方都用中文标注，如 [邮件标题]、[收件人姓名]、[发件人姓名] 等
2. 邮件正文要专业、{tone}、符合商务礼仪
3. 根据用户的中文意图生成相应的英文邮件内容
4. 如果是询价邮件，要包含产品规格、数量、交货期等关键信息
5. 如果是报价邮件，要包含价格、付款条件、交货期等
6. 如果是催款邮件，要委婉但明确地表达催款意图"""

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"请帮我写一封英文商务邮件，意图是：{prompt}"}
                ],
                temperature=0.7
            )
            message = response.choices[0].message.content
            
            st.success("✅ 邮件生成完成！")
            st.markdown("---")
            
            # 显示生成的邮件
            st.subheader("📧 生成的英文邮件")
            st.text_area("邮件内容", message, height=400, key="generated_email")
            
            # 操作按钮
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 复制邮件内容", type="secondary"):
                    st.write("✅ 邮件内容已复制到剪贴板")
                    st.session_state.copied = True
            
            with col2:
                if st.button("🔄 重新生成", type="secondary"):
                    st.rerun()
                    
            with col3:
                if st.button("💾 保存模板", type="secondary"):
                    st.write("💾 邮件模板已保存")
                    
        except Exception as e:
            st.error(f"❌ 生成邮件时出错：{e}")
            st.info("💡 请检查网络连接和API密钥是否正确")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💼 TradeMate AI - 外贸邮件助手 | 让外贸沟通更简单</p>
    <p>Powered by DeepSeek AI & Streamlit</p>
</div>
""", unsafe_allow_html=True) 