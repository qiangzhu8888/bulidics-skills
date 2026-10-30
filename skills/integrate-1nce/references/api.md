# API仕様と確認境界

確認日: 2026-10-30。公開資料確認のみ。実アカウント接続未実施。

## 認証

ベースURL: `https://api.1nce.com/management-api`。
`POST /oauth/token`へHTTP BasicでClient ID/Secretを渡し、JSON bodyを`{"grant_type":"client_credentials"}`にする。返却のaccess_tokenを各APIのBearer認証に使う。期限を固定値で保証しない。
Platform 2.0はAccount → Management API Accessで専用資格情報を発行する。Ownerのログイン情報をAPIに使わない。

公式資料:
- https://help.1nce.com/platform-migration/feature-changes/portal-and-api-access/
- https://help.1nce.com/dev-hub/reference/postaccesstokenpost

## SIM管理v2

| 用途 | メソッドと相対パス |
|---|---|
| 一覧 | GET `/v2/sims` |
| 詳細／変更 | GET / PUT `/v2/sims/{iccid}` |
| 接続状態 | GET `/v2/sims/{iccid}/status` |
| 接続リセット | POST `/v2/sims/{iccid}/reset` |
| イベント | GET `/v2/sims/{iccid}/events` |
| データ容量 | GET `/v2/sims/{iccid}/quota/data` |
| SMS容量 | GET `/v2/sims/{iccid}/quota/sms` |
| SMS一覧／送信 | GET / POST `/v2/sims/{iccid}/sms` |
| 容量追加 | POST `/v2/sims/{iccid}/topup` |

レスポンスの詳細フィールドと変更bodyは現行OpenAPIで確認する。v1のレスポンスをv2へ流用しない。容量APIは値の単位・総枠か残量かを確認してから画面表示する。

公式資料:
- https://help.1nce.com/platform-migration/api-migration/
- https://help.1nce.com/api/v2/sim-management/get-sim-using-get/
- https://help.1nce.com/api/v2/sim-management/get-data-quota-for-sim-using-get/

## 測定値のREST取得

対象は1NCE OSが受信したデータ。SIM管理APIやData Streamerの通信量レコードから温度等を得られると説明しない。

公式Historian例:
```http
GET /v1/inspect/devices/history?iccid=...&pageSize=25
Authorization: Bearer <token>
```
期間指定はstartDateTime/endDateTime。ICCIDは文字列。ISO時刻の+等をURLエンコードする。
items配列にtime、payload、iccid、deviceId、protocolを含む。payloadはJSON文字列またはBase64の場合があり、Webhookのpayloadオブジェクト形式と混同しない。
例のページサイズは既定10、1～25。続きはnextToken。資料のページング例に異なるパスも混在するため、API Explorerで同じhistoryパスのパラメーターを照合する。
無指定例は直近7日間を検索する。これを保持期間保証と解釈しない。保持期間・最大検索範囲は別途確認し、自社で長期保存する。
Platform v2の資料にもこの/v1/例が残る。利用可否・移行予定を実装前に確認する。

公式資料:
- https://help.1nce.com/docs/v2/1nce-os/1nce-os-device-inspector/device-inspector-historian-api/
- https://help.1nce.com/api/

## 上限と移行

SIM管理v1は移行資料で2026年末廃止予定。新規SIM管理はv2を基準とする。旧usage、一括・自動top-up等の代替は確認が必要。
標準10 TPSが案内されるが、上限変更可否は移行資料とRate Limits資料に不一致がある。認証等の個別上限も確認し、429・Retry-Afterに対応する。
SIMイベント・通信量の大量監視はData Streamer、測定値配信はCloud Integratorと使い分ける。

公式資料:
- https://help.1nce.com/api/api-rate-limits/
- https://help.1nce.com/platform-migration/api-migration/
- https://help.1nce.com/docs/v2/connectivity-services/connectivity-services-data-services/data-services-data-monitoring/

## 同梱クライアントの使用例

Skillディレクトリで実行する。Client ID/Secretは環境変数に安全に設定済みとし、コマンドへ直接書かない。

```bash
python3 scripts/read_1nce.py quota --iccid "$ICCID"
python3 scripts/read_1nce.py history --iccid "$ICCID" --allow-documented-os-v1 --start '2026-10-30T00:00:00Z' --end '2026-10-30T01:00:00Z'
python3 scripts/normalize_event.py < event.json
```

`--allow-documented-os-v1`は契約で利用可能と確認した後に指定する。サンプルはAPI成功を保証せず、実行時に実サービスへアクセスする。読み取り結果は端末へ表示するため、共有環境では識別子を保護する。自動再試行・トークンキャッシュ・全ページ走査は実装していない。本番ジョブには適切な再試行とチェックポイントを追加する。
