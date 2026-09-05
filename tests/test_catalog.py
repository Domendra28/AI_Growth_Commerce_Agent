import pytest
from app.tools.catalog_tools import search_catalog_tool, get_product_details_tool
import json

def test_catalog_search_filters():
    res_str = search_catalog_tool(query="running", max_price=5000.0)
    data = json.loads(res_str)
    assert data["status"] == "success"
    for p in data["products"]:
        assert p["price"] <= 5000.0

def test_catalog_get_details():
    res_str = get_product_details_tool("prod_laptop_basic")
    data = json.loads(res_str)
    assert data["status"] == "success"
    assert data["product"]["name"] == "TechBook Air 14"
