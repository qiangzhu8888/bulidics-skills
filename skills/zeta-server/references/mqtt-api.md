# MQTT API — センサーの上行データを受信

既存資料で確認できる接続先例: `tcp://en-apis.zifisense.com:1883`、独立設置 `tcp://<ip>:1883`。本番ではTLS対応とアクセス制御を確認する。

認証: `api_key` / `api_secret`。clientIDは一意である必要がある。

トピック例:
- 基地局ハートビート: `{api_key}/v1/ap/{uid}/heartbeat`
- 端末の上行解析データ: `{api_key}/jll/property/ms/{uid}/updata`
- 企業単位の端末購読例: `{api_key}/jll/property/ms/+/updata`

`updata` は元資料の表記。`update` に書き換えない。

上行メッセージ例には `deviceId`, `deviceType`, `upTime`, `data`, `dataDetail` がある。`dataDetail` はJSON文字列で届く場合がある。

注意: 既存資料にはMQTTバージョンによるワイルドカード制約の記述がある。利用サーバーで実際の対応状況を確認する。下行制御はこの入門版の対象外。

元資料: `skills/agentic-iot-architect/references/zeta-api/mqtt-api.md`（GitHub）