# 乳腺癌预测系统 - PythonAnywhere 部署指南

## 🚀 免费部署，无需信用卡

### 步骤 1：注册 PythonAnywhere

1. 访问：https://www.pythonanywhere.com
2. 点击 "Pricing" → 选择 "Beginner"（完全免费）
3. 填写注册信息：
   - 用户名：lanxin488（建议和 GitHub 一致）
   - 邮箱：您的邮箱
   - 密码：设置密码

### 步骤 2：上传代码

**方法 A：使用 GitHub 导入（推荐）**

1. 登录后，点击右上角 "Files" → "Open Bash console here"
2. 在 Bash 中执行：
```bash
git clone https://github.com/lanxin488/breast-cancer-prediction.git
cd breast-cancer-prediction
```

**方法 B：手动上传**

1. 点击 "Files"
2. 点击 "Upload a file" 逐个上传文件
3. 或者使用 PythonAnywhere 的文件管理器

### 步骤 3：安装依赖

在 Bash 中执行：
```bash
cd breast-cancer-prediction
pip install -r requirements.txt --user
```

### 步骤 4：创建 Web 应用

1. 点击 "Web" → "Add a new web app"
2. 选择 Python 版本：**Python 3.10**
3. 选择 "Manual configuration"（手动配置）
4. 点击 "Next" 完成创建

### 步骤 5：配置 WSGI 文件

1. 在 Web 页面找到 "WSGI configuration file"，点击路径打开编辑器
2. 将文件内容替换为：
```python
import sys
import os

path = '/home/lanxin488/breast-cancer-prediction'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```
3. 保存文件（Ctrl+S 或点击 Save）

### 步骤 6：设置虚拟环境（可选，但推荐）

在 Bash 中：
```bash
cd ~
virtualenv --python=python3.10 myenv
source myenv/bin/activate
cd breast-cancer-prediction
pip install -r requirements.txt
```

然后在 Web 页面：
- "Virtualenv" → "Enter path to virtualenv"
- 输入：`/home/lanxin488/myenv`

### 步骤 7：设置环境变量

在 Web 页面找到 "Environment Variables"：
```
SECRET_KEY=your-random-secret-key
FLASK_ENV=production
```

### 步骤 8：重新加载应用

点击 Web 页面的 **"Reload"** 按钮（带有您用户名的那个）

### 步骤 9：访问网站

部署成功后，您的网站地址是：
```
https://lanxin488.pythonanywhere.com
```

---

## ⚠️ 重要注意事项

### 1. 数据库问题
PythonAnywhere 免费版不支持持久化 SQLite（应用重启后数据会清空）。

**解决方案**：
- 使用 PythonAnywhere 的 MySQL 数据库（免费版有配额）
- 或者每次演示前重新注册账号

### 2. 测试账号
首次使用需要注册账号，或在 Bash 中运行：
```bash
cd breast-cancer-prediction
python create_db.py
python register_admin.py
```

### 3. 模型文件
确保以下文件已上传：
- `lr_model.pkl`
- `rf_model.pkl`
- `scaler.pkl`

---

## 📋 检查清单

- [ ] 注册 PythonAnywhere 账号
- [ ] 克隆或上传代码
- [ ] 安装依赖
- [ ] 创建 Web 应用（Python 3.10）
- [ ] 配置 WSGI 文件
- [ ] 安装依赖包
- [ ] 点击 Reload
- [ ] 访问网站测试

---

## ❓ 常见问题

### Q1: 访问时报 500 错误？
- 检查 WSGI 配置路径是否正确
- 检查依赖是否安装
- 查看 "Error log" 获取详细错误信息

### Q2: 模型加载失败？
- 确保 `.pkl` 文件已上传
- 检查文件路径是否正确

### Q3: 数据库错误？
- 首次使用需要初始化数据库
- 在 Bash 中运行：
```bash
cd breast-cancer-prediction
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Q4: 页面乱码？
- 已在 `app.py` 中设置 `app.config['JSON_AS_ASCII'] = False`
- 确保浏览器编码为 UTF-8

---

## 🚀 快速测试

部署成功后，访问：
```
https://lanxin488.pythonanywhere.com
```

**测试步骤**：
1. 点击注册创建账号
2. 登录后测试预测功能
3. 测试 AI 聊天功能
4. 测试医生咨询和社区页面

---

## 📞 获取帮助

如果遇到问题：
1. 查看 PythonAnywhere 的 "Error log"
2. 查看 "Server log"
3. 检查依赖是否都安装成功

祝您部署成功！🎉
