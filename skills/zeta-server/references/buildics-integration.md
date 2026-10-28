# BUILDICS連携 — 推奨する正規化イベント

ZETA MQTT/HTTPの結果を、以下のような内部イベントに正規化してからBUILDICSへ渡す（**以下は提案スキーマでありBUILDICSの既存API仕様ではない**）。

```json
{
  "source": "zeta-server",
  "device_id": "00000001",
  "observed_at": "2026-10-28T12:00:00Z",
  "status": "warning",
  "measurements": {"temperature_c": 35.2},
  "raw_message_id": "example-id"
}
```

対応付け: ZETA `deviceId` → BUILDICS設備/デバイスID → 計測ポイントID。再送時の重複排除、タイムスタンプ検証、単位変換、品質フラグ、通信断を設計する。BUILDICS APIの実際のエンドポイント・認証方式は `bulidics-api` Skillで確認する。

Agentic IoTでは `warning` だけで自動制御せず、設備位置・履歴・担当者・優先度を付加して具体的な点検提案を生成する。