#!/bin/bash
# ============================================
# Let's Encrypt SSL証明書 初期取得スクリプト
# ============================================

set -e

# ドメイン設定
DOMAIN="${DOMAIN:-k-trendtimes.com}"
EMAIL="${EMAIL:-admin@k-trendtimes.com}"

echo "============================================"
echo "SSL証明書を取得します"
echo "ドメイン: $DOMAIN"
echo "メール: $EMAIL"
echo "============================================"

# ディレクトリ作成
mkdir -p ./certbot/www
mkdir -p ./certbot/conf

# 一時的なNginx設定 (HTTP only)
cat > ./nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name k-trendtimes.com www.k-trendtimes.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 200 'SSL setup in progress...';
        add_header Content-Type text/plain;
    }
}
EOF

echo "1. Nginxを起動中 (HTTP only)..."
docker compose up -d nginx

sleep 5

echo "2. SSL証明書を取得中..."
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

echo "3. Nginx設定をHTTPSに切り替え中..."

# 本番用Nginx設定に戻す
cat > ./nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name k-trendtimes.com www.k-trendtimes.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name k-trendtimes.com www.k-trendtimes.com;

    ssl_certificate /etc/letsencrypt/live/k-trendtimes.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/k-trendtimes.com/privkey.pem;

    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    add_header Strict-Transport-Security "max-age=63072000" always;

    root /var/www/html;
    index index.php index.html;

    client_max_body_size 100M;

    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json application/xml image/svg+xml;

    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|svg|webp)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass wordpress:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_read_timeout 300;
    }

    location ~ /\. {
        deny all;
    }

    location ~* wp-config\.php {
        deny all;
    }

    location = /xmlrpc.php {
        deny all;
    }
}
EOF

echo "4. 全サービスを再起動中..."
docker compose down
docker compose up -d

echo ""
echo "============================================"
echo "SSL証明書の取得が完了しました!"
echo "https://$DOMAIN でアクセスできます"
echo "============================================"
