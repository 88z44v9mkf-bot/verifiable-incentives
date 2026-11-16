# Getting a Stripe test key (2 minutes)

We cannot create a Stripe account or a key on your behalf: signup requires your
email, phone verification, and acceptance of Stripe's terms. A test key is free
and does not require a business or a bank account in most regions.

1. Go to https://dashboard.stripe.com/register and create an account with your
   email. Verify the email and, if asked, the phone number.
2. In the Dashboard, make sure the **Test mode** toggle (top right) is ON.
3. Open **Developers → API keys** (or https://dashboard.stripe.com/test/apikeys).
4. Copy the **Secret key** that starts with `sk_test_`. Do not copy the
   publishable key; the sandbox needs the secret key.
5. Store it in the environment, never in a file or in git:
   ```
   export STRIPE_SECRET_KEY=sk_test_...
   ```
6. Run the integration check (no real money):
   ```
   cd experiments/payments
   python3 live_run.py --test-mode --tasks 2 --max-spend 20
   ```

Test mode charges are simulated by Stripe; they never move real money. The
sandbox's `StripeBackend` uses `pm_card_visa`, a Stripe test payment method.

## If Stripe is not available in your region

The same interface can be implemented with a domestic provider, but each
requires a merchant/sandbox account issued to the account holder:

- **Alipay sandbox**: app id, RSA2 key pair, sandbox buyer account. An adapter
  skeleton is in `providers/alipay_sandbox.py`; settlement polling is not yet
  implemented.
- **WeChat Pay**: merchant id, API v3 key, certificate serial and private key.
  The old sandbox has been retired; a test merchant environment is required.
- **Aggregators** (Ping++, UnionPay, etc.): a test merchant account with a
  create-charge / query / refund API.

To add a provider, implement the `charge(amount, currency, description,
idempotency_key, merchant)` method used by `backend.py` and return a
`ChargeResult`. The ledger and the sandbox environment are provider-agnostic.

## Security notes

- Never paste a secret key into a chat, an issue, or a repository. If a key was
  exposed, roll it in the Stripe Dashboard immediately.
- Use a separate restricted key with write access only to PaymentIntents for
  experiments, and set a low monthly cap in the Dashboard.
- The sandbox stores only charge ids and amounts; card data stays with Stripe.
- For live mode, use a dedicated account with a hard spend limit and reconcile
  the ledger against the Dashboard after every run.
