# BUILDICS連携の設計例

以下は自社実装の提案。1NCE仕様やBUILDICS既存APIを保証するものではない。

## 機器台帳

tenant_id, building_id, device_id, provider, integration_id, iccid, sensor_model, decoder_versionを紐付ける。
ICCIDだけでテナントを決めず、認証済み接続設定と台帳を照合する。ゲートウェイ配下の複数子機はpayload中の子機IDも使う。

## 保存項目

provider, integration_id, source_event_id, iccid, device_id, received_at, measured_at, measurements, raw_event, quality_statusを保存する。
単位・倍率はメーカー仕様で確認する。measured_atがなければnullにし、受信時刻で代用した場合は明記する。
RESTとWebhookに共通IDがなければ機器・測定時刻・連番等から安定キーを設計し、同時刻の別測定を消さない。
通信異常、容量低下、測定異常、解析異常を分ける。

## 取込経路

測定値はWebhook → 永続キュー → デコーダー → 時系列DBへ取り込み、必要ならHistorianのRESTで補完する。SIM管理は別ジョブにする。
1NCE OSへ送信しない機器はメーカーAPIまたは直接HTTPS/MQTT受信を選ぶ。
ZETAデータも同じモデルに正規化するが、デコードと受信認証は各通信方式に合わせる。
Agentic IoTでは設備の文脈、判断根拠、対処提案、承認条件、実行結果、誤報/実報ラベルを追加する。通信リセット等の自動操作は明示された運用範囲から始める。
