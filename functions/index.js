const functions = require('@google-cloud/functions-framework');
const http = require('http');

const VM_URL = 'http://34.146.62.216:8080';

// Webhook proxy - forwards all requests to VM
functions.http('webhook', async (req, res) => {
    const body = JSON.stringify(req.body);

    const options = {
        hostname: '34.146.62.216',
        port: 8080,
        path: '/webhook',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body),
            'x-line-signature': req.headers['x-line-signature'] || ''
        }
    };

    try {
        const proxyReq = http.request(options, (proxyRes) => {
            let responseBody = '';
            proxyRes.on('data', chunk => { responseBody += chunk; });
            proxyRes.on('end', () => {
                res.status(proxyRes.statusCode).send(responseBody);
            });
        });

        proxyReq.on('error', (err) => {
            console.error('Proxy error:', err.message);
            res.status(500).json({ error: err.message });
        });

        proxyReq.write(body);
        proxyReq.end();
    } catch (err) {
        console.error('Error:', err.message);
        res.status(500).json({ error: err.message });
    }
});
