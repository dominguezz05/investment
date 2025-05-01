import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from core.models.base import Trade
from core.utils.time_utils import utc_now
from price_consensus import create_price_consensus_network
from uuid import uuid4

def create_test_trade(symbol: str, price: Decimal) -> Trade:
    """Create a test trade object."""
    return Trade(
        id=uuid4(),
        symbol=symbol,
        price=price,
        quantity=Decimal('100'),
        buyer_order_id=uuid4(),
        seller_order_id=uuid4(),
        timestamp=utc_now()
    )

def test_price_consensus_basic():
    # Create network with 5 nodes, tolerating 1 fault
    network = create_price_consensus_network(num_nodes=5, fault_tolerance=1)
    symbol = "AAPL"
    start_time = utc_now()
    
    # Add some trades
    prices = [Decimal('150.00'), Decimal('151.00'), Decimal('149.50'), 
              Decimal('150.50'), Decimal('150.25')]
    
    for price in prices:
        trade = create_test_trade(symbol, price)
        network.add_trade(trade, start_time)
    
    # Run consensus
    consensus_price = network.run_consensus(symbol, start_time)
    
    # Verify consensus
    assert consensus_price is not None
    expected_mean = sum(float(p) for p in prices) / len(prices)
    assert abs(float(consensus_price) - expected_mean) < 0.1

def test_price_consensus_with_corrupt_nodes():
    network = create_price_consensus_network(num_nodes=7, fault_tolerance=2)
    network.corrupt_nodes = [2, 5]  # Mark nodes 2 and 5 as corrupt
    symbol = "MSFT"
    start_time = utc_now()
    
    # Add trades
    prices = [Decimal('250.00'), Decimal('251.00'), Decimal('249.50'),
              Decimal('250.50'), Decimal('250.25')]
    
    for price in prices:
        trade = create_test_trade(symbol, price)
        network.add_trade(trade, start_time)
    
    # Run consensus
    consensus_price = network.run_consensus(symbol, start_time)
    
    # Verify consensus
    assert consensus_price is not None
    # Consensus should still work despite corrupt nodes
    expected_mean = sum(float(p) for p in prices) / len(prices)
    assert abs(float(consensus_price) - expected_mean) < 0.1

def test_consensus_interval():
    network = create_price_consensus_network(
        num_nodes=5,
        fault_tolerance=1,
        consensus_interval=timedelta(days=7)
    )
    symbol = "GOOGL"
    start_time = utc_now()
    
    # Add initial trades and run consensus
    trade = create_test_trade(symbol, Decimal('2800.00'))
    network.add_trade(trade, start_time)
    network.run_consensus(symbol, start_time)
    
    # Try running consensus before interval
    early_time = start_time + timedelta(days=3)
    assert not network.should_run_consensus(symbol, early_time)
    
    # Try running consensus after interval
    later_time = start_time + timedelta(days=8)
    assert network.should_run_consensus(symbol, later_time) 