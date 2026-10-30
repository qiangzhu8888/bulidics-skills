# Cloud Integrator Webhook

確認日: 2026-10-30。公開仕様確認のみ。契約アカウント未検証。

## 準備と設定

1. センサーが1NCE OSへUDP、CoAP、LwM2Mで送信できることを確認する。型番、ファーム、契約・リージョン別の接続先を確認する。
2. 自社に有効なTLS証明書のHTTPS POST受信APIを作る。例: `https://ingest.example.com/webhooks/1nce`。
3. Cloud Integratorで名前、URL、Event Types TELEMETRY_DATAを指定する。
4. Custom HTTP Headersにx-api-keyを設定し、受信側で検証する。自社発行のWebhook専用キーを使い、OAuth資格情報と分離する。
5. JSON機器はParse JSON payloadを有効化する。非JSONの入力はBase64になる場合がある。
6. TEST_MESSAGEと実機TELEMETRY_DATAの両方を確認する。テストにdevice/payloadがなくても不正としない。

APIでも登録可能。次は公式掲載例を基にしたbody。Platform v2資料にも/v1/が残るため、現行の利用可否を確認する。作成などの変更操作は依頼範囲内で行う。

```http
POST /v1/integrate/clouds/webhooks
Authorization: Bearer <1NCE OAuth token>
Content-Type: application/json

{
  "name": "BUILDICS",
  "url": "https://ingest.example.com/webhooks/1nce",
  "headers": {"x-api-key": "<自社のWebhook受信用キー>"},
  "eventTypes": [{"type": "TELEMETRY_DATA"}]
}
```
テスト: POST `/v1/integrate/clouds/webhooks/{integrationId}/test`。
再開: POST `/v1/integrate/clouds/webhooks/{integrationId}/restart`。

公式資料:
- https://help.1nce.com/docs/v2/1nce-os/1nce-os-device-integrator/
- https://help.1nce.com/docs/v2/1nce-os/1nce-os-cloud-integrator/cloud-integrator-webhook-configuration/

## イベント形式

以下は公式envelopeを基にした架空の測定値例。測定項目はメーカー固有。
```json
{
  "id": "example-001",
  "type": "TELEMETRY_DATA",
  "source": "COAP",
  "version": "1.0.0",
  "received": "1793347200000",
  "device": {"iccid": "8988280666000000000"},
  "payload": {"type": "JSON", "value": {"temperature": 24.6, "humidity": 58}}
}
```
idはメッセージID、receivedはUNIXミリ秒の受信時刻で測定時刻とは限らない。ICCIDは文字列で保存する。
payload.typeはJSONまたはSTRING。rawデータにはencoding: base64が付く。デコード後のバイナリはメーカー仕様で解釈する。

公式資料:
- https://help.1nce.com/docs/v2/1nce-os/1nce-os-cloud-integrator/cloud-integrator-output-format/

## 受信側の実装方針（自社設計）

- POST限定、本文サイズ制限、定数時間比較でキー検証を実装し、認証情報をログに出さない。
- JSONとイベントを検証し、テストと測定値を分ける。
- DBまたは永続キューへ保存後に2xxを返す。永続化失敗時は非2xxとする。メモリー追加だけで受信完了としない。
- `(integration_id, event.id)`を一意にし、再送で通知や登録が重複しないようにする。
- 非同期で解析・機器紐付け・単位変換・警報判定する。未知形式や未登録ICCIDは元データ付きで隔離する。
- 最終受信時刻、処理失敗、連携状態を監視する。

## 公式の配信要件

HTTPS POSTのみ。20秒以内に2xx。自己署名証明書は不可。同じURLを複数Webhookへ同時登録できない。
初回含め計5回の試行。再試行間隔の例は150/180/420/1020秒。失敗継続でINTEGRATION_FAILEDとなり、手動再開する。
再開による過去データ全件再配信を仮定しない。欠損期間を照合し、可能ならHistorianで補完する。
IP制限が必要なら契約リージョンの現行送信元IPを確認する。固定IPを本資料では保証しない。
Data Streamerの一括配列・Basic認証と、Cloud Integratorのイベント形式・独自ヘッダーを混同しない。

公式資料:
- https://help.1nce.com/docs/v2/1nce-os/1nce-os-cloud-integrator/cloud-integrator-features-limitations/
