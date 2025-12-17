<div align="center">

# 🛡️ MonitorTask

**漏洞情报监控平台 - Vulnerability Intelligence Monitoring Platform**

[![GitHub stars](https://img.shields.io/github/stars/rockmelodies/MonitorTask?style=social)](https://github.com/rockmelodies/MonitorTask/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/rockmelodies/MonitorTask?style=social)](https://github.com/rockmelodies/MonitorTask/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/rockmelodies/MonitorTask?style=social)](https://github.com/rockmelodies/MonitorTask/watchers)
[![GitHub issues](https://img.shields.io/github/issues/rockmelodies/MonitorTask)](https://github.com/rockmelodies/MonitorTask/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/rockmelodies/MonitorTask)](https://github.com/rockmelodies/MonitorTask/pulls)
[![GitHub last commit](https://img.shields.io/github/last-commit/rockmelodies/MonitorTask)](https://github.com/rockmelodies/MonitorTask/commits/main)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Vue](https://img.shields.io/badge/Vue-3.4.0-brightgreen.svg)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-blue.svg)](https://www.typescriptlang.org/)
[![Element Plus](https://img.shields.io/badge/Element_Plus-2.5.0-409eff.svg)](https://element-plus.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code size](https://img.shields.io/github/languages/code-size/rockmelodies/MonitorTask)](https://github.com/rockmelodies/MonitorTask)
[![GitHub release](https://img.shields.io/github/v/release/rockmelodies/MonitorTask)](https://github.com/rockmelodies/MonitorTask/releases)

**专为漏洞情报分析师设计的自动化监控系统**

帮助安全团队第一时间发现漏洞威胁,提升安全响应效率

[功能特性](#-功能特性) •
[快速开始](#-快速开始) •
[技术栈](#-技术栈) •
[使用指南](#-使用指南) •
[预设情报源](#-预设情报源)

</div>

---

## ✨ 功能特性

<div align="center">

### 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=rockmelodies/MonitorTask&type=Date)](https://star-history.com/rockmelodies/MonitorTask&Date)

</div>

---

### 核心功能

- 🎯 **智能监控** - 自动检测网页内容变化,支持CSS选择器精准监控
- 🔔 **实时通知** - 钉钉机器人实时推送,高危漏洞@所有人
- 🔍 **关键词过滤** - 支持正则表达式,只关注重要情报
- 📊 **数据分析** - 自动提取CVE编号、CVSS评分、风险等级
- 🎨 **美观界面** - 基于Vue3 + Element Plus的现代化UI

### 安全管理

- 👤 **用户认证** - JWT Token身份验证
- 🔐 **权限管理** - 管理员/用户/访客三级权限体系
- 📝 **操作审计** - 完整的操作日志记录
- 🛡️ **数据安全** - 密码加密存储,敏感信息保护

### 高级特性

- ⚡ **高性能** - 支持并发监控100+个网页
- 🔄 **7x24运行** - 自动重试,异常报警
- 📈 **实时统计** - 仪表盘展示监控状态
- 🏷️ **任务分类** - 标签管理,优先级分级

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Node.js**: 16.0+
- **npm**: 8.0+

### 后端部署

#### 方法一: 一键启动(推荐)

**Windows用户:**
```bash
# 双击运行或命令行执行
start.bat
```

**Linux/Mac用户:**
```bash
chmod +x start.sh
./start.sh
```

脚本会自动:
- ✅ 检查Python环境
- ✅ 创建/激活虚拟环境(.venv)
- ✅ 安装依赖包
- ✅ 创建配置文件
- ✅ 启动服务

#### 方法二: 手动部署

#### 1. 克隆项目

```bash
git clone <repository-url>
cd MonitorTask
```

#### 2. 创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. 安装依赖

```bash
# 使用国内镜像加速(推荐)
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者使用官方源
pip install -r requirements.txt
```

**重要依赖说明:**
- `Flask-JWT-Extended`: JWT认证
- `Flask-Bcrypt`: 密码加密
- `APScheduler`: 任务调度
- `BeautifulSoup4`: HTML解析
- `requests`: HTTP请求

#### 4. 配置环境变量

复制 `.env.example` 到 `.env` 并修改配置:

```bash
cp .env.example .env
```

编辑 `.env` 文件,**必须修改以下配置**:

```ini
# 数据库配置
DATABASE_URL=sqlite:///monitor.db

# Flask配置
FLASK_ENV=development  # 开发环境: development, 生产环境: production
SECRET_KEY=your-secret-key-here  # ⚠️ 必须修改为随机字符串
JWT_SECRET_KEY=your-jwt-secret-key  # ⚠️ 必须修改为随机字符串

# 钉钉配置(可选)
DEFAULT_DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx

# 监控配置
DEFAULT_CHECK_INTERVAL=300  # 默认检查间隔(秒)
MAX_CONCURRENT_TASKS=100     # 最大并发任务数
REQUEST_TIMEOUT=30           # 请求超时时间(秒)
```

**⚠️ 安全提示:**

1. **SECRET_KEY 和 JWT_SECRET_KEY 必须修改!**
2. 生产环境必须使用强随机密钥
3. 不要将 `.env` 文件提交到Git仓库

**生成安全密钥的方法:**

```bash
# Python方式生成随机密钥
python -c "import secrets; print(secrets.token_hex(32))"

# 输出示例:
# a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```

将生成的密钥分别填入 `SECRET_KEY` 和 `JWT_SECRET_KEY`:

```ini
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
JWT_SECRET_KEY=f2e1d0c9b8a7z6y5x4w3v2u1t0s9r8q7p6o5n4m3l2k1j0i9h8g7f6e5d4c3b2a1
```

**环境变量说明:**

| 变量 | 说明 | 示例值 | 必填 |
|------|------|--------|------|
| `DATABASE_URL` | 数据库连接字符串 | `sqlite:///monitor.db` | 是 |
| `FLASK_ENV` | Flask运行环境 | `development` / `production` | 是 |
| `SECRET_KEY` | Flask会话密钥 | 随机字符串(64位) | **是** |
| `JWT_SECRET_KEY` | JWT加密密钥 | 随机字符串(64位) | **是** |
| `DEFAULT_DINGTALK_WEBHOOK` | 默认钉钉机器人地址 | `https://oapi.dingtalk.com/...` | 否 |
| `DEFAULT_CHECK_INTERVAL` | 默认检查间隔(秒) | `300` | 否 |
| `MAX_CONCURRENT_TASKS` | 最大并发任务数 | `100` | 否 |
| `REQUEST_TIMEOUT` | HTTP请求超时(秒) | `30` | 否 |

#### 5. 启动后端服务

```bash
python run.py
```

服务启动后访问: `http://localhost:5000`

---

### 前端部署

#### 1. 进入前端目录

```bash
cd frontend
```

#### 2. 安装依赖

```bash
npm install
```

#### 3. 开发模式运行

```bash
npm run dev
```

前端服务访问: `http://localhost:3000`

#### 4. 生产环境构建

```bash
npm run build
```

构建产物会输出到 `../static` 目录,与后端集成。

---

## 🎨 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| **Python** | 3.8+ | 编程语言 |
| **Flask** | 3.0.0 | Web框架 |
| **SQLAlchemy** | 3.1.1 | ORM框架 |
| **SQLite** | - | 数据库 |
| **APScheduler** | 3.10.4 | 任务调度 |
| **BeautifulSoup4** | 4.12.2 | HTML解析 |
| **Requests** | 2.31.0 | HTTP客户端 |
| **Flask-JWT-Extended** | 4.5.3 | JWT认证 |
| **Flask-Bcrypt** | 1.0.1 | 密码加密 |

### 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| **Vue** | 3.4.0 | 前端框架 |
| **TypeScript** | 5.3.3 | 类型系统 |
| **Element Plus** | 2.5.0 | UI组件库 |
| **Vue Router** | 4.2.5 | 路由管理 |
| **Pinia** | 2.1.7 | 状态管理 |
| **Axios** | 1.6.2 | HTTP客户端 |
| **Vite** | 5.0.8 | 构建工具 |

---

## 📖 使用指南

### 1. 登录系统

默认管理员账号:
- **用户名**: `admin`
- **密码**: `admin123`

⚠️ **首次登录后请立即修改密码!**

### 2. 添加监控任务

#### 方式一: 手动添加

1. 进入 **监控任务** 页面
2. 点击 **添加任务** 按钮
3. 填写任务信息:
   - **任务名称**: 如"CNVD最新漏洞"
   - **监控URL**: 如 `https://www.cnvd.org.cn/flaw/list`
   - **检查间隔**: 建议300秒(5分钟)
   - **CSS选择器**: 可选,精准监控特定区域
   - **关键词**: 如"高危,紧急,CVE-"
   - **钉钉Webhook**: 配置接收通知的钉钉群
   - **优先级**: 高/中/低
   - **标签**: 如"国内官方,漏洞库"

#### 方式二: 使用预设源

系统内置了10+个常用漏洞情报源,参考 `preset_sources.json`

### 3. 配置钉钉机器人

#### 步骤:

1. 打开钉钉群 → **群设置** → **智能群助手** → **添加机器人** → **自定义**
2. 设置机器人名称: "MonitorTask"
3. 安全设置选择 **自定义关键词**: "漏洞预警" 或 "监控提醒"
4. 复制 **Webhook地址**
5. 在MonitorTask添加/编辑任务时粘贴Webhook地址

#### 消息示例:

```markdown
## 🚨 漏洞情报预警

**来源**: CNVD国家漏洞库
**时间**: 2024-01-15 14:30:25
**优先级**: 🔴 HIGH

**CVE编号**: CVE-2024-12345
**风险等级**: 高危
**匹配关键词**: 高危, 远程代码执行

**变化摘要**:
新增Apache Struts2远程代码执行漏洞...

**查看详情**: https://www.cnvd.org.cn/...

@所有人 请相关团队立即响应!
```

### 4. 用户管理(管理员)

管理员可以:
- ✅ 查看所有用户
- ✅ 编辑用户角色和权限
- ✅ 启用/禁用用户账户
- ✅ 重置用户密码
- ✅ 删除用户(admin账户除外)

### 5. 权限说明

| 角色 | 权限 |
|------|------|
| **admin** | 全部权限,包括用户管理 |
| **user** | 创建/编辑/删除监控任务,查看变化记录 |
| **viewer** | 仅查看权限,不能修改 |

---

## 📚 预设情报源

系统内置以下常用漏洞情报源:

### 国内官方

- ✅ **CNVD** - 国家信息安全漏洞共享平台
- ✅ **CNNVD** - 国家信息安全漏洞库
- ✅ **奇安信威胁情报中心**
- ✅ **绿盟科技安全预警**
- ✅ **深信服安全通告**

### 国际权威

- ✅ **NVD** - 美国国家漏洞数据库
- ✅ **Exploit-DB** - 漏洞利用库
- ✅ **GitHub Security Advisories**

### 厂商公告

- ✅ **Microsoft安全更新**
- ✅ **阿里云安全公告**

*详细配置请参考 `preset_sources.json`*

---

## 📊 项目结构

```
MonitorTask/
├── backend/                    # 后端代码
│   ├── app.py                 # Flask应用入口
│   ├── config.py              # 配置文件
│   ├── models.py              # 数据库模型
│   ├── monitor_engine.py      # 监控引擎
│   ├── notifier.py            # 通知模块
│   ├── scheduler.py           # 任务调度器
│   └── run.py                 # 启动脚本
│
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── api/              # API接口
│   │   ├── layouts/          # 布局组件
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia状态管理
│   │   ├── utils/            # 工具函数
│   │   ├── views/            # 页面组件
│   │   ├── App.vue           # 根组件
│   │   └── main.ts           # 入口文件
│   ├── package.json
│   └── vite.config.ts
│
├── preset_sources.json        # 预设情报源
├── requirements.txt           # Python依赖
├── .env.example              # 环境变量示例
├── .gitignore                # Git忽略文件
└── README.md                 # 项目文档
```

---

## 🔧 API文档

### 认证相关

```
POST   /api/auth/register     # 用户注册
POST   /api/auth/login        # 用户登录
GET    /api/auth/me           # 获取当前用户信息
```

### 任务管理

```
GET    /api/tasks             # 获取所有任务
POST   /api/tasks             # 创建任务
GET    /api/tasks/{id}        # 获取单个任务
PUT    /api/tasks/{id}        # 更新任务
DELETE /api/tasks/{id}        # 删除任务
GET    /api/tasks/{id}/changes # 获取任务变化记录
```

### 数据统计

```
GET    /api/stats             # 获取统计信息
GET    /api/changes           # 获取所有变化记录
```

### 用户管理(管理员)

```
GET    /api/users             # 获取所有用户
PUT    /api/users/{id}        # 更新用户
DELETE /api/users/{id}        # 删除用户
```

---

## ⚙️ 高级配置

### 修改检查频率

在 `.env` 文件中:

```ini
DEFAULT_CHECK_INTERVAL=300    # 默认5分钟
```

### 调整并发任务数

```ini
MAX_CONCURRENT_TASKS=100      # 最大并发数
```

### 请求超时设置

```ini
REQUEST_TIMEOUT=30            # 30秒超时
```

---

## 🛠️ 故障排查

### 问题1: 启动失败

**原因**: 端口被占用

**解决**:
```bash
# 检查端口占用
netstat -ano | findstr :5000

# 修改端口(在app.py)
app.run(host='0.0.0.0', port=5001)
```

### 问题2: 无法接收钉钉通知

**检查清单**:
- ✅ Webhook地址正确
- ✅ 钉钉机器人关键词设置正确
- ✅ 任务中配置了Webhook
- ✅ 网络可以访问钉钉API

### 问题3: 监控不生效

**检查**:
```bash
# 查看日志
tail -f logs/monitor.log

# 检查任务是否激活
# 在数据库中查看 is_active 字段
```

---

## 📝 开发计划

### V1.0 ✅ (已完成)
- ✅ 基础监控功能
- ✅ 钉钉通知
- ✅ 用户认证
- ✅ 权限管理

### V1.1 (计划中)
- ⬜ 邮件通知
- ⬜ 微信通知
- ⬜ 自动截图
- ⬜ 数据导出

### V1.2 (未来)
- ⬜ 多租户支持
- ⬜ 可视化大屏
- ⬜ AI智能分析
- ⬜ Docker部署

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request!

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 作者

**MonitorTask Team**

- 📧 Email: rockysocket@gmail.com
- 🌐 Website: https://blog.csdn.net/sinat_17584329?type=blog

---

## 🙏 致谢

- Element Plus - 优秀的Vue3 UI组件库
- Flask - 轻量级Python Web框架
- 所有为漏洞披露做出贡献的安全研究员

---

<div align="center">

**如果这个项目对你有帮助,请给一个 ⭐ Star!**

Made with ❤️ by MonitorTask Team

</div>
