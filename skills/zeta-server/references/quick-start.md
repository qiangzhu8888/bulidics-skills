# 5分で理解する ZETA SERVER

1. ZETA端末が上行イベントを送信。
2. ZETA SERVERからHTTP APIで認証、またはMQTTでイベントを購読。
3. `dataDetail` のJSON文字列を解析して温度や警報状態などを取り出す。
4. BUILDICSのデバイスID・ポイントIDに紐付ける。
5. Agentic IoTが「状態→判断→提案」を行う。

## 最小実行例（通信なし）
```bash
python scripts/zeta_helper.py decode --json '{"deviceId":"00000001","dataDetail":"{\"dataStatus\":\"warning\",\"temperature\":{\"name\":\"温度\",\"unit\":\"℃\",\"value\":\"35.2\"}}"}'
```

本例はJSON形式のデコード確認用であり、実際のZETAデバイスがこの内容を送ることを保証しない。