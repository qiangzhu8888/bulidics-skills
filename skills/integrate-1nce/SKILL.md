---
name: integrate-1nce
description: Develop and troubleshoot 1NCE IoT integrations with BUILDICS or custom backends. Use for OAuth authentication, SIM management REST APIs, sensor telemetry retrieval with Device Inspector Historian, Cloud Integrator webhooks, payload decoding, or Platform v1/v2 migration. Explain in Japanese and distinguish connectivity metadata from sensor measurements with explicit verification status.
---

# 1NCE開発・BUILDICS連携

## 取得対象と送信先を判別する

1. SIM情報・通信量と、温度・漏水などの測定値を分ける。
2. 測定値の場合は機器の送信先を確認する。1NCE SIMを搭載しただけでは測定値は1NCE OSに保存されない。メーカーのクラウドへ送る機器にはそのAPIを使う。1NCE OSに送信済みならHistorianまたはCloud Integratorを使う。
3. 既存設定・コードから契約プラットフォーム、リージョン、機器型番、プロトコル、ICCID対応関係を確認する。不明な項目だけ質問し、独立して進められるサンプル作成を進める。
4. [API仕様](references/api.md)、[Webhook仕様](references/webhook.md)、[BUILDICS設計](references/buildics.md)から必要な資料を読む。

## 仕様の確度を明記する

- 同梱資料は2026-10-30に公式公開ページを確認した要約であり、契約アカウントへの実接続検証ではない。
- 実装時に現行API Explorer/OpenAPIと契約アカウントの動作を照合し、参照URLと確認日を記録する。資料を取得できない場合は最新確認済みと表現しない。
- Platform v2の資料にも1NCE OSの`/v1/inspect/...`や`/v1/integrate/...`例が残る。SIM管理v2と混同せず、OSのパスを勝手に`/v2/`へ置換しない。
- v1廃止の対象範囲、Historian保持期間、契約別上限、リージョン別送信元IPを未確認のまま断定しない。資料の矛盾は隠さない。

## 認証と接続を準備する

- API資格情報とWebhook受信用キーを分離する。環境変数やシークレット管理を使い、画面・ログ・ソース・Skillへ実キーを保存しない。Client Secretをブラウザー側で扱わない。
- `ONE_NCE_CLIENT_ID`、`ONE_NCE_CLIENT_SECRET`からOAuth Bearer tokenを取得し、返却された期限に沿って再取得する。未確認の期限を固定しない。
- 読み取り接続を依頼範囲内で進める。課金・停止・SMS送信・通信リセット・Webhook作成等の変更操作は、ユーザーの依頼範囲に入っていることを確認する。開発準備だけの依頼で本番設定を変更しない。
- 読み取り専用サンプルを`python3 scripts/read_1nce.py --help`で確認する。標準出力には取得データが出るため、共有時にはICCID等をマスキングする。

## 測定値を取り込む

- RESTではHistorianの期間指定・ページングを照合して差分取得と再開位置を実装する。同梱スクリプトは単一ページのみ。単一ページで全件取得済みとしない。
- WebhookではHTTPS POST、受信認証、永続化または永続キュー登録、2xx応答、非同期解析を実装する。
- `TEST_MESSAGE`を測定値と分けて扱い、テスト疎通だけで実機連携完了としない。
- 元のイベントとpayloadを保存する。Base64をデコードした後はメーカー仕様で測定値へ変換する。デコードだけで温度等に変換できるとは説明しない。
- `scripts/normalize_event.py`を純粋な変換例として使う。このスクリプトはHTTPサーバー、認証、永続化、メーカー固有デコーダーを提供しない。
- ZETAとの統合が必要なら利用可能なzeta-server Skillを併用し、各取込処理を共通BUILDICSデータモデルへ正規化する。

## 検証して引き渡す

- `python3 -m unittest discover -s scripts -p 'test_*.py'`でローカル処理を検証する。
- 実装した受信APIでは認証不正、JSON不正、テスト、実測定値、Base64、再送重複、永続化失敗を検証する。永続化失敗時に成功応答を返さない。
- 実接続の有無、未確認事項、実行方法を日本語で報告する。Skillの導入だけで機器の接続が有効になったとは伝えない。
