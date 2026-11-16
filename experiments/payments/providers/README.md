# Domestic payment providers

Stripe is the reference implementation because it offers a test mode without a
merchant account. Domestic providers require a merchant/sandbox account and
credentials issued to the account holder; they cannot be created on the user's
behalf.

## Alipay sandbox (implemented, untested without credentials)

1. Open the Alipay Open Platform sandbox console and create a sandbox app.
2. Generate an RSA2 key pair (2048-bit). Keep the private key on the research
   machine; upload the public key to the console.
3. Set:
   ```
   export ALIPAY_APP_ID=...
   export ALIPAY_PRIVATE_KEY="$(cat app_private_key.pem | base64 -w0)"   # or PEM
   export ALIPAY_GATEWAY=https://openapi-sandbox.dl.alipaydev.com/gateway.do
   ```
4. The adapter uses `alipay.trade.precreate` and returns a QR code; the charge
   is pending until the sandbox buyer pays. Settlement must be confirmed by
   polling `alipay.trade.query` (not yet implemented).
5. Buyer-side sandbox credentials are also required to complete a payment; the
   sandbox provides a buyer account for this.

## WeChat Pay

WeChat Pay v3 sandbox has been retired; use the merchant platform's test
environment with `mchid`, API v3 key, merchant certificate serial number and
private key. Integration requires signed HTTP requests and certificate
management. This is a larger adapter and is not implemented here.

## UnionPay / Ping++ / other aggregators

Most aggregators expose a test merchant account. The sandbox only needs a
provider that can (a) create a charge with an idempotency key, (b) report
settlement, and (c) refund. The `backend.py` interface (`charge`) is the only
integration point; add an adapter that satisfies it.

## What we can and cannot do

We can implement and test adapters against local mocks (done for Stripe:
`mock_stripe_server.py` + `integration_test.py`). We cannot create a Stripe,
Alipay, or WeChat merchant account, generate credentials for it, or use
credentials that belong to a third party. Account creation requires identity,
phone/email verification, and acceptance of the provider's terms by the account
holder.
