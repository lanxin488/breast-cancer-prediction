# 乳腺癌预测系统 - 外网部署指南

## 🚀 推荐方案：Render（免费、简单）

### 优点
- ✅ 免费额度（750小时/月）
- ✅ 支持 Flask
- ✅ 自动 HTTPS
- ✅ 部署简单

### 部署步骤

#### 1. 准备代码
确保项目包含以下文件：
```
├── app.py                  # 主应用
├── requirements.txt        # 依赖
├── render.yaml            # Render 配置
├── Procfile               # Procfile
├── templates/             # HTML 模板
├── models.py              # 模型
├── lr_model.pkl           # 模型文件
├── rf_model.pkl
├── scaler.pkl
└── knowledge_base.py       # 知识库
```

#### 2. 推送到 GitHub
```bash
# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "乳腺癌预测系统"

# 在 GitHub 创建仓库，然后推送
git remote add origin https://github.com/你的用户名/breast-cancer-prediction.git
git push -u origin main
```

#### 3. 在 Render 部署

1. **访问 Render**
   打开浏览器访问：https://render.com

2. **登录/注册**
   - 点击 "Sign Up" 注册账号
   - 推荐使用 GitHub 账号登录

3. **创建 Web Service**
   - 点击 "New +" 按钮
   - 选择 "Web Service"
   - 连接你的 GitHub 仓库

4. **配置服务**
   - **Name**: `breast-cancer-prediction`
   - **Region**: Singapore（离中国近）
   - **Branch**: main
   - **Root Directory**: （留空）
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. **选择免费套餐**
   - 点击 "Free" 套餐

6. **部署**
   - 点击 "Create Web Service"
   - 等待构建和部署（3-5分钟）

7. **完成！**
   - 部署成功后，你会获得一个 URL：`https://breast-cancer-prediction.onrender.com`
   - 这个链接可以直接分享给任何人访问！

---

## 🔄 替代方案：Railway

### 优点
- ✅ 每月 $5 免费额度
- ✅ 部署简单
- ✅ 支持自定义域名

### 部署步骤

1. **访问 Railway**
   打开：https://railway.app

2. **登录**
   使用 GitHub 账号登录

3. **创建项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库

4. **配置**
   Railway 会自动检测 Python 项目
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

5. **部署完成**
   - 获得公共 URL
   - 可以自定义域名

---

## 🌐 临时方案：ngrok（内网穿透）

如果只是临时演示，不想部署到云服务器：

### 1. 下载 ngrok
访问：https://ngrok.com/download

### 2. 启动 Flask 应用
```bash
python app.py
```
（应用运行在 http://127.0.0.1:5000）

### 3. 启动 ngrok
```bash
ngrok http 5000
```

### 4. 获取外网链接
ngrok 会显示：
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
```

### 5. 使用
把 `https://abc123.ngrok.io` 发给任何人，他们就能访问你的应用了！

⚠️ 注意：ngrok 免费版每次重启都会换链接

---

## 📋 部署检查清单

### 代码准备
- [x] `requirements.txt` 已更新
- [x] `app.py` 存在
- [x] 所有模板文件存在
- [x] 模型文件存在（.pkl）

### GitHub 准备
- [ ] 创建 GitHub 仓库
- [ ] 推送代码
- [ ] 确认仓库公开或可访问

### Render 部署
- [ ] 注册 Render 账号
- [ ] 连接 GitHub
- [ ] 配置构建命令
- [ ] 启动服务
- [ ] 测试访问

### 后续
- [ ] 记录外网访问地址
- [ ] 测试所有功能
- [ ] （可选）配置自定义域名

---

## 🔧 常见问题

### Q1: 部署失败怎么办？
查看 Render 的构建日志，通常是依赖安装问题。常见错误：
- `requirements.txt` 格式错误
- 缺少 `.pkl` 模型文件
- 路径问题

### Q2: 数据库问题？
Render 免费版不支持持久化数据库。系统已配置使用 SQLite 临时数据库，每次重启会清空数据。如需持久化，可以：
- 使用 Railway 的 PostgreSQL
- 使用 Render 的持久化磁盘

### Q3: 如何更新代码？
推送新代码到 GitHub，Render 会自动重新部署。

### Q4: 免费额度够用吗？
- Render 免费版：750小时/月（约一个月不停机）
- Railway $5额度：足够小规模演示

---

## 📞 获取帮助

如果部署遇到问题，请提供：
1. 错误日志截图
2. 你使用的平台（Render/Railway）
3. 具体的错误信息

---

## 🌟 推荐工作流

1. **开发**：本地运行测试
2. **推送**：代码推送到 GitHub
3. **部署**：Render 自动部署
4. **分享**：获得外网链接

这样每次更新代码，只需 `git push`，Render 就会自动重新部署！
