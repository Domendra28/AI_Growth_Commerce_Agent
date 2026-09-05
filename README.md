# AI Growth & Agentic Commerce Agent System

An end-to-end multi-agent system built in Python leveraging **Google Agent Development Kit (ADK)**, **Universal Commerce Protocol (UCP)**, **Agent Payments Protocol (AP2)**, and **Razorpay Test Mode APIs**.

This system solves two core problems:
1. **AI Growth for Merchants**: Revenue optimization through explainable upselling, cross-selling, and campaign orchestration.
2. **Agentic Commerce**: Making merchants fully transactable by an AI buyer across standard protocol boundaries (Discovery -> Cart -> Checkout -> Authorization -> Payment Execution -> Order Confirmation -> Audit Trail).

---

## Architecture Overview

```text
                               ┌─────────────────────────┐
                               │       ROOT AGENT        │
                               │  (Root Orchestrator)    │
                               └────────────┬────────────┘
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               ▼                            ▼                            ▼
   ┌───────────────────────┐    ┌───────────────────────┐    ┌───────────────────────┐
   │    Shopping Agent     │    │     Growth Agent      │    │     Payment Agent     │
   │  (Catalog & Checkout) │    │  (Upsell & Campaigns) │    │   (Money Safety & AP2)│
   └───────────┬───────────┘    └───────────┬───────────┘    └───────────┬───────────┘
               │                            │                            │
               ▼                            ▼                            ▼
   ┌───────────────────────┐    ┌───────────────────────┐    ┌───────────────────────┐
   │   UCP Protocol Client │    │   Analytics & AOV     │    │  AP2 Protocol Client  │
   │  (Catalog, Cart, Ord) │    │   Recommendation      │    │  (Razorpay / Mock)    │
   └───────────────────────┘    └───────────────────────┘    └───────────────────────┘
```

---

## 1. Features & Safety Framework

### A. Money Safety Framework (Non-Negotiable)
- **Explainable Transactions**: Prior to any payment, the system generates a clear breakdown of item names, quantities, unit prices, merchant identity, totals, currency, and payment mechanisms.
- **Bounded Enforcement**: Rejects transactions exceeding `MAX_TRANSACTION_AMOUNT` (e.g. ₹10,000) or involving disallowed merchants/categories.
- **Gated Authorization**: Payment execution strictly requires explicit user authorization (`user_authorized=True`). Recommendations never constitute authorization.
- **Structured Audit Trail**: Audit events (`PRODUCT_SEARCHED`, `CART_CREATED`, `AUTHORIZATION_REQUESTED`, `AUTHORIZATION_GRANTED`, `PAYMENT_INITIATED`, `PAYMENT_SUCCEEDED`, `PAYMENT_FAILED`) are recorded with timestamps. Credentials/secrets are automatically redacted.

### B. Protocol Boundaries
- **UCP (Universal Commerce Protocol)**: Standardized merchant discovery, inventory check, cart management, checkout preparation, and order lifecycle management.
- **AP2 (Agent Payments Protocol)**: Standardized payment intent creation, authorization request gating, request execution, and settlement confirmation.
- **Razorpay Integration**: Seamless integration with Razorpay Test Mode APIs (`RAZORPAY_MODE=test`), with toggleable fallback to mock payment provider (`PAYMENT_PROVIDER=mock`).

---

## 2. Installation & Setup Instructions

### Environment Setup

1. **Clone & Navigate to directory:**
   ```bash
   cd ai-growth-agentic-commerce
   ```

2. **Create Python Virtual Environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment:**
   - **Windows PowerShell:**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows CMD:**
     ```cmd
     .venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables:**
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

---

## 3. Running the Demonstration

To launch the interactive CLI demonstration showcasing both merchant AI Growth and AI Buyer Agentic Commerce:

```bash
python -m app
```

### Demo Interactive Flow:
1. **AI Growth Campaign**: Merchant requests AOV boost -> Growth Agent proposes bundled discount strategy -> Merchant authorizes campaign.
2. **AI Buyer Discovery**: Buyer requests running shoes under ₹5,000 -> Shopping Agent searches UCP catalog -> Recommends `Runner Pro Shoes`.
3. **Cross-Sell Recommendation**: Growth Agent suggests sports socks.
4. **UCP Checkout**: Product added to cart and checkout order created.
5. **Gated Authorization**: Payment agent presents explainable transaction breakdown and halts for explicit user approval.
6. **AP2 Payment Execution**: Payment processed via Razorpay Test Mode / AP2 Client, confirming order and logging audit trail.

---

## 4. Running Automated Tests

Run the complete test suite using `pytest`:

```bash
pytest
```

To run individual test components:
```bash
pytest tests/test_agent.py             # Agent initialization & delegation
pytest tests/test_ucp.py               # UCP protocol flow
pytest tests/test_ap2.py               # AP2 payment protocol
pytest tests/test_payment.py           # Razorpay payment integration
pytest tests/test_growth.py            # AI Upsell & Campaign strategy
pytest tests/test_failure_handling.py # Failure recovery & safety limits
```

---

## 5. Docker Deployment

To build and run using Docker Compose:

```bash
docker-compose up --build
```
