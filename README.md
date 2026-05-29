

# Python Data Analyst Job Checker

自动扫描远程友好公司的招聘页面，筛选出含有 Python / Data Analyst 相关岗位的公司，并通过 GitHub Pages 发布可交互的岗位列表。

---

## ✨ 功能特性

- 从 `companies.xlsx` 读取公司名单，自动筛选 **worldwide / global** 远程公司
- 多线程爬取各公司 `/careers`、`/jobs` 等常见招聘路径
- 关键词匹配（`python`、`data analyst`、`data analysis`、`data scientist`）
- 本地 JSON 缓存，避免重复请求
- 自动生成带可点击岗位链接的 HTML 页面，部署至 **GitHub Pages**
- 支持定时任务（每天北京时间 08:00 自动运行）

---

## 📁 项目结构

```
.
├── check_jobs.py                              # 主脚本：爬取 + 匹配 + 输出
├── companies.xlsx                             # 公司名单（需自行提供）
├── requirements.txt                           # Python 依赖
├── cache.json                                 # 爬取缓存（自动生成）
├── remote_companies_with_python_jobs_cached.xlsx  # 完整结果（自动生成）
├── python_data_jobs.csv                       # 仅含匹配岗位的结果（自动生成）
└── .github/
    └── workflows/
        └── check_jobs.yml                     # GitHub Actions 工作流
```

---

## 🚀 快速开始

### 1. 准备公司名单

在项目根目录放置 `companies.xlsx`，至少包含以下列：

| 列名 | 说明 |
|------|------|
| `name` | 公司名称 |
| `website` | 公司官网（含 `http://` 或 `https://`） |
| `region` | 地区，含 `worldwide` 或 `global` 的行会被处理 |

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 本地运行

```bash
python check_jobs.py
```

运行完成后会生成：
- `remote_companies_with_python_jobs_cached.xlsx` — 全量结果
- `python_data_jobs.csv` — 仅匹配到岗位的公司
- `cache.json` — 请求缓存

---

## ⚙️ GitHub Actions 自动化

工作流文件 `.github/workflows/check_jobs.yml` 支持三种触发方式：

| 触发方式 | 说明 |
|----------|------|
| `push` / PR | 提交或更新 Pull Request 时自动运行 |
| `workflow_dispatch` | 在 Actions 页面手动触发 |
| `schedule` | 每天 UTC 00:00（北京 08:00）定时运行 |

运行完成后，结果会自动部署到仓库的 **GitHub Pages**（`gh-pages` 分支），可直接访问：

```
https://<your-username>.github.io/<your-repo>/
```

页面包含可搜索、可翻页的岗位表格，以及 Excel 文件的下载链接。

---

## 🔧 配置说明

在 `check_jobs.py` 开头可调整以下参数：

```python
KEYWORDS = ["python", "data analyst", "data analysis", "data scientist"]
CAREER_PATHS = ["/careers", "/jobs", "/join-us", "/join", "/recruitment"]
MAX_WORKERS = 10      # 并发线程数
BATCH_DELAY = 1       # 每个任务完成后的延迟（秒），降低被封风险
```

---

## 📦 依赖

```
requests
pandas
beautifulsoup4
openpyxl
```

---

## ⚠️ 注意事项

- 爬取行为请遵守目标网站的 `robots.txt` 及使用条款
- 部分网站有反爬机制，可能导致抓取失败，结果仅供参考
- 首次运行速度较慢，后续通过缓存加速
- GitHub Actions 需要仓库开启 **Pages** 功能，并将 Source 设为 `gh-pages` 分支

---

## 📄 License

MIT
