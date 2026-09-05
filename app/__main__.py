import sys
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from app.agent import CommerceAgentSystem
from app.audit.trail import get_audit_trail
from app.config import config

console = Console()

def run_demo():
    console.print(Panel.fit(
        "[bold cyan]AI Growth & Agentic Commerce Agent System[/bold cyan]\n"
        "[dim]Powered by Google ADK, UCP, AP2 & Razorpay Test Mode[/dim]",
        style="red",
    ))

    system = CommerceAgentSystem()
    audit = get_audit_trail()
    session_id = "demo_live_session"

    console.print("\n[bold yellow]--- 1. MERCHANDISING & AI GROWTH DEMONSTRATION ---[/bold yellow]")
    console.print("Merchant requests: [italic]'Help me increase my Average Order Value (AOV) for TechStore'[/italic]")
    time.sleep(1)

    campaign_res = system.process_campaign_orchestration(
        merchant_id="TechStore",
        goal="increase_average_order_value",
        merchant_authorized=False,
        session_id=session_id
    )

    console.print("\n[bold magenta]Growth Agent Response:[/bold magenta]")
    console.print(f"Status: [bold]{campaign_res.get('status')}[/bold]")
    campaign_info = campaign_res.get("campaign", {})
    console.print(f"Proposed Strategy: {campaign_info.get('strategy')}")
    console.print(f"Expected ROI: {campaign_info.get('estimated_aov_increase')}")
    console.print(f"Action: {campaign_info.get('proposed_action')}")

    auth_campaign = Confirm.ask("\nMerchant: Authorize activation of this campaign strategy?")
    if auth_campaign:
        campaign_activated = system.process_campaign_orchestration(
            merchant_id="TechStore",
            goal="increase_average_order_value",
            merchant_authorized=True,
            session_id=session_id
        )
        console.print(f"[bold green]✔ Campaign Activated:[/bold green] {campaign_activated.get('message')}")

    console.print("\n[bold yellow]--- 2. CONVERSATIONAL SHOPPING & AI BUYER DISCOVERY ---[/bold yellow]")
    query_str = "running shoes"
    max_budget = 5000.0
    console.print(f"AI Buyer Intent: [italic]'I need running shoes under ₹{max_budget:,.0f}'[/italic]")
    
    discovery = system.process_shopping_intent(query=query_str, max_price=max_budget, session_id=session_id)
    products = discovery.get("products", [])

    table = Table(title=f"UCP Catalog Discovery ({len(products)} products found)")
    table.add_column("ID", style="dim")
    table.add_column("Product Name", style="bold green")
    table.add_column("Category")
    table.add_column("Price", justify="right")

    for p in products:
        table.add_row(p["product_id"], p["name"], p["category"], f"₹{p['price']:,.2f}")
    console.print(table)

    selected_product = products[1] if len(products) > 1 else products[0]
    console.print(f"\nShopping Agent recommends: [bold green]{selected_product['name']}[/bold green] (Best balance of price and features).")

    # Upsell / Cross-sell suggestions
    cross_sell_res = system.process_cross_sell_analysis(selected_product["product_id"], session_id=session_id)
    cross_sells = cross_sell_res.get("cross_sells", [])
    if cross_sells:
        cs_names = [cs["product"]["name"] for cs in cross_sells]
        console.print(f"Growth Agent Cross-Sell Suggestion: Add [cyan]{', '.join(cs_names)}[/cyan] to pair with your shoes.")

    buy_confirm = Confirm.ask(f"\nAI Buyer: Add [bold]{selected_product['name']}[/bold] to cart and prepare checkout?")
    if not buy_confirm:
        console.print("[yellow]Shopping session ended by user.[/yellow]")
        return

    # Cart & Checkout
    cart_res = system.process_cart_creation(
        merchant_id=selected_product["merchant_id"],
        product_id=selected_product["product_id"],
        quantity=1,
        session_id=session_id
    )
    cart_id = cart_res["cart"]["cart_id"]

    checkout_res = system.process_checkout_preparation(cart_id=cart_id, session_id=session_id)
    order_id = checkout_res["order"]["order_id"]
    order_amount = checkout_res["order"]["total_amount"]

    console.print(f"\n[bold green]✔ Checkout Order Prepared:[/bold green] Order ID [cyan]{order_id}[/cyan], Total: [bold]₹{order_amount:,.2f}[/bold]")

    console.print("\n[bold yellow]--- 3. MONEY SAFETY: EXPLAINABILITY & GATED AUTHORIZATION ---[/bold yellow]")
    
    # 1st attempt: Call payment tool WITHOUT explicit user authorization to show gating
    unauth_pay = system.process_payment_execution(order_id=order_id, user_authorized=False, session_id=session_id)
    console.print(Panel(
        f"[bold red]AUTHORIZATION GATE TEST:[/bold red]\n"
        f"{unauth_pay.get('transaction_explanation')}\n\n"
        f"[bold yellow]Agent Response:[/bold yellow] {unauth_pay.get('message')}",
        title="AP2 Explainable Transaction Breakdown"
    ))

    user_auth = Confirm.ask("\n[bold bright_white]USER AUTHORIZATION:[/bold bright_white] Do you grant permission to process this charge?")
    if not user_auth:
        console.print("[bold red]Transaction aborted: User authorization denied.[/bold red]")
        return

    console.print("\n[bold yellow]--- 4. AP2 & RAZORPAY TEST MODE PAYMENT EXECUTION ---[/bold yellow]")
    
    # Ask if user wants to simulate failure or success
    sim_fail = Confirm.ask("Simulate payment failure for testing recovery?", default=False)

    pay_res = system.process_payment_execution(
        order_id=order_id,
        user_authorized=True,
        simulate_failure=sim_fail,
        session_id=session_id
    )

    if pay_res.get("status") == "success":
        tx = pay_res["transaction"]
        console.print(Panel(
            f"[bold green]✔ PAYMENT SUCCESSFUL![/bold green]\n"
            f"Transaction ID: [cyan]{tx['transaction_id']}[/cyan]\n"
            f"Provider: {tx['provider'].upper()}\n"
            f"Amount Paid: ₹{tx['amount']:,.2f} {tx['currency']}\n"
            f"Order Status: [bold green]CONFIRMED[/bold green]",
            title="Order & Payment Confirmation"
        ))
    else:
        console.print(Panel(
            f"[bold red]✖ PAYMENT FAILED![/bold red]\n"
            f"Error: {pay_res.get('message')}\n"
            f"Safe Next Step: [yellow]{pay_res.get('safe_next_step')}[/yellow]",
            title="Payment Failure & Graceful Recovery"
        ))

    console.print("\n[bold yellow]--- 5. STRUCTURED AUDIT TRAIL SUMMARY ---[/bold yellow]")
    session_events = audit.get_session_events(session_id)
    audit_table = Table(title=f"Audit Log Events ({len(session_events)} entries recorded)")
    audit_table.add_column("Timestamp", style="dim")
    audit_table.add_column("Event Type", style="bold cyan")
    audit_table.add_column("Agent", style="magenta")
    audit_table.add_column("Tool", style="yellow")
    audit_table.add_column("Order/Tx ID", style="dim")

    for ev in session_events[-8:]:  # Show last 8 events
        audit_table.add_row(
            ev.timestamp.split("T")[1][:8],
            ev.event_type.value,
            ev.agent,
            ev.tool or "-",
            ev.order_id or ev.transaction_id or "-"
        )
    console.print(audit_table)

    console.print("\n[bold green]Demonstration Complete![/bold green]\n")

if __name__ == "__main__":
    run_demo()
