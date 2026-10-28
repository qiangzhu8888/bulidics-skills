# Sensor Codecs — データを意味ある値へ

既存資料の共通項目:
- `dataStatus`: `normal`（通常）, `warning`（警報）, `recovery`（解除）, `resp`（応答）, `illegal`（解析不可）
- `completeData`: 解析済みの説明文字列（型番により異なる）
- 個別センサー値: `{ "name": "温度", "unit": "℃", "value": "-0.2" }` のような構造

**必須手順**: デバイスの製品型番・コード・プロトコル版数を特定し、該当モデルの仕様でデコードする。型番未確認の生バイト列を独自推定で解析しない。

元資料は `301-ZETA端智能温度传感器-ZAIoT-TD01` などのモデル別フィールドを掲載している。網羅的なコード表はGitHubの `skills/agentic-iot-architect/references/zeta-api/sensor-codecs.md` を参照。