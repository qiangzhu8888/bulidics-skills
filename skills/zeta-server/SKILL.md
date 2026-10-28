---
name: zeta-server
description: Connect, inspect, and integrate ZiFiSense ZETA Server with BUILDICS and Agentic IoT. Use for ZETA HTTP API authentication, MQTT uplink topics, sensor payload decoding, device-data retrieval examples, troubleshooting, and safe read-only integration prototypes. Explain workflows in Japanese with runnable examples and distinguish verified endpoints from illustrative code.
---

# ZETA SERVER — すぐ使えるガイド

## まず、やりたいことを選ぶ

| 目的 | 参照 | 最初の成果物 |
| --- | --- | --- |
| 接続・認証を試す | `references/http-api.md` | Access Token取得のサンプル |
| MQTTで受信する | `references/mqtt-api.md` | Topicと購読コード |
| センサー値を読む | `references/sensor-codecs.md` | dataDetailの正規化 |
| BUILDICSへ連携する | `references/buildics-integration.md` | 共通イベント形式と接続設計 |
| まず動かしてみる | `references/quick-start.md` | ローカルのデモ |

## 標準フロー
1. 最初に「認証」「MQTT受信」「デコード」「BUILDICS連携」のどれかを特定する。
2. 該当するreferencesだけを読み、確認済み仕様と例示を区別する。
3. 最初は読み取り専用でサンプルを作る。秘密情報は環境変数またはSecret Managerを使う。
4. ZETA生データ → 構造化センサーイベント → BUILDICSのデータポイント → Agentic IoTの状態/行動提案、の順で設計する。
5. 実機操作・下行制御・設定変更は必ず権限、対象、影響、承認を確認し、明示的な許可なしに実行しない。
6. 通信方式、エンドポイント、デバイス型番、データフィールドが未確認なら推測で埋めない。

## 利用できるスクリプト
`python scripts/zeta_helper.py sign --api-key DEMO --secret-key DEMO --request-time 1645068740`
`python scripts/zeta_helper.py decode --json '{"dataDetail":"{\"dataStatus\":\"normal\"}"}'`

## 仕様の出所と限界
このパッケージは既存GitHubの `skills/agentic-iot-architect/references/zeta-api/` にあるHTTP/MQTT/codec資料を読みやすく整理した入門版。網羅的なAPI仕様は元のGitHub資料を参照。API接続・デバイス取得の本番実証は未実施。実際のサーバー版数、TLS、認証・購読制約を運用環境で確認すること。