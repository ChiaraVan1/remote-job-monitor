# Remote Job Monitor

This repository contains a lightweight script for scanning company career pages and flagging remote-friendly Python or data-focused positions.

## Getting Started

After pulling the latest changes (including the PR you just merged), follow these steps locally:

1. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare the company list:**
   Ensure `companies.xlsx` is present and includes a `Region` column. Rows containing `Worldwide` or `Global` (case-insensitive, even when combined with other regions such as `USA, Worldwide`) will be processed. The script normalizes column names to lower case, so `Region`, `region`, or `REGION` are all accepted.

## Running the Monitor

Execute the script to crawl the configured company list:

```bash
python check_jobs.py
```

The script will:

- Filter the company list to those marked as worldwide remote-friendly.
- Visit common career page paths to locate a hiring page.
- Parse the page for Python/data-related job postings.
- Cache results in `cache.json` to avoid repeated crawling.
- Save the aggregated output to `remote_companies_with_python_jobs_cached.xlsx`.

## Reviewing Results

Open `remote_companies_with_python_jobs_cached.xlsx` to review findings. If you want to force a fresh crawl, delete `cache.json` before rerunning the script.

## Troubleshooting

- If you encounter network-related errors, rerun the script later or adjust the timeouts inside `check_jobs.py`.
- To inspect verbose logs, temporarily add `print` statements inside `check_jobs.py` where needed.

