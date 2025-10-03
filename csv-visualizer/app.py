import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import random
import requests
import json

# ✅ 最先设置网页基础配置
st.set_page_config(page_title="数据平台 · 可视化 + 聊天机器人", layout="wide")

# 初始化验证状态
if "verified" not in st.session_state:
    st.session_state.verified = False

# 初始化验证码
if "captcha_a" not in st.session_state:
    st.session_state.captcha_a = random.randint(1, 9)
if "captcha_b" not in st.session_state:
    st.session_state.captcha_b = random.randint(1, 9)

# 验证逻辑
if not st.session_state.verified:
    st.title("🔒 安全验证 · 验证码")
    a = st.session_state.captcha_a
    b = st.session_state.captcha_b
    user_input = st.number_input(f"请输入答案：{a} + {b} = ?", step=1)

    if st.button("验证"):
        if user_input == a + b:
            st.session_state.verified = True
            st.rerun()  # 立即刷新页面
        else:
            st.error("验证失败，请再试一次 🛑")
    st.stop()  # 验证未通过时停止执行后续代码

# ✅ 模块一：📊 CSV 数据可视化平台
st.title("📊 CSV 数据可视化平台")

uploaded_file = st.file_uploader("请上传 CSV 文件", type=["csv"])
df = None  # 初始化 df

if not uploaded_file:
    if st.button("🚀 加载示例数据"):
        df = pd.DataFrame({
            "日期": pd.date_range("2023-01-01", periods=10),
            "销售额": [100, 120, 150, 170, 180, 160, 200, 220, 230, 250]
        })
        st.success("✅ 成功加载示例数据！")
    else:
        st.info("👋 请上传 CSV 文件或点击上方按钮加载示例数据")
elif uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="gbk")
    st.success("✅ 数据读取成功！")

if df is not None:
    st.subheader("📌 数据预览")
    st.dataframe(df)

    columns = df.columns.tolist()
    x_axis = st.selectbox("选择 X 轴", options=columns)
    y_axis = st.selectbox("选择 Y 轴", options=columns)

    chart_type = st.radio("选择图表类型", ["折线图", "柱状图", "散点图"])

    st.subheader("📈 可视化图表")
    if chart_type == "折线图":
        fig = px.line(df, x=x_axis, y=y_axis, title="折线图展示")
    elif chart_type == "柱状图":
        fig = px.bar(df, x=x_axis, y=y_axis, title="柱状图展示")
    else:
        fig = px.scatter(df, x=x_axis, y=y_axis, title="散点图展示")

    st.plotly_chart(fig, use_container_width=True)

# ✅ 模块二：🤖 DeepSeek 聊天机器人（Ollama 接口调用）
with st.expander("🤖 DeepSeek 聊天机器人"):
    st.markdown("在这里你可以与 DeepSeek 模型进行自然语言对话 ✨")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_prompt = st.text_input("你想问什么？", key="chat_input")

    if st.button("发送问题", key="send_btn"):
        if user_prompt:
            # 先显示用户消息
            st.session_state.chat_history.append(("你", user_prompt))
            
            # 创建占位符用于流式输出
            bot_message_placeholder = st.empty()
            full_response = ""
            
            try:
                # 使用流式请求
                response = requests.post(
                    "http://bc.x9x.top/api/generate",
                    json={
                        "model": "deepseek-r1:1.5b",
                        "prompt": user_prompt,
                        "stream": True  # 启用流式传输
                    },
                    stream=True,
                    timeout=60  # 延长超时时间
                )
                
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            try:
                                data = json.loads(line.decode('utf-8'))
                                chunk = data.get("response", "")
                                full_response += chunk
                                
                                # 实时更新显示（过滤掉<think>标签）
                                clean_response = full_response.replace("<think>", "").replace("</think>", "")
                                bot_message_placeholder.markdown(f"🤖 **DeepSeek**：{clean_response}")
                                
                            except json.JSONDecodeError:
                                continue
                    
                    # 最终保存完整响应（已过滤标签）
                    st.session_state.chat_history.append(("🤖 DeepSeek", clean_response))
                
                else:
                    st.error(f"API请求失败，状态码：{response.status_code}")
            
            except requests.exceptions.Timeout:
                st.error("请求超时，可能是响应时间过长，请尝试简化问题")
            except Exception as e:
                st.error(f"请求出错：{str(e)}")

    # 显示历史消息（过滤标签）
    for role, msg in st.session_state.chat_history:
        clean_msg = msg.replace("<think>", "").replace("</think>", "")
        if role == "你":
            st.markdown(f"👤 **{role}**：{clean_msg}")
        else:
            st.markdown(f"🤖 **{role}**：{clean_msg}")