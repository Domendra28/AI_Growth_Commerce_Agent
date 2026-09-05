import pytest
import json
from app.tools.growth_tools import analyze_upsell_tool, analyze_cross_sell_tool, orchestrate_campaign_tool

def test_growth_upsell_and_cross_sell():
    upsell_res = json.loads(analyze_upsell_tool("prod_laptop_basic"))
    assert upsell_res["status"] == "success"
    assert len(upsell_res["upsells"]) > 0

    cross_sell_res = json.loads(analyze_cross_sell_tool("prod_laptop_basic"))
    assert cross_sell_res["status"] == "success"
    assert len(cross_sell_res["cross_sells"]) > 0

def test_campaign_orchestration_authorization_gate():
    pending_res = json.loads(orchestrate_campaign_tool("TechStore", merchant_authorized=False))
    assert pending_res["status"] == "pending_authorization"

    active_res = json.loads(orchestrate_campaign_tool("TechStore", merchant_authorized=True))
    assert active_res["status"] == "active"
