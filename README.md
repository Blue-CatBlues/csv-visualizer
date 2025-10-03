# 📊 CSV 数据可视化平台 · Streamlit + Docker

一个轻量级的 Web 数据平台，支持 CSV 文件上传、图表生成与安全验证。基于python + Streamlit 构建，支持本地运行与 Docker 部署，适合快速搭建数据展示界面。

---

## 🚀 功能亮点

- 🔒 **验证码验证机制**：防止恶意访问，保障平台安全
- 📁 **CSV 文件上传**：支持 GBK 编码，兼容国内常见数据格式
- 📈 **图表可视化**：支持折线图、柱状图、散点图，基于 Plotly 动态渲染
- 🧪 **示例数据加载**：无需上传也可体验功能
- 🐳 **Docker 一键部署**：无需配置环境，快速上线

---

## 🌐 在线体验

👉 [点击访问部署好的演示网站](http://bc.x9x.top:8501/)  
> 如果页面暂时无法访问，请联系作者。

---

## 🛠️ 使用方法

### ✅ 本地运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```
启动应用：

```bash
streamlit run app.py
```
访问地址：
http://localhost:8501

🐳 Docker 部署
构建镜像：

```bash
docker build -t csv-visualizer .
```
运行容器：

```bash
docker run -d -p 8501:8501 --name csv-app csv-visualizer
```
访问地址：
http://your-server-ip:8501

📌 注意事项
CSV 文件需包含至少两个字段用于图表展示

默认编码为 gbk，如需支持其他编码请修改 pd.read_csv() 参数

验证码机制基于 session_state，适用于轻量级防护
