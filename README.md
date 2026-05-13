# 乳腺癌预测系统 - 软件工程课程作业

## 📖 项目简介

本项目是一个基于机器学习的乳腺癌预测系统，使用Python Flask框架开发，整合了多种机器学习算法（随机森林、逻辑回归）来实现乳腺癌的智能预测。

### 主要功能
- 🔐 用户注册与登录系统
- 🎯 基于30个特征的乳腺癌预测
- 📊 预测结果可视化展示
- 📋 历史预测记录管理
- 🤖 AI健康助手（基于知识库）
- 📈 模型性能评估
- 🎨 美观的蓝色医疗主题界面

---

## 🚀 快速开始

### 1. 环境要求
- Python 3.8 或更高版本
- pip 包管理器

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行项目
```bash
python app.py
```

### 4. 访问系统
打开浏览器访问：http://127.0.0.1:5000

---

## 📂 项目结构

```
乳腺癌预测系统_软件工程作业/
├── app.py                          # Flask应用主文件
├── models.py                       # 数据库模型和机器学习模型
├── knowledge_base.py               # AI健康助手知识库
├── requirements.txt                # Python依赖包列表
├── README.md                       # 项目说明文档（本文件）
├── run.bat                         # Windows快速启动脚本
├── static/
│   ├── css/
│   │   └── style.css               # 样式文件
│   └── js/
│       └── main.js                 # JavaScript交互文件
├── templates/
│   ├── base.html                   # 基础模板
│   ├── index.html                  # 首页
│   ├── login.html                  # 登录页
│   ├── register.html               # 注册页
│   ├── predict.html                # 预测页
│   ├── prediction_report.html      # 预测报告
│   ├── history.html                # 历史记录
│   ├── profile.html                # 个人中心
│   ├── risk_interpretation.html    # 风险解读
│   ├── model_performance.html      # 模型性能
│   ├── model_comparison.html       # 模型对比
│   ├── data_visualization.html     # 数据可视化
│   ├── health_profile.html         # 健康档案
│   ├── lifestyle_intervention.html # 生活方式干预
│   ├── doctor_consultation.html    # 医生咨询
│   ├── community.html              # 病友交流
│   ├── privacy_security.html       # 隐私安全
│   ├── faq.html                    # 使用指南
│   ├── about.html                  # 关于项目
│   ├── ai_chat.html                # AI助手
│   ├── admin_db.html               # 管理员后台
│   └── errors/
│       ├── 404.html                # 404错误页
│       └── 500.html                # 500错误页
├── instance/                       # 数据库目录（自动创建）
│   └── breast_cancer.db            # SQLite数据库文件
└── docs/                           # 文档目录
```

---

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| **后端框架** | Flask |
| **数据库** | SQLite + SQLAlchemy |
| **用户认证** | Flask-Login |
| **机器学习** | scikit-learn |
| **模型算法** | 随机森林、逻辑回归 |
| **前端** | HTML5 + CSS3 + JavaScript |
| **数据集** | scikit-learn内置乳腺癌数据集 |

---

## 📊 机器学习模型

### 数据集
- 来源：scikit-learn内置乳腺癌数据集
- 样本数：569例
- 特征数：30个（Mean、SE、Worst各10个）
- 类别：良性/恶性

### 特征说明
1. **Mean组（10个特征）**：平均值
2. **SE组（10个特征）**：标准误差
3. **Worst组（10个特征）**：最大值/最差值

### 模型性能
- **随机森林**：准确率约97%+
- **逻辑回归**：准确率约96%+

---

## 📝 使用说明

### 1. 首次运行
- 系统会自动创建数据库和训练模型
- 首次运行需要等待几秒（模型训练时间）

### 2. 用户注册
- 访问注册页面创建账号
- 填写用户名、邮箱、密码
- 注册后自动登录

### 3. 预测流程
1. 登录系统
2. 进入预测页面
3. 填写30个特征数据（或点击"随机填入"）
4. 选择预测模型
5. 点击"开始预测"
6. 查看预测结果和特征重要性

### 4. AI助手
- 支持27+个常见问题的自动回答
- 涵盖：症状、预防、检查、治疗、饮食等
- 使用内置知识库，无需联网

---

## 🔧 管理员功能

- 注册用户名为 **"admin"** 获得管理员权限
- 访问 `/admin-db` 查看后台
- 可以查看所有用户和预测记录
- 查看统计数据

---

## ⚠️ 重要声明

**本系统仅供学习研究使用，不替代专业医生的诊断！**

- 所有预测结果仅供参考
- 如有身体不适，请及时就医
- 模型准确率虽高，但仍存在误判可能

---

## 📚 参考资料

- scikit-learn官方文档
- Flask官方文档
- UCI机器学习仓库

---

## 👥 作者信息

- 课程：软件工程
- 完成时间：2024年

---

## 📄 许可证

本项目仅用于教学研究目的。
