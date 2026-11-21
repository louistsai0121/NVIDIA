# NVIDIA Daily Digest

每天搜尋 NVIDIA 內部組織變化、以及對 AI 商業影響的新聞，整理成 email 寄出。

透過 GitHub Actions 排程執行（`.github/workflows/daily.yml`），每天 08:00 台北時間（00:00 UTC）跑一次，也可以在 Actions 頁面手動 `Run workflow`。

## 需要設定的 Repo Secrets

到 repo 的 Settings → Secrets and variables → Actions 新增：

- `FIRECRAWL_API_KEY`
- `GMAIL_ADDRESS`（寄件/收件信箱）
- `GMAIL_APP_PASSWORD`（Gmail App Password，非帳號主密碼，可在 https://myaccount.google.com/apppasswords 管理）
