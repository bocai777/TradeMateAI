# TradeMate AI - 外贸邮件助手

一个基于Streamlit和DeepSeek AI的外贸邮件生成工具，帮助外贸人员更好地与外国客户沟通。

## 功能特点

- 🚀 快速生成专业的英文商务邮件
- 💼 针对外贸场景优化
- 🌍 支持多种商务沟通场景
- 🎯 友好的中文界面

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置API密钥

建议将API密钥设置为环境变量：

```bash
# Windows
set DEEPSEEK_API_KEY=your_api_key_here

# Linux/Mac
export DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 运行应用

```bash
streamlit run app.py
```

## 使用方法

1. 在文本框中输入中文意图（例如："催一下客户付款"）
2. 点击"生成英文邮件"按钮
3. 等待AI生成专业的英文商务邮件
4. 复制生成的邮件内容使用

## 注意事项

- 请确保您的DeepSeek API密钥有效且有足够的额度
- 生成的邮件内容仅供参考，建议根据实际情况进行调整
- 请遵守相关法律法规和商业道德

## 技术栈

- **前端框架**: Streamlit
- **AI服务**: DeepSeek API
- **语言**: Python 