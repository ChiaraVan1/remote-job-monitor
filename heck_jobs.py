import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
import json

# ---------------- 配置 ----------------
KEYWORDS = ["python", "data analyst", "data analysis", "data scientist"]
CAREER_PATHS = ["/careers", "/jobs", "/join-us", "/join", "/recruitment"]
CACHE_FILE = "cache.json"
MAX_WORKERS = 10
BATCH_DELAY = 1

# ---------------- 1. 拉取公司名单 ----------------
url = "https://raw.githubusercontent.com/remoteintech/remote-jobs/main/data/companies.json"
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data)
df.columns = df.columns.str.lower()

# 筛选 region = worldwide
df = df[df["Region"] == "worldwide"].reset_index(drop=True)
print(f"✅ 筛选出 {len(df)} 家 面向 worldwide 招聘公司")

# ---------------- 2. 加载缓存 ----------------
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}

# ---------------- 3. 检查 Careers 页面 ----------------
def check_careers(website):
    if not website or not website.startswith("http"):
        return None
    website = website.rstrip("/")
    for path in CAREER_PATHS:
        url = website + path
        try:
            r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                text = r.text.lower()
                if any(word in text for word in ["job", "career", "openings", "hiring"]):
                    return url
        except:
            pass
    return None

# ---------------- 4. 抓取匹配岗位 ----------------
def find_python_jobs(career_url):
    matched_jobs = []
    if not career_url:
        return matched_jobs
    try:
        r = requests.get(career_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return matched_jobs
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all("a", href=True):
            text = link.get_text(strip=True).lower()
            href = link["href"]
            if any(kw in text for kw in KEYWORDS):
                if not href.startswith("http"):
                    href = career_url.rstrip("/") + "/" + href.lstrip("/")
                matched_jobs.append(f"{text} ({href})")
        return matched_jobs
    except:
        return matched_jobs

# ---------------- 5. 处理单个公司 ----------------
def process_company(row):
    name = row.get("name")
    website = row.get("website")
    if name in cache:
        return cache[name]
    career_page = check_careers(website)
    matched_jobs = find_python_jobs(career_page) if career_page else []
    result = {
        "career_page": career_page,
        "is_hiring": career_page is not None,
        "matched_jobs": matched_jobs,
        "has_python_data_analyst_job": len(matched_jobs) > 0
    }
    cache[name] = result
    return result

# ---------------- 6. 多线程处理 ----------------
results = []
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(process_company, row): idx for idx, row in df.iterrows()}
    for future in as_completed(futures):
        idx = futures[future]
        try:
            result = future.result()
        except Exception as e:
            result = {
                "career_page": None,
                "is_hiring": False,
                "matched_jobs": [],
                "has_python_data_analyst_job": False
            }
        results.append((idx, result))
        time.sleep(BATCH_DELAY)

results.sort(key=lambda x: x[0])
df["career_page"] = [r["career_page"] for idx, r in results]
df["is_hiring"] = [r["is_hiring"] for idx, r in results]
df["matched_jobs"] = [r["matched_jobs"] for idx, r in results]
df["has_python_data_analyst_job"] = [r["has_python_data_analyst_job"] for idx, r in results]

# ---------------- 7. 保存结果 ----------------
output_file = "remote_companies_with_python_jobs_cached.xlsx"
df.to_excel(output_file, index=False)

with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(cache, f, indent=2, ensure_ascii=False)

print(f"✅ 检查完成，结果保存为 {output_file}")
