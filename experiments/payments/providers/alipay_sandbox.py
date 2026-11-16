"""Alipay sandbox adapter (RSA2, precreate/QR flow).

Status: experimental; requires sandbox credentials from the Alipay Open
Platform. It has NOT been run against the sandbox gateway in this repository.
The adapter signs requests with openssl and calls `alipay.trade.precreate`,
which returns a QR code; the charge is pending until the buyer pays.

Required environment:
  ALIPAY_APP_ID
  ALIPAY_PRIVATE_KEY   (PKCS8 base64 or PEM)
  ALIPAY_PUBLIC_KEY    (optional, for response verification)
  ALIPAY_GATEWAY       (default sandbox gateway)
"""
from __future__ import annotations

import base64, json, os, subprocess, tempfile, time, urllib.parse, urllib.request
from dataclasses import dataclass

DEFAULT_GATEWAY = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"


@dataclass
class ChargeResult:
    ok: bool
    charge_id: str
    amount: float
    currency: str
    mode: str
    error: str = ""
    qr_code: str = ""


class AlipaySandboxBackend:
    def __init__(self, app_id: str, private_key: str, public_key: str = "",
                 gateway: str = DEFAULT_GATEWAY):
        if not app_id or not private_key:
            raise ValueError("ALIPAY_APP_ID and ALIPAY_PRIVATE_KEY are required")
        self.app_id = app_id
        self.private_key = private_key
        self.public_key = public_key
        self.gateway = gateway

    def _pem(self) -> str:
        k = self.private_key.strip()
        if "BEGIN" in k:
            return k
        body = "\n".join(k[i:i + 64] for i in range(0, len(k), 64))
        return f"-----BEGIN PRIVATE KEY-----\n{body}\n-----END PRIVATE KEY-----\n"

    def _sign(self, content: str) -> str:
        with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f:
            f.write(self._pem())
            path = f.name
        try:
            proc = subprocess.run(["openssl", "dgst", "-sha256", "-sign", path],
                                  input=content.encode(), capture_output=True, check=True)
            return base64.b64encode(proc.stdout).decode()
        finally:
            os.unlink(path)

    def _request(self, method: str, biz: dict) -> dict:
        params = {
            "app_id": self.app_id,
            "method": method,
            "format": "JSON",
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": json.dumps(biz, ensure_ascii=False, separators=(",", ":")),
        }
        content = "&".join(f"{k}={params[k]}" for k in sorted(params) if params[k] != "")
        params["sign"] = self._sign(content)
        body = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(self.gateway, data=body, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())

    def charge(self, amount: float, currency: str, description: str, idempotency_key: str, merchant: str):
        biz = {
            "out_trade_no": idempotency_key[:32],
            "total_amount": f"{amount:.2f}",
            "subject": description[:100],
            "timeout_express": "5m",
        }
        try:
            res = self._request("alipay.trade.precreate", biz)
        except Exception as exc:
            return ChargeResult(False, "", amount, "cny", "alipay-sandbox", str(exc))
        payload = res.get("alipay_trade_precreate_response", {})
        ok = payload.get("code") == "10000" and bool(payload.get("qr_code"))
        return ChargeResult(ok, biz["out_trade_no"], amount, "cny", "alipay-sandbox-pending",
                            "" if ok else str(payload.get("sub_msg") or payload.get("msg")),
                            payload.get("qr_code", ""))
