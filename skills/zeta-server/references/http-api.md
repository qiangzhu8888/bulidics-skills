# HTTP API — 認証から始める

既存のZETA HTTP資料で確認できるエンドポイント:

- クラウド（中国） `https://cn-apis.zifisense.com/`
- クラウド（海外） `https://en-apis.zifisense.com/`
- 独立設置 `http://<server-ip>:25455/` （TLS構成は運用環境で確認）
- Token: `GET /teamcms/ws/auth_v2/auth_token/query/getWanAccessToken?api_key=...&signal=...&request_time=...`
- `request_time`: 秒単位Unix timestamp。サーバーとの時差は3分以内。
- `signal`: HMAC-SHA1。メッセージは `api_key`、鍵は `api_secret + request_time`。
- Token有効期間: 2時間。
- 成功応答例: `{ "status":0, "data":[{"access_token":"..."}], "errmsg":"", "ts": 175907811 }`

## 注意
実際のAPIキーと秘密鍵はチャット、ログ、GitHub、URL例に記載しない。スクリプトの署名生成結果は機密情報として扱う。公開ネットワークでHTTP平文の独立設置サーバーを使用しない。

元資料: `skills/agentic-iot-architect/references/zeta-api/http-api.md`（GitHub）