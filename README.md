# OpportunityRadar 🚀

OpportunityRadar is a comprehensive Startup Opportunity Aggregator that scans the web for grants, accelerators, conferences, and competitions. It uses AI to automatically tag opportunities with funding ranges, startup stages, and remote/on-site status.

## 🌟 Features
- **Real-time Aggregation**: Scrapes F6S, Devpost, Grants.gov, and AlphaGamma.
- **AI-Powered Tagging**: Uses Anthropic Claude (Haiku) to analyze descriptions and extract key data.
- **Modern Dashboard**: A dark-themed, data-dense UI built with vanilla JS and CSS.
- **Advanced Filtering**: Search by keyword, type, source, and date.
- **Data Export**: Export all opportunities to CSV or JSON with a single click.
- **Automated Scheduler**: Background tasks run every 6 hours to fetch new data.

## 🛠 Tech Stack
- **Backend**: Python (FastAPI)
- **Database**: SQLite with SQLAlchemy ORM
- **Scraping**: httpx, BeautifulSoup4, feedparser
- **Scheduler**: APScheduler
- **AI**: Anthropic Claude API (claude-3-5-haiku)
- **Frontend**: Vanilla HTML/JS/CSS

## 🚀 Setup & Deployment

### Local Setup
1. **Clone the repository** (or navigate to the project directory).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your API Key**:
   ```bash
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```
4. **Seed the database** (Optional but recommended for first run):
   ```bash
   python seed.py
   ```
5. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```
6. **Access the dashboard**:
   Open `http://localhost:8000` in your browser.

### Cloud Deployment (Render - Recommended)
The easiest way to deploy this app is on **Render** because it supports persistent storage for the SQLite database.

1. **Push your code** to GitHub or GitLab.
2. **Create a new Blueprint Instance** on Render.
3. Select your repository.
4. Render will automatically use the `render.yaml` file to:
   - Create a Web Service.
   - Attach a 1GB Persistent Disk (to keep your database safe between restarts).
   - Set the `DATABASE_URL` to point to the disk.
5. **Add your Environment Variable**:
   - In the Render Dashboard, go to your service -> Environment.
   - Add `ANTHROPIC_API_KEY`.
6. **Seed the Production DB** (First time only):
   - Go to the **Shell** tab in Render and run: `python seed.py`.

### Docker Deployment
1. Build the image: `docker build -t opportunity-radar .`
2. Run the container: `docker run -p 8000:8000 -e ANTHROPIC_API_KEY="your_key" opportunity-radar`

## 📡 Sources Used
- **F6S**: Primarily for accelerators and startup programs.
- **Devpost**: For hackathons and engineering competitions.
- **Grants.gov**: For US Federal government grants.
- **AlphaGamma**: For global startup opportunities and news.

## 🕵️‍♂️ Scraping Challenges
- **Rate Limiting**: Addressed using random delays (1–3s) and rotating User-Agent strings.
- **JS-Rendering**: Some sites (like F6S) use dynamic content. The scraper includes error handling to skip failed pages without crashing.
- **Deduplication**: Managed at the database level using a `UNIQUE` constraint on `source_link`.
- **Anti-Bot**: Realistic headers and Referers are used to mimic real browser behavior.

## 🤖 AI Tagging
New opportunities are automatically processed by Claude Haiku. The AI extracts:
- **Funding Range**: Estimated dollar amount or "Equity-free".
- **Startup Stage**: Classified as Early, Growth, or Any.
- **Work Mode**: Remote, On-site, or Hybrid.

## 📊 Exporting Data
- **CSV**: Access `/api/export/csv` to download the entire database as a CSV.
- **JSON**: Access `/api/export/json` for a JSON dump.
- **Dashboard**: Use the "Export" buttons at the bottom of the UI.

## 📅 Maintenance
The app runs a background scheduler that:
1. Performs a full scrape immediately on startup.
2. Repeats the scrape every 6 hours.
3. Automatically triggers AI tagging for any newly discovered opportunities.
