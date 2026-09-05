import pytest
from app.agent import CommerceAgentSystem
from app.agents.root_agent import create_root_agent
from app.agents.shopping_agent import create_shopping_agent
from app.agents.growth_agent import create_growth_agent
from app.agents.payment_agent import create_payment_agent

def test_agent_initialization():
    system = CommerceAgentSystem()
    assert system.root_agent.name == "root_agent"
    assert system.shopping_agent.name == "shopping_agent"
    assert system.growth_agent.name == "growth_agent"
    assert system.payment_agent.name == "payment_agent"

def test_agent_delegation_flow():
    system = CommerceAgentSystem()
    # Test shopping discovery
    res = system.process_shopping_intent(query="TechBook")
    assert res["status"] == "success"
    assert res["count"] > 0

    # Test growth analysis
    product_id = res["products"][0]["product_id"]
    upsell_res = system.process_upsell_analysis(product_id)
    assert upsell_res["status"] == "success"
