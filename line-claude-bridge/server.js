/**
 * LINE → Claude Code Bridge Server (統合版 v4)
 *
 * 機能:
 * 1. Webチャット UI (リッチメニューから開く)
 * 2. テキストメッセージ → Claude Code 自動実行
 * 3. 記事作成リクエスト → 記事生成 → 承認ボタン送信
 * 4. 未公開記事一覧 & 編集機能
 * 5. 画像アップロード対応
 */

const http = require("http");
const https = require("https");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 8080;
const LINE_CHANNEL_SECRET = process.env.LINE_CHANNEL_SECRET;
const LINE_CHANNEL_ACCESS_TOKEN = process.env.LINE_CHANNEL_ACCESS_TOKEN;
const LINE_ADMIN_USER_ID = process.env.LINE_USER_ID || process.env.LINE_ADMIN_USER_ID;
const CLAUDE_OAUTH_TOKEN = process.env.CLAUDE_CODE_OAUTH_TOKEN;
const WORKSPACE = process.env.WORKSPACE || "/home/workspace/ktrend-autobot";
const DRAFTS_DIR = process.env.DRAFTS_DIR || "/home/workspace/drafts";
const UPLOADS_DIR = process.env.UPLOADS_DIR || "/home/workspace/uploads";
const PUBLIC_DIR = path.join(__dirname, "public");
const BASE_URL = process.env.BASE_URL || "http://localhost:8080";

// WordPress設定
const WORDPRESS_URL = process.env.WORDPRESS_URL;
const WORDPRESS_USER = process.env.WORDPRESS_USER;
const WORDPRESS_APP_PASSWORD = process.env.WORDPRESS_APP_PASSWORD;

// Analytics & AdSense設定
const ANALYTICS_CONFIG_PATH = process.env.ANALYTICS_CONFIG_PATH || "/home/workspace/analytics-config.json";
const GA_PROPERTY_ID = process.env.GA4_PROPERTY_ID;

// ディレクトリ作成
[DRAFTS_DIR, UPLOADS_DIR, PUBLIC_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// Analytics設定を読み込み
function loadAnalyticsConfig() {
    if (fs.existsSync(ANALYTICS_CONFIG_PATH)) {
        return JSON.parse(fs.readFileSync(ANALYTICS_CONFIG_PATH, "utf8"));
    }
    return {
        measurementId: null,  // G-XXXXXXXXXX
        adsensePublisherId: "ca-pub-6657168802277658",  // K-TREND AdSense
        dailyReportTime: "09:00",  // 毎日9時に送信
        lastReportDate: null
    };
}

// Analytics設定を保存
function saveAnalyticsConfig(config) {
    fs.writeFileSync(ANALYTICS_CONFIG_PATH, JSON.stringify(config, null, 2));
}

function verifySignature(body, signature) {
    const hash = crypto.createHmac("sha256", LINE_CHANNEL_SECRET).update(body).digest("base64");
    return hash === signature;
}

function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
}

// LINE テキストメッセージ送信
function sendLineMessage(userId, message) {
    const text = message.length > 5000 ? message.substring(0, 4997) + "..." : message;
    const data = JSON.stringify({
        to: userId,
        messages: [{ type: "text", text: text }]
    });
    console.log("[LINE] Sending to:", userId, "Message:", text.substring(0, 50) + "...");
    const req = https.request({
        hostname: "api.line.me", path: "/v2/bot/message/push", method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN, "Content-Length": Buffer.byteLength(data) }
    }, (res) => {
        let body = "";
        res.on("data", chunk => { body += chunk; });
        res.on("end", () => {
            if (res.statusCode === 200) console.log("[LINE] Message sent successfully");
            else console.error("[LINE] Error:", res.statusCode, body);
        });
    });
    req.on("error", (err) => console.error("[LINE] Request error:", err.message));
    req.write(data);
    req.end();
}

// LINE Flex メッセージ送信（記事承認用 - 修正ボタン付き）
function sendArticleApprovalMessage(userId, draftId, title, summary) {
    const data = JSON.stringify({
        to: userId,
        messages: [{
            type: "flex",
            altText: "新規記事: " + title,
            contents: {
                type: "bubble",
                header: {
                    type: "box", layout: "vertical",
                    contents: [{ type: "text", text: "📝 新規記事", weight: "bold", size: "lg", color: "#1DB446" }]
                },
                body: {
                    type: "box", layout: "vertical",
                    contents: [
                        { type: "text", text: title, weight: "bold", size: "md", wrap: true },
                        { type: "separator", margin: "md" },
                        { type: "text", text: summary.substring(0, 150) + "...", size: "sm", color: "#666666", margin: "md", wrap: true }
                    ]
                },
                footer: {
                    type: "box", layout: "vertical", spacing: "sm",
                    contents: [
                        {
                            type: "box", layout: "horizontal", spacing: "sm",
                            contents: [
                                { type: "button", style: "primary", color: "#1DB446", action: { type: "postback", label: "✅ 承認", data: "action=approve_article&draft_id=" + draftId } },
                                { type: "button", style: "secondary", action: { type: "postback", label: "❌ 却下", data: "action=reject_article&draft_id=" + draftId } }
                            ]
                        },
                        {
                            type: "box", layout: "horizontal", spacing: "sm",
                            contents: [
                                { type: "button", style: "link", action: { type: "uri", label: "✏️ 修正", uri: BASE_URL + "/edit/" + draftId } },
                                { type: "button", style: "link", action: { type: "uri", label: "👁 確認", uri: BASE_URL + "/draft/" + draftId } }
                            ]
                        }
                    ]
                }
            }
        }]
    });

    const req = https.request({
        hostname: "api.line.me", path: "/v2/bot/message/push", method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN, "Content-Length": Buffer.byteLength(data) }
    });
    req.write(data);
    req.end();
}

// WordPress に記事を投稿
function publishToWordPress(title, content, category, featuredImage) {
    return new Promise((resolve, reject) => {
        const auth = Buffer.from(WORDPRESS_USER + ":" + WORDPRESS_APP_PASSWORD).toString("base64");
        const postData = JSON.stringify({
            title, content, status: "publish",
            categories: category ? [category] : [],
            featured_media: featuredImage || 0
        });
        const req = http.request({
            hostname: new URL(WORDPRESS_URL).hostname, port: 80, path: "/wp-json/wp/v2/posts", method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": "Basic " + auth, "Content-Length": Buffer.byteLength(postData) }
        }, (res) => {
            let body = "";
            res.on("data", chunk => { body += chunk; });
            res.on("end", () => {
                if (res.statusCode === 201) {
                    const result = JSON.parse(body);
                    resolve({ id: result.id, url: result.link });
                } else reject(new Error("WordPress error: " + res.statusCode));
            });
        });
        req.on("error", reject);
        req.write(postData);
        req.end();
    });
}

// Google Analytics レポートを取得（REST API使用）
async function fetchAnalyticsReport() {
    const config = loadAnalyticsConfig();

    // 本格的なGA Data APIには認証が必要
    // ここでは簡易的なサマリーを生成
    // TODO: サービスアカウント認証を追加してリアルデータを取得

    return new Promise((resolve) => {
        // WordPressの記事統計を取得
        const auth = Buffer.from(WORDPRESS_USER + ":" + WORDPRESS_APP_PASSWORD).toString("base64");
        const postsReq = http.request({
            hostname: new URL(WORDPRESS_URL).hostname,
            port: 80,
            path: "/wp-json/wp/v2/posts?per_page=100&status=publish",
            method: "GET",
            headers: { "Authorization": "Basic " + auth }
        }, (res) => {
            let body = "";
            res.on("data", chunk => { body += chunk; });
            res.on("end", () => {
                try {
                    const posts = JSON.parse(body);
                    const today = new Date();
                    const todayStr = today.toISOString().split('T')[0];
                    const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);

                    // 今日の投稿
                    const todayPosts = posts.filter(p => p.date.startsWith(todayStr));

                    // 今週の投稿
                    const weekPosts = posts.filter(p => new Date(p.date) >= weekAgo);

                    resolve({
                        totalPosts: posts.length,
                        todayPosts: todayPosts.length,
                        weekPosts: weekPosts.length,
                        latestPosts: posts.slice(0, 5).map(p => ({
                            title: p.title.rendered,
                            date: p.date.split('T')[0],
                            url: p.link
                        }))
                    });
                } catch (err) {
                    resolve({
                        totalPosts: 0,
                        todayPosts: 0,
                        weekPosts: 0,
                        latestPosts: [],
                        error: err.message
                    });
                }
            });
        });
        postsReq.on("error", (err) => {
            resolve({ error: err.message });
        });
        postsReq.end();
    });
}

// 日次レポートを生成して送信
async function sendDailyReport() {
    const config = loadAnalyticsConfig();
    const report = await fetchAnalyticsReport();
    const today = new Date();
    const todayStr = today.toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' });

    let message = `📊 K-Trend Times 日次レポート\n`;
    message += `━━━━━━━━━━━━━━━━━━\n`;
    message += `📅 ${todayStr}\n\n`;

    // 記事統計
    message += `📝 記事統計\n`;
    message += `• 総記事数: ${report.totalPosts}件\n`;
    message += `• 今日の投稿: ${report.todayPosts}件\n`;
    message += `• 今週の投稿: ${report.weekPosts}件\n\n`;

    // 最新記事
    if (report.latestPosts && report.latestPosts.length > 0) {
        message += `📰 最新記事\n`;
        report.latestPosts.slice(0, 3).forEach((p, i) => {
            message += `${i + 1}. ${p.title}\n`;
        });
        message += `\n`;
    }

    // Analytics情報（設定済みの場合）
    if (config.measurementId) {
        message += `📈 Google Analytics\n`;
        message += `• Measurement ID: ${config.measurementId}\n`;
        message += `（詳細なアクセス解析はGoogle Analytics管理画面をご確認ください）\n\n`;
    } else {
        message += `ℹ️ Google Analytics未設定\n`;
        message += `設定するには「/analytics G-XXXXXXXXXX」と送信してください\n\n`;
    }

    // AdSense情報（設定済みの場合）
    if (config.adsensePublisherId) {
        message += `💰 Google AdSense\n`;
        message += `• Publisher ID: ${config.adsensePublisherId}\n`;
        message += `（収益情報はAdSense管理画面をご確認ください）\n`;
    } else {
        message += `ℹ️ Google AdSense未設定\n`;
        message += `設定するには「/adsense ca-pub-XXXXXXXXXX」と送信してください\n`;
    }

    // 設定を更新
    config.lastReportDate = today.toISOString().split('T')[0];
    saveAnalyticsConfig(config);

    sendLineMessage(LINE_ADMIN_USER_ID, message);
    console.log("[Report] Daily report sent");
}

// 日次レポートスケジューラー
function startDailyReportScheduler() {
    const checkAndSendReport = () => {
        const config = loadAnalyticsConfig();
        const now = new Date();
        const todayStr = now.toISOString().split('T')[0];
        const [targetHour, targetMinute] = (config.dailyReportTime || "09:00").split(':').map(Number);

        // 今日まだ送信していない && 指定時刻を過ぎている
        if (config.lastReportDate !== todayStr &&
            now.getHours() >= targetHour &&
            (now.getHours() > targetHour || now.getMinutes() >= targetMinute)) {
            sendDailyReport();
        }
    };

    // 1時間ごとにチェック
    setInterval(checkAndSendReport, 60 * 60 * 1000);

    // 起動時にもチェック
    setTimeout(checkAndSendReport, 5000);

    console.log("[Scheduler] Daily report scheduler started");
}

// Claude Code 実行
function executeClaudeCode(prompt) {
    return new Promise((resolve) => {
        console.log("[Claude] Executing:", prompt.substring(0, 100));
        const { execSync } = require("child_process");
        try {
            const result = execSync(`claude -p --dangerously-skip-permissions "${prompt.replace(/"/g, '\\"')}"`, {
                cwd: WORKSPACE,
                env: { ...process.env, CLAUDE_CODE_OAUTH_TOKEN: CLAUDE_OAUTH_TOKEN, HOME: "/home/yuiyane" },
                timeout: 120000, maxBuffer: 10 * 1024 * 1024, encoding: "utf8"
            });
            let output = result || "処理完了（出力なし）";
            if (output.length > 4500) output = output.substring(0, 4500) + "\n...(省略)";
            resolve(output);
        } catch (err) {
            console.error("[Claude] Error:", err.message);
            resolve(err.stdout ? err.stdout.toString() : "エラー: " + err.message);
        }
    });
}

// Claude Code で記事を生成
async function generateArticle(topic) {
    const prompt = `以下のトピックについて、K-POPファン向けのブログ記事を作成してください。

トピック: ${topic}

以下の形式でJSON形式で出力してください:
{
  "title": "記事タイトル（魅力的で検索されやすいもの）",
  "content": "記事本文（HTML形式、見出しh2/h3を使用、1500-2000文字程度）",
  "summary": "記事の要約（100文字程度）",
  "category": "カテゴリ（news/music/drama/fashion/idol のいずれか）"
}

JSONのみを出力し、他の説明は不要です。`;

    const output = await executeClaudeCode(prompt);
    console.log("[Article] Raw output length:", output.length);
    try {
        // JSON コードブロックを抽出
        const codeBlockMatch = output.match(/```json\s*([\s\S]*?)\s*```/);
        if (codeBlockMatch) {
            console.log("[Article] Found JSON in code block");
            return JSON.parse(codeBlockMatch[1]);
        }
        // 直接 JSON を探す
        const jsonMatch = output.match(/\{\s*"title"[\s\S]*?"category"[^}]*\}/);
        if (jsonMatch) {
            console.log("[Article] Found JSON directly");
            return JSON.parse(jsonMatch[0]);
        }
        console.log("[Article] No JSON found in output");
    } catch (err) {
        console.error("[Article] Parse error:", err.message);
        console.error("[Article] Output snippet:", output.substring(0, 500));
    }
    return null;
}

function isArticleRequest(text) {
    return /^記事[:：]/i.test(text) || /^article:/i.test(text);
}

function extractTopic(text) {
    return text.replace(/^(記事[:：]|article:)/i, "").trim();
}

// 未公開記事を取得
function getPendingDrafts() {
    const files = fs.readdirSync(DRAFTS_DIR).filter(f => f.endsWith(".json"));
    const drafts = [];
    for (const file of files) {
        try {
            const draft = JSON.parse(fs.readFileSync(path.join(DRAFTS_DIR, file), "utf8"));
            if (draft.status === "pending") {
                drafts.push(draft);
            }
        } catch (err) {}
    }
    return drafts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
}

// Multipart パーサー（簡易版）
function parseMultipart(buffer, boundary) {
    const parts = {};
    const boundaryBuffer = Buffer.from('--' + boundary);
    let start = buffer.indexOf(boundaryBuffer) + boundaryBuffer.length + 2;

    while (start < buffer.length) {
        const end = buffer.indexOf(boundaryBuffer, start);
        if (end === -1) break;

        const part = buffer.slice(start, end - 2);
        const headerEnd = part.indexOf('\r\n\r\n');
        if (headerEnd === -1) { start = end + boundaryBuffer.length + 2; continue; }

        const headers = part.slice(0, headerEnd).toString();
        const content = part.slice(headerEnd + 4);

        const nameMatch = headers.match(/name="([^"]+)"/);
        const filenameMatch = headers.match(/filename="([^"]+)"/);

        if (nameMatch) {
            if (filenameMatch) {
                parts[nameMatch[1]] = { filename: filenameMatch[1], data: content };
            } else {
                parts[nameMatch[1]] = content.toString();
            }
        }
        start = end + boundaryBuffer.length + 2;
    }
    return parts;
}

const MIME_TYPES = {
    '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript',
    '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp'
};

const server = http.createServer(async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

    const url = new URL(req.url, `http://${req.headers.host}`);

    // ヘルスチェック
    if (req.method === "GET" && url.pathname === "/") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ service: "line-claude-bridge", status: "running", version: "v4" }));
        return;
    }

    // Claude Chat UI
    if (req.method === "GET" && url.pathname === "/chat") {
        const filePath = path.join(PUBLIC_DIR, "claude-chat.html");
        if (fs.existsSync(filePath)) {
            res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
            res.end(fs.readFileSync(filePath));
        } else { res.writeHead(404); res.end("Chat UI not found"); }
        return;
    }

    // 未公開記事一覧ページ
    if (req.method === "GET" && url.pathname === "/drafts") {
        const drafts = getPendingDrafts();
        const html = `<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>未公開記事一覧</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f5f5f5; padding: 16px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 16px; text-align: center; }
        .header h1 { font-size: 20px; }
        .count { font-size: 14px; opacity: 0.9; margin-top: 4px; }
        .draft-list { display: flex; flex-direction: column; gap: 12px; }
        .draft-card { background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .draft-title { font-weight: bold; font-size: 16px; color: #333; margin-bottom: 8px; }
        .draft-meta { font-size: 12px; color: #888; margin-bottom: 12px; }
        .draft-summary { font-size: 14px; color: #666; line-height: 1.5; margin-bottom: 12px; }
        .draft-actions { display: flex; gap: 8px; }
        .btn { flex: 1; padding: 10px; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; text-decoration: none; text-align: center; }
        .btn-edit { background: #667eea; color: white; }
        .btn-view { background: #e0e0e0; color: #333; }
        .empty { text-align: center; padding: 40px; color: #888; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #667eea; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 未公開記事一覧</h1>
        <div class="count">${drafts.length}件の記事</div>
    </div>
    <div class="draft-list">
        ${drafts.length === 0 ? '<div class="empty">未公開の記事はありません</div>' : drafts.map(d => `
        <div class="draft-card">
            <div class="draft-title">${d.title}</div>
            <div class="draft-meta">📁 ${d.category || '未分類'} | 📅 ${new Date(d.created_at).toLocaleDateString('ja-JP')}</div>
            <div class="draft-summary">${(d.summary || '').substring(0, 100)}...</div>
            <div class="draft-actions">
                <a href="/edit/${d.id}" class="btn btn-edit">✏️ 編集</a>
                <a href="/draft/${d.id}" class="btn btn-view">👁 確認</a>
            </div>
        </div>
        `).join('')}
    </div>
    <a href="/chat" class="back-link">← Claude Chat に戻る</a>
</body>
</html>`;
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end(html);
        return;
    }

    // 記事編集ページ
    if (req.method === "GET" && url.pathname.startsWith("/edit/")) {
        const draftId = url.pathname.split("/edit/")[1];
        const draftPath = path.join(DRAFTS_DIR, draftId + ".json");

        if (!fs.existsSync(draftPath)) {
            res.writeHead(404); res.end("Draft not found"); return;
        }

        const draft = JSON.parse(fs.readFileSync(draftPath, "utf8"));
        const html = `<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>記事編集: ${draft.title}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f5f5f5; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px; position: sticky; top: 0; z-index: 100; }
        .header h1 { font-size: 18px; }
        .container { padding: 16px; max-width: 800px; margin: 0 auto; }
        .form-group { margin-bottom: 16px; }
        label { display: block; font-weight: bold; margin-bottom: 6px; color: #333; font-size: 14px; }
        input[type="text"], select, textarea { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; }
        textarea { min-height: 300px; font-family: monospace; line-height: 1.5; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: #667eea; }
        .image-section { background: white; border-radius: 12px; padding: 16px; margin-bottom: 16px; }
        .image-preview { width: 100%; max-height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 12px; display: none; }
        .image-upload { display: flex; gap: 8px; }
        .upload-btn { flex: 1; padding: 12px; background: #f0f0f0; border: 2px dashed #ccc; border-radius: 8px; text-align: center; cursor: pointer; }
        .upload-btn:hover { background: #e8e8e8; }
        input[type="file"] { display: none; }
        .actions { display: flex; gap: 12px; margin-top: 20px; padding-bottom: 40px; }
        .btn { flex: 1; padding: 14px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }
        .btn-save { background: #1DB446; color: white; }
        .btn-cancel { background: #e0e0e0; color: #333; }
        .btn:disabled { opacity: 0.5; }
        .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #333; color: white; padding: 12px 24px; border-radius: 8px; display: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>✏️ 記事編集</h1>
    </div>
    <div class="container">
        <form id="editForm">
            <div class="form-group">
                <label>タイトル</label>
                <input type="text" id="title" value="${draft.title.replace(/"/g, '&quot;')}" required>
            </div>

            <div class="image-section">
                <label>アイキャッチ画像</label>
                <img id="imagePreview" class="image-preview" src="${draft.image || ''}" style="${draft.image ? 'display:block' : ''}">
                <div class="image-upload">
                    <label class="upload-btn" for="imageFile">📷 画像を選択</label>
                    <input type="file" id="imageFile" accept="image/*">
                </div>
                <div class="form-group" style="margin-top: 12px;">
                    <label>画像クレジット（例: Photo by BigHit Music）</label>
                    <input type="text" id="imageCredit" placeholder="画像の出典やクレジットを入力" value="${draft.imageCredit || ''}">
                </div>
            </div>

            <div class="form-group">
                <label>カテゴリ</label>
                <select id="category">
                    <option value="news" ${draft.category === 'news' ? 'selected' : ''}>ニュース</option>
                    <option value="music" ${draft.category === 'music' ? 'selected' : ''}>音楽</option>
                    <option value="drama" ${draft.category === 'drama' ? 'selected' : ''}>ドラマ</option>
                    <option value="fashion" ${draft.category === 'fashion' ? 'selected' : ''}>ファッション</option>
                    <option value="idol" ${draft.category === 'idol' ? 'selected' : ''}>アイドル</option>
                </select>
            </div>

            <div class="form-group">
                <label>要約</label>
                <textarea id="summary" rows="3">${draft.summary || ''}</textarea>
            </div>

            <div class="form-group">
                <label>本文 (HTML)</label>
                <textarea id="content">${draft.content.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</textarea>
            </div>

            <div class="actions">
                <button type="button" class="btn btn-cancel" onclick="location.href='/drafts'">キャンセル</button>
                <button type="submit" class="btn btn-save" id="saveBtn">💾 保存</button>
            </div>
        </form>
    </div>
    <div class="toast" id="toast"></div>

    <script>
        const draftId = "${draftId}";
        let imageData = ${draft.image ? '"' + draft.image + '"' : 'null'};

        document.getElementById('imageFile').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('imagePreview').src = e.target.result;
                    document.getElementById('imagePreview').style.display = 'block';
                    imageData = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });

        document.getElementById('editForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const btn = document.getElementById('saveBtn');
            btn.disabled = true;
            btn.textContent = '保存中...';

            try {
                const response = await fetch('/api/draft/' + draftId, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: document.getElementById('title').value,
                        category: document.getElementById('category').value,
                        summary: document.getElementById('summary').value,
                        content: document.getElementById('content').value,
                        image: imageData,
                        imageCredit: document.getElementById('imageCredit').value
                    })
                });

                if (response.ok) {
                    showToast('✅ 保存しました');
                    setTimeout(() => location.href = '/drafts', 1000);
                } else {
                    throw new Error('保存に失敗しました');
                }
            } catch (err) {
                showToast('❌ ' + err.message);
                btn.disabled = false;
                btn.textContent = '💾 保存';
            }
        });

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.style.display = 'block';
            setTimeout(() => toast.style.display = 'none', 3000);
        }
    </script>
</body>
</html>`;
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end(html);
        return;
    }

    // 記事更新API
    if (req.method === "PUT" && url.pathname.startsWith("/api/draft/")) {
        const draftId = url.pathname.split("/api/draft/")[1];
        const draftPath = path.join(DRAFTS_DIR, draftId + ".json");

        if (!fs.existsSync(draftPath)) {
            res.writeHead(404, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ error: "Draft not found" }));
            return;
        }

        let body = "";
        req.on("data", chunk => { body += chunk; });
        req.on("end", () => {
            try {
                const updates = JSON.parse(body);
                const draft = JSON.parse(fs.readFileSync(draftPath, "utf8"));

                // 更新
                if (updates.title) draft.title = updates.title;
                if (updates.category) draft.category = updates.category;
                if (updates.summary) draft.summary = updates.summary;
                if (updates.content) draft.content = updates.content;
                if (updates.image !== undefined) draft.image = updates.image;
                if (updates.imageCredit !== undefined) draft.imageCredit = updates.imageCredit;
                draft.updated_at = new Date().toISOString();

                fs.writeFileSync(draftPath, JSON.stringify(draft, null, 2));

                res.writeHead(200, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ success: true, draft }));
            } catch (err) {
                res.writeHead(500, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ error: err.message }));
            }
        });
        return;
    }

    // 画像配信
    if (req.method === "GET" && url.pathname.startsWith("/uploads/")) {
        const filePath = path.join(UPLOADS_DIR, url.pathname.replace("/uploads/", ""));
        if (fs.existsSync(filePath)) {
            const ext = path.extname(filePath).toLowerCase();
            res.writeHead(200, { "Content-Type": MIME_TYPES[ext] || "application/octet-stream" });
            res.end(fs.readFileSync(filePath));
        } else { res.writeHead(404); res.end("Not found"); }
        return;
    }

    // Analytics設定ページ
    if (req.method === "GET" && url.pathname === "/settings") {
        const config = loadAnalyticsConfig();
        const html = `<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>設定 - K-Trend Times</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f5f5f5; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
        .header h1 { font-size: 20px; }
        .container { padding: 16px; max-width: 600px; margin: 0 auto; }
        .card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .card h2 { font-size: 16px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
        .form-group { margin-bottom: 16px; }
        label { display: block; font-size: 14px; color: #666; margin-bottom: 6px; }
        input { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; }
        input:focus { outline: none; border-color: #667eea; }
        .btn { width: 100%; padding: 14px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }
        .btn-save { background: #1DB446; color: white; }
        .btn-report { background: #667eea; color: white; margin-top: 12px; }
        .status { padding: 8px 12px; border-radius: 6px; font-size: 14px; margin-bottom: 12px; }
        .status.configured { background: #d4edda; color: #155724; }
        .status.not-configured { background: #fff3cd; color: #856404; }
        .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #333; color: white; padding: 12px 24px; border-radius: 8px; display: none; }
        .back-link { display: block; text-align: center; margin-top: 20px; color: #667eea; }
        .code-block { background: #f8f9fa; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 12px; overflow-x: auto; margin-top: 8px; white-space: pre-wrap; word-break: break-all; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚙️ 設定</h1>
    </div>
    <div class="container">
        <div class="card">
            <h2>📈 Google Analytics</h2>
            <div class="status ${config.measurementId ? 'configured' : 'not-configured'}">
                ${config.measurementId ? '✅ 設定済み: ' + config.measurementId : '⚠️ 未設定'}
            </div>
            <div class="form-group">
                <label>Measurement ID</label>
                <input type="text" id="measurementId" value="${config.measurementId || ''}" placeholder="G-XXXXXXXXXX">
            </div>
            ${config.measurementId ? '<div><label>トラッキングコード（WordPressに追加）</label><div class="code-block">&lt;script async src="https://www.googletagmanager.com/gtag/js?id=' + config.measurementId + '"&gt;&lt;/script&gt;\n&lt;script&gt;\nwindow.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag(&#39;js&#39;, new Date());\ngtag(&#39;config&#39;, &#39;' + config.measurementId + '&#39;);\n&lt;/script&gt;</div></div>' : ''}
        </div>

        <div class="card">
            <h2>💰 Google AdSense</h2>
            <div class="status ${config.adsensePublisherId ? 'configured' : 'not-configured'}">
                ${config.adsensePublisherId ? '✅ 設定済み: ' + config.adsensePublisherId : '⚠️ 未設定'}
            </div>
            <div class="form-group">
                <label>Publisher ID</label>
                <input type="text" id="adsensePublisherId" value="${config.adsensePublisherId || ''}" placeholder="ca-pub-XXXXXXXXXX">
            </div>
            ${config.adsensePublisherId ? '<div><label>広告コード（WordPressに追加）</label><div class="code-block">&lt;script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + config.adsensePublisherId + '" crossorigin="anonymous"&gt;&lt;/script&gt;</div></div>' : ''}
        </div>

        <div class="card">
            <h2>📅 日次レポート</h2>
            <div class="form-group">
                <label>送信時刻</label>
                <input type="time" id="dailyReportTime" value="${config.dailyReportTime || '09:00'}">
            </div>
            <div class="form-group">
                <label>最終送信日</label>
                <input type="text" value="${config.lastReportDate || '未送信'}" disabled>
            </div>
            <button class="btn btn-report" onclick="sendReport()">📊 今すぐレポート送信</button>
        </div>

        <button class="btn btn-save" onclick="saveSettings()">💾 設定を保存</button>
        <a href="/chat" class="back-link">← Claude Chat に戻る</a>
    </div>
    <div class="toast" id="toast"></div>

    <script>
        async function saveSettings() {
            const data = {
                measurementId: document.getElementById('measurementId').value || null,
                adsensePublisherId: document.getElementById('adsensePublisherId').value || null,
                dailyReportTime: document.getElementById('dailyReportTime').value
            };

            try {
                const res = await fetch('/api/settings', {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (res.ok) {
                    showToast('✅ 設定を保存しました');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    throw new Error('保存に失敗しました');
                }
            } catch (err) {
                showToast('❌ ' + err.message);
            }
        }

        async function sendReport() {
            showToast('📊 レポートを送信中...');
            try {
                const res = await fetch('/api/report', { method: 'POST' });
                if (res.ok) {
                    showToast('✅ レポートを送信しました');
                } else {
                    throw new Error('送信に失敗しました');
                }
            } catch (err) {
                showToast('❌ ' + err.message);
            }
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.style.display = 'block';
            setTimeout(() => toast.style.display = 'none', 3000);
        }
    </script>
</body>
</html>`;
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end(html);
        return;
    }

    // Analytics設定API
    if (req.method === "PUT" && url.pathname === "/api/settings") {
        let body = "";
        req.on("data", chunk => { body += chunk; });
        req.on("end", () => {
            try {
                const updates = JSON.parse(body);
                const config = loadAnalyticsConfig();

                if (updates.measurementId !== undefined) {
                    config.measurementId = updates.measurementId;
                }
                if (updates.adsensePublisherId !== undefined) {
                    config.adsensePublisherId = updates.adsensePublisherId;
                }
                if (updates.dailyReportTime) {
                    config.dailyReportTime = updates.dailyReportTime;
                }

                saveAnalyticsConfig(config);

                res.writeHead(200, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ success: true, config }));
            } catch (err) {
                res.writeHead(500, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ error: err.message }));
            }
        });
        return;
    }

    // レポート手動送信API
    if (req.method === "POST" && url.pathname === "/api/report") {
        sendDailyReport();
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ success: true, message: "Report sent" }));
        return;
    }

    // Chat API
    if (req.method === "POST" && url.pathname === "/api/chat") {
        let body = "";
        req.on("data", chunk => { body += chunk; });
        req.on("end", async () => {
            try {
                const data = JSON.parse(body);
                const message = data.message;

                if (!message) {
                    res.writeHead(400, { "Content-Type": "application/json" });
                    res.end(JSON.stringify({ error: "message is required" }));
                    return;
                }

                if (message === "/status") {
                    const drafts = fs.readdirSync(DRAFTS_DIR).filter(f => f.endsWith(".json")).length;
                    res.writeHead(200, { "Content-Type": "application/json" });
                    res.end(JSON.stringify({ response: "✅ システム稼働中\n\n• Claude Code: 有効\n• 記事生成: 有効\n• 下書き数: " + drafts }));
                    return;
                }

                if (message === "/help") {
                    res.writeHead(200, { "Content-Type": "application/json" });
                    res.end(JSON.stringify({ response: "📖 コマンド一覧\n\n• /status - システム状態\n• /help - このヘルプ\n• 記事: [トピック] - 記事生成" }));
                    return;
                }

                if (isArticleRequest(message)) {
                    const topic = extractTopic(message);
                    if (!topic || topic.trim() === "") {
                        res.writeHead(200, { "Content-Type": "application/json" });
                        res.end(JSON.stringify({ response: "📝 記事を作成するには、トピックを入力してください。\n\n例: 記事: BTSの新曲\n例: 記事: IVEの日本デビュー" }));
                        return;
                    }
                    const article = await generateArticle(topic);

                    if (article) {
                        const draftId = generateId();
                        const draft = {
                            id: draftId, title: article.title, content: article.content,
                            summary: article.summary, category: article.category,
                            status: "pending", created_at: new Date().toISOString()
                        };
                        fs.writeFileSync(path.join(DRAFTS_DIR, draftId + ".json"), JSON.stringify(draft, null, 2));
                        sendArticleApprovalMessage(LINE_ADMIN_USER_ID, draftId, article.title, article.summary);

                        res.writeHead(200, { "Content-Type": "application/json" });
                        res.end(JSON.stringify({
                            response: "📝 記事を生成しました！\n\n【タイトル】\n" + article.title + "\n\n✅ LINEに承認ボタンを送信しました。"
                        }));
                    } else {
                        res.writeHead(200, { "Content-Type": "application/json" });
                        res.end(JSON.stringify({ response: "❌ 記事の生成に失敗しました。" }));
                    }
                    return;
                }

                const result = await executeClaudeCode(message);
                res.writeHead(200, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ response: result }));
            } catch (err) {
                res.writeHead(500, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ error: err.message }));
            }
        });
        return;
    }

    // ドラフトプレビュー
    if (req.method === "GET" && url.pathname.startsWith("/draft/")) {
        const draftId = url.pathname.split("/draft/")[1];
        const draftPath = path.join(DRAFTS_DIR, draftId + ".json");

        if (fs.existsSync(draftPath)) {
            const draft = JSON.parse(fs.readFileSync(draftPath, "utf8"));
            const html = `<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${draft.title}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; border-bottom: 2px solid #1DB446; padding-bottom: 10px; }
        .meta { color: #666; font-size: 14px; margin-bottom: 20px; }
        .featured-image { width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 4px; }
        .image-credit { font-size: 0.75rem; color: #666; font-style: italic; text-align: right; margin-bottom: 20px; }
        .image-credit::before { content: "📷 "; opacity: 0.7; }
        .content { line-height: 1.8; }
        .status { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .status.pending { background: #fff3cd; color: #856404; }
        .status.published { background: #d4edda; color: #155724; }
        .edit-btn { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="meta">
        <span class="status ${draft.status}">${draft.status.toUpperCase()}</span>
        <span style="margin-left: 10px;">📁 ${draft.category || "未分類"}</span>
    </div>
    ${draft.image ? '<img src="' + draft.image + '" class="featured-image">' : ''}
    ${draft.imageCredit ? '<div class="image-credit">' + draft.imageCredit + '</div>' : ''}
    <h1>${draft.title}</h1>
    <div class="content">${draft.content}</div>
    <a href="/edit/${draft.id}" class="edit-btn">✏️ 編集する</a>
</body>
</html>`;
            res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
            res.end(html);
        } else {
            res.writeHead(404, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ error: "Draft not found" }));
        }
        return;
    }

    // LINE Webhook
    if (req.method === "POST" && url.pathname === "/webhook") {
        let body = "";
        req.on("data", chunk => { body += chunk; });
        req.on("end", async () => {
            const signature = req.headers["x-line-signature"];
            if (signature && !verifySignature(body, signature)) {
                res.writeHead(401); res.end("Invalid signature"); return;
            }
            res.writeHead(200);
            res.end(JSON.stringify({ status: "ok" }));

            try {
                const data = JSON.parse(body);

                for (const event of data.events || []) {
                    const userId = event.source && event.source.userId;

                    if (event.type === "postback") {
                        const postbackData = event.postback.data;
                        const params = {};
                        postbackData.split("&").forEach(p => { const [k, v] = p.split("="); params[k] = v; });

                        if (params.action === "approve_article") {
                            const draftPath = path.join(DRAFTS_DIR, params.draft_id + ".json");
                            if (fs.existsSync(draftPath)) {
                                const draft = JSON.parse(fs.readFileSync(draftPath, "utf8"));
                                sendLineMessage(userId, "📤 WordPressに公開中...");
                                try {
                                    const result = await publishToWordPress(draft.title, draft.content, draft.category);
                                    draft.status = "published";
                                    draft.wordpress_id = result.id;
                                    draft.wordpress_url = result.url;
                                    fs.writeFileSync(draftPath, JSON.stringify(draft, null, 2));
                                    sendLineMessage(userId, "✅ 公開完了!\n\n" + draft.title + "\n\n" + result.url);
                                } catch (err) {
                                    sendLineMessage(userId, "❌ 公開エラー: " + err.message);
                                }
                            }
                            continue;
                        }

                        if (params.action === "reject_article") {
                            const draftPath = path.join(DRAFTS_DIR, params.draft_id + ".json");
                            if (fs.existsSync(draftPath)) {
                                const draft = JSON.parse(fs.readFileSync(draftPath, "utf8"));
                                draft.status = "rejected";
                                fs.writeFileSync(draftPath, JSON.stringify(draft, null, 2));
                                sendLineMessage(userId, "🗑 記事を却下しました: " + draft.title);
                            }
                            continue;
                        }
                        continue;
                    }

                    if (userId !== LINE_ADMIN_USER_ID) continue;

                    if (event.type === "message" && event.message && event.message.type === "text") {
                        const text = event.message.text;

                        if (text === "/status") {
                            const drafts = getPendingDrafts().length;
                            sendLineMessage(userId, "✅ システム稼働中\n\n• 未公開記事: " + drafts + "件\n• 記事一覧: " + BASE_URL + "/drafts");
                            continue;
                        }

                        if (text === "/help") {
                            sendLineMessage(userId, "📖 コマンド一覧\n\n• /status - システム状態\n• /help - このヘルプ\n• /report - 日次レポート送信\n• /analytics G-XXXXX - Analytics設定\n• /adsense ca-pub-XXXXX - AdSense設定\n• 記事: [トピック] - 記事生成\n\n📋 未公開記事一覧:\n" + BASE_URL + "/drafts");
                            continue;
                        }

                        // 日次レポートを手動送信
                        if (text === "/report") {
                            sendLineMessage(userId, "📊 レポートを生成中...");
                            await sendDailyReport();
                            continue;
                        }

                        // Google Analytics設定
                        if (text.startsWith("/analytics ")) {
                            const measurementId = text.replace("/analytics ", "").trim();
                            if (measurementId.startsWith("G-")) {
                                const config = loadAnalyticsConfig();
                                config.measurementId = measurementId;
                                saveAnalyticsConfig(config);
                                sendLineMessage(userId, `✅ Google Analytics設定完了\n\nMeasurement ID: ${measurementId}\n\nWordPressにトラッキングコードを追加してください:\n\n<script async src="https://www.googletagmanager.com/gtag/js?id=${measurementId}"></script>\n<script>\nwindow.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\ngtag('config', '${measurementId}');\n</script>`);
                            } else {
                                sendLineMessage(userId, "❌ Measurement IDは「G-」で始まる形式です\n\n例: /analytics G-XXXXXXXXXX");
                            }
                            continue;
                        }

                        // Google AdSense設定
                        if (text.startsWith("/adsense ")) {
                            const publisherId = text.replace("/adsense ", "").trim();
                            if (publisherId.startsWith("ca-pub-")) {
                                const config = loadAnalyticsConfig();
                                config.adsensePublisherId = publisherId;
                                saveAnalyticsConfig(config);
                                sendLineMessage(userId, `✅ Google AdSense設定完了\n\nPublisher ID: ${publisherId}\n\nWordPressの<head>に以下を追加してください:\n\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${publisherId}" crossorigin="anonymous"></script>`);
                            } else {
                                sendLineMessage(userId, "❌ Publisher IDは「ca-pub-」で始まる形式です\n\n例: /adsense ca-pub-1234567890123456");
                            }
                            continue;
                        }

                        if (isArticleRequest(text)) {
                            const topic = extractTopic(text);
                            if (!topic || topic.trim() === "") {
                                sendLineMessage(userId, "📝 記事を作成するには、トピックを入力してください。\n\n例: 記事: BTSの新曲\n例: 記事: IVEの日本デビュー");
                                continue;
                            }
                            sendLineMessage(userId, "📝 記事を生成中...\n\nトピック: " + topic);
                            const article = await generateArticle(topic);

                            if (article) {
                                const draftId = generateId();
                                const draft = { id: draftId, title: article.title, content: article.content, summary: article.summary, category: article.category, status: "pending", created_at: new Date().toISOString() };
                                fs.writeFileSync(path.join(DRAFTS_DIR, draftId + ".json"), JSON.stringify(draft, null, 2));
                                sendArticleApprovalMessage(userId, draftId, article.title, article.summary);
                            } else {
                                sendLineMessage(userId, "❌ 記事の生成に失敗しました。");
                            }
                            continue;
                        }
                    }
                }
            } catch (err) {
                console.error("[Error]", err.message);
            }
        });
        return;
    }

    res.writeHead(404);
    res.end("Not Found");
});

server.listen(PORT, () => {
    console.log("=================================");
    console.log("LINE-Claude Bridge (v5)");
    console.log("=================================");
    console.log("Port:", PORT);
    console.log("Drafts:", BASE_URL + "/drafts");
    console.log("Chat:", BASE_URL + "/chat");
    console.log("=================================");

    // 日次レポートスケジューラーを開始
    startDailyReportScheduler();

    // Analytics設定を表示
    const config = loadAnalyticsConfig();
    console.log("Analytics Measurement ID:", config.measurementId || "(未設定)");
    console.log("AdSense Publisher ID:", config.adsensePublisherId || "(未設定)");
    console.log("Daily Report Time:", config.dailyReportTime);
    console.log("=================================");
});
