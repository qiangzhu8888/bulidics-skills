# BULIDICS Agent Skills

Portable skills for implementing and operating BULIDICS integrations and Agentic IoT design in Codex, Cursor, and other Agent Skills-compatible tools.

## Included skills

| Skill | Purpose |
|---|---|
| `aimeet-ui-design` | Build and improve AiMeet exhibitor list/detail pages using bundled HTML/CSS references, a React card, and visual QA guidance. |
| `integrate-1nce` | Implement 1NCE OAuth, SIM management, Historian REST retrieval, and telemetry webhooks for BUILDICS. |
| `agentic-iot-architect` | Design, diagnose, and transform IoT systems using Agentic IoT concepts, including ZiFiSense ZETA Server API & MQTT integrations. |
| `bulidics-api` | Implement and review BULIDICS HTTP push v1.0 and RESTful API v1.0.2 integrations. |
| `bulidics-water-leak-monitor` | Evaluate water-leak sensor state, transition history, duplicate delivery, communication freshness, and polling data-loss risk. |
| `agentic-iot-architect` | Design, diagnose, and transform IoT systems from monitoring/visualization into context-aware decision and action flows using the Agentic IoT framework. |

Each folder under `skills/` is an independent skill with its own `SKILL.md`, references, and optional validation scripts.

## Repository layout

```text
skills/
├── agentic-iot-architect/
├── bulidics-api/
├── bulidics-water-leak-monitor/
└── agentic-iot-architect/
```

## Install for Codex

Copy the desired skill folders into `~/.codex/skills/` so that each `SKILL.md` is located directly under its skill directory:

```text
~/.codex/skills/bulidics-api/SKILL.md
~/.codex/skills/bulidics-water-leak-monitor/SKILL.md
~/.codex/skills/agentic-iot-architect/SKILL.md
```

Invoke them as `$bulidics-api`, `$bulidics-water-leak-monitor`, and `$agentic-iot-architect`. Automatic selection is also enabled for relevant requests.

## Install for Cursor

Place the desired skill folders under `~/.cursor/skills/` for global use or `.cursor/skills/` for one project. Cursor also discovers skills in Codex-compatible `~/.codex/skills/` locations.

Invoke them from Agent chat as `/bulidics-api`, `/bulidics-water-leak-monitor`, and `/agentic-iot-architect`.

## Agentic IoT Architect examples

Typical requests include:

- `この漏水監視システムをAgentic IoT化して`
- `この既存IoTはAgentic IoTのLevelいくつ？`
- `工場設備保全をAgentic IoTで企画して`
- `BUILDICSを使ったAgentic IoT構成を設計して`

The skill starts from the human decision that follows sensor data, then designs Perception, Context, Proposal, Human-in-the-loop, Actuation, Learning, Decision Logs, and a practical Level 0-4 evolution path.

## Validation

API push payload:

```bash
python skills/bulidics-api/scripts/validate_push_payload.py payload.json
```

Water-leak observation:

```bash
python skills/bulidics-water-leak-monitor/scripts/evaluate_water_leak.py record.json --previous 0
```

The scripts validate local data structure and state rules only. They do not prove that a device, BULIDICS endpoint, Dify workflow, or MCP server is reachable.

## Security

Do not commit BULIDICS `Apikey` values, Dify MCP URLs, customer endpoint credentials, or other secrets. Keep live access and secrets in the API or MCP runtime, not in skill files.

## 1NCE integration

See [integrate-1nce](skills/integrate-1nce/SKILL.md) for API references, webhook design, and read-only Python examples.

Copy `skills/integrate-1nce` to your tool's skills directory and invoke `$integrate-1nce` in Codex or `/integrate-1nce` in Cursor.

Run local checks:

```bash
python3 -m unittest discover -s skills/integrate-1nce/scripts -p 'test_*.py'
```

The references summarize official documentation checked on 2026-10-30. Account-specific API availability and live connectivity have not been tested. Keep SIM management and sensor telemetry separate; do not automatically replace documented 1NCE OS `/v1/` paths with `/v2/`.

## AiMeet UIデザイン

[aimeet-ui-design](skills/aimeet-ui-design/SKILL.md) は、AiMeetの出展者一覧・詳細ページを共通デザインで整えるスキルです。HTML/CSSの完成見本、React用カード、デザインルール、既存API・認証・多言語を保つ移植手順、画面比較の確認項目を収録しています。

`skills/aimeet-ui-design` を利用する開発環境のスキルフォルダーに配置し、次のように依頼してください。

> $aimeet-ui-design を使って、dm-summit-2026の出展者一覧を完成見本に合わせて修正してください。既存機能を維持し、ブラウザで表示と操作を確認してください。

見本は `assets/reference/index.html` と `assets/reference/exhibitor.html?slug=demo-01` です。利用環境のローカルHTTPプレビューで表示してください。掲載データはすべて架空で、本番APIへの接続やログイン・送信機能は実装先の既存機能を使用します。

スキルの構造・見本JavaScript・見本の検索/詳細遷移/お気に入りは確認済みです。React部品の型チェック・ビルド、および対象アプリでのモバイル表示は実装先で確認してください。
