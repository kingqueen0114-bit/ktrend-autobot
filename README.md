# K-Trend AutoBot 🇰🇷🤖

**K-Trend AutoBot** is an automated system that fetches the latest Korean trends, generates engaging SNS/Article content using Google Gemini AI, and streamlines the publishing workflow via LINE integration.

## 🌟 Features

1.  **Automated Trend Fetching**: Searches daily for top Korean trends using Google Custom Search API.
2.  **AI Content Generation**: Uses **Gemini 1.5 Flash** to analyze search results and generate:
    *   **Instagram Post**: Catchy caption with emojis and hashtags.
    *   **CMS Article**: Structured blog post with title, lead, body, and conclusion.
3.  **LINE Approval Workflow**: Sends a draft notification to your LINE. You can "Approve" with one tap.
4.  **Auto-Publishing**: Upon approval:
    *   Images are uploaded to **Google Cloud Storage (Public)**.
    *   Content is saved to **Firestore** and appended to **Google Sheets** for your CMS/Studio team.

## 🏗️ Architecture

-   **Cloud Functions (Gen 2)**:
    -   `ktrend-daily-fetch`: Triggered daily by Cloud Scheduler. Performs search & AI generation.
    -   `ktrend-line-webhook`: Receives "Approve" events from LINE and handles publishing.
-   **Google Cloud Storage**: Stores images referenced in articles.
-   **Firestore**: Database for managing draft states (`draft` -> `published`).
-   **Google Sheets**: Acts as the content database for the CMS.

## 🚀 Usage

### Automatic Mode
The system runs automatically every day at **9:00 AM JST** (configured in Cloud Scheduler).

### Manual Mode (Testing)
You can trigger the process manually via the Google Cloud Console:
1.  Go to [Cloud Scheduler](https://console.cloud.google.com/cloudscheduler).
2.  Find `ktrend-daily-trigger`.
3.  Click **Actions** > **Force Run**.

### Approval Process
1.  You will receive a **Flex Message** on LINE with the trend image and summary.
2.  Review the content.
3.  Tap **"Approve & Publish"**.
4.  **Auto-Publishing**: Upon approval:
    *   Images are uploaded to **Google Cloud Storage (Public)**.
    *   Content is saved to **Firestore** and appended to **WordPress** (via REST API).

## 🎨 Customizing Content
You can customize the AI persona, writing style, and output format by editing a single file.
See **[PROMPT_GUIDE.md](./PROMPT_GUIDE.md)** for details.


## 🛠️ Deployment

### 1. Project Setup (First Time Only)
To ensure you are deploying to the correct Google Cloud project, run the setup script. This creates a dedicated `gcloud` configuration for this project.

```bash
./setup_project.sh
```

### 2. Deploy
The project is deployed using the `deploy.sh` script, which handles API enablement and function updates.

```bash
# Deploy/Update both functions
./deploy.sh
```

### Environment Variables
The system relies on environment variables managed through `.env.yaml` (local) or Google Cloud Secret Manager (production).

Key environment variables:
-   `GEMINI_API_KEY`: For AI generation.
-   `GOOGLE_CUSTOM_SEARCH_API_KEY` / `GOOGLE_CSE_ID`: For search.
-   `LINE_CHANNEL_ACCESS_TOKEN` / `LINE_CHANNEL_SECRET`: For LINE Bot.
-   `GCP_PROJECT_ID`: `k-trend-autobot`.
-   `WORDPRESS_URL` / `WORDPRESS_USER` / `WORDPRESS_APP_PASSWORD`: For WordPress integration.

**For detailed setup and security management, see [DEVELOPMENT.md](./DEVELOPMENT.md).**

## 📁 Project Structure

-   `cloud_entry.py`: Thin router for Cloud Functions.
-   `setup_project.sh`: Project initialization script.
-   `deploy.sh`: Deployment automation script.
-   `handlers/`:
    -   `schedulers.py`: Daily fetch & report logic.
    -   `webhook.py`: LINE webhook handler.
    -   `line_actions.py`: Approval/Reject/Edit logic.
    -   `draft_editor.py`: HTML editor for drafts.
-   `src/`:
    -   `fetch_trends.py`: Search logic.
    -   `content_generator.py`: AI generation logic.
    -   `content_prompts.py`: **AI Prompts & Rules** (Edit here!).
    -   `notifier.py`: LINE message formatting.
    -   `storage_manager.py`: GCP (Firestore/Storage) handler.
-   `utils/`:
    -   `logging_config.py`: Structured logging.
    -   `helpers.py`: Common utilities.

## 📝 Troubleshooting

### 1. Google Search API Error (403 Forbidden)
If the LINE notification says **"Mock Trend"**, the Google Custom Search API is failing (likely due to IP restrictions).
**Fix:**
1.  Go to [Google Cloud Console > Credentials](https://console.cloud.google.com/apis/credentials).
2.  Find the **Search API Key**.
3.  Under "Application restrictions", switch to **None** (or add Cloud Functions IPs).
4.  Save.

### 2. Disabling Mock Mode
Once the API key is fixed:
1.  Edit `deploy.sh`.
2.  Remove `--set-env-vars USE_MOCK_ON_FAIL="true" \`.
3.  Run `./deploy.sh` to redeploy.

### 3. Other Issues
If something goes wrong (e.g., no message received):
1.  Check **Cloud Logging**:
    [View Logs](https://console.cloud.google.com/logs/viewer?project=k-trend-autobot)
2.  Filter by `severity >= ERROR` to find crashes.
