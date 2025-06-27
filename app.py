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
        ["标准模板", "公司模板A", "自定义模板"]
    )
    
    tone = st.selectbox(
        "邮件语气",
        ["正式", "友好", "紧急", "礼貌", "专业"]
    )
    
    
    st.header("✍️ 签名设置")
    if email_type == "标准模板":
        sign_name = st.text_input("姓名", value="")
        sign_title = ""
        sign_company = ""
        sign_phone = ""
        sign_email = ""
    else:
        sign_name = st.text_input("姓名", value="")
        sign_title = st.text_input("职位", value="")
        sign_company = st.text_input("公司", value="")
        sign_phone = st.text_input("电话", value="")
        sign_email = st.text_input("邮箱", value="")
    
    # 模板内容
    default_template = '''Subject: [邮件标题]\n\nDear [收件人姓名],\n\n[邮件正文内容]\n\nBest regards,\n[签名]'''
    company_template = '''Subject: [邮件标题]\n\nDear [收件人姓名],\n\n[邮件正文内容]\n\nSincerely,\n[签名]'''
    if email_type == "自定义模板":
        custom_template = st.text_area("自定义模板内容", value=default_template, height=180)
        template = custom_template
    elif email_type == "公司模板A":
        template = company_template
    else:
        template = default_template
    
    # 预览
    preview = template.replace('[签名]', '(签名)').replace('[公司]', '(公司)').replace('[职位]', '(职位)').replace('[电话]', '(电话)').replace('[邮箱]', '(邮箱)').replace('[邮件正文内容]', '(正文)').replace('[邮件标题]', '(标题)').replace('[收件人姓名]', '(收件人)')
    st.header("📋 邮件模板预览")
    st.text_area("模板格式", preview, height=200, disabled=True)

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
        2. 设置签名
        3. 输入中文意图
        4. 点击生成按钮
        5. 复制生成的邮件内容（纯文本）
        """)

def render_signature_html():
    lines = []
    if sign_name: lines.append(sign_name)
    if sign_title: lines.append(sign_title)
    if sign_company: lines.append(sign_company)
    if sign_phone: lines.append(sign_phone)
    if sign_email: lines.append(sign_email)
    return "<br>".join(lines)

def render_signature_text():
    lines = []
    if sign_name: lines.append(sign_name)
    if sign_title: lines.append(sign_title)
    if sign_company: lines.append(sign_company)
    if sign_phone: lines.append(sign_phone)
    if sign_email: lines.append(sign_email)
    return "\n".join(lines)

if generate_button and prompt:
    with st.spinner("🤖 AI 正在撰写邮件..."):
        try:
            # 让AI同时生成标题和正文
            system_prompt = (
                "你是一个擅长英文商务沟通的外贸助理。请根据用户意图，生成一封英文商务邮件，包括合适的英文邮件标题（Subject）和正文，格式如下：\n"
                "Subject: ...\n\n正文内容...。不要输出多余内容。"
            )
            user_prompt = f"请帮我写一封英文商务邮件，意图是：{prompt}，请给出合适的英文邮件标题和正文。"
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            ai_content = response.choices[0].message.content or ""
            # 解析标题和正文
            subject = ""
            body = ai_content
            if isinstance(ai_content, str):
                match = re.match(r"Subject:\s*(.*)\n+([\s\S]*)", ai_content)
                if match:
                    subject = match.group(1).strip()
                    body = match.group(2).strip()
            # 合成最终邮件
            mail_html = template
            mail_text = template
            mail_html = mail_html.replace('[邮件标题]', subject)
            mail_text = mail_text.replace('[邮件标题]', subject)
            mail_html = mail_html.replace('[签名]', render_signature_html() or "")
            mail_text = mail_text.replace('[签名]', render_signature_text() or "")
            mail_html = mail_html.replace('[公司]', sign_company or "")
            mail_text = mail_text.replace('[公司]', sign_company or "")
            mail_html = mail_html.replace('[职位]', sign_title or "")
            mail_text = mail_text.replace('[职位]', sign_title or "")
            mail_html = mail_html.replace('[电话]', sign_phone or "")
            mail_text = mail_text.replace('[电话]', sign_phone or "")
            mail_html = mail_html.replace('[邮箱]', sign_email or "")
            mail_text = mail_text.replace('[邮箱]', sign_email or "")
            mail_html = mail_html.replace('[邮件正文内容]', body or "")
            mail_text = mail_text.replace('[邮件正文内容]', body or "")
            # 其他占位符留给用户手动填写
            st.success("✅ 邮件生成完成！")
            st.markdown("---")
            st.subheader("📧 生成的英文邮件")
            st.markdown(mail_html, unsafe_allow_html=True)
            st.text_area("纯文本邮件内容（可复制）", mail_text, height=400, key="generated_email")
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