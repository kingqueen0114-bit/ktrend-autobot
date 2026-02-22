FROM node:18-slim

# 作業ディレクトリ
WORKDIR /app

# アプリケーションファイルをコピー
COPY server.js .
COPY analytics-config.json .
COPY public ./public

# 必要なディレクトリを作成
RUN mkdir -p /home/workspace/drafts /home/workspace/uploads

# ポート8080を公開
EXPOSE 8080

# 環境変数設定（Cloud Runのデフォルト）
ENV PORT=8080
ENV NODE_ENV=production

# サーバー起動
CMD ["node", "server.js"]
