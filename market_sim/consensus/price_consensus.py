from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, timedelta
import numpy as np
from dolev_strong import Node, simulate_consensus
from core.models.base import Trade
from core.utils.time_utils import utc_now

class PriceConsensusNode(Node):
    def __init__(self, node_id: int, is_corrupt: bool = False):
        super().__init__(node_id, is_corrupt)
        self.price_history: Dict[str, List[float]] = {}  # symbol -> list of prices
        self.last_consensus_time: Dict[str, datetime] = {}  # symbol -> last consensus time
        self.consensus_results: Dict[str, Dict] = {}  # symbol -> {timestamp, value}
    
    def add_price(self, symbol: str, price: float, timestamp: datetime):
        """Add a price observation to the node's history."""
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        self.price_history[symbol].append(price)
    
    def compute_price_estimate(self, symbol: str) -> Optional[int]:
        """
        Compute price estimate using statistical analysis.
        Returns price in cents (integer) to work with Dolev-Strong protocol.
        """
        if symbol not in self.price_history or not self.price_history[symbol]:
            return None
            
        prices = self.price_history[symbol]
        # Compute mean of normal distribution
        mean_price = np.mean(prices)
        # Convert to cents for integer consensus
        return int(mean_price * 100)

class NetworkPriceConsensus:
    def __init__(self, num_nodes: int, fault_tolerance: int, 
                 consensus_interval: timedelta = timedelta(days=7)):
        self.nodes = [PriceConsensusNode(i) for i in range(num_nodes)]
        self.num_nodes = num_nodes
        self.fault_tolerance = fault_tolerance
        self.consensus_interval = consensus_interval
        self.corrupt_nodes: List[int] = []
    
    def add_trade(self, trade: Trade, timestamp: datetime):
        """Add a trade observation to all nodes."""
        price = float(trade.price)
        for node in self.nodes:
            if not node.is_corrupt:
                node.add_price(trade.symbol, price, timestamp)
    
    def should_run_consensus(self, symbol: str, current_time: datetime) -> bool:
        """Check if consensus should be run for a symbol."""
        last_consensus = self.nodes[0].last_consensus_time.get(symbol)
        if not last_consensus:
            return True
        return current_time - last_consensus >= self.consensus_interval
    
    def run_consensus(self, symbol: str, current_time: datetime) -> Optional[Decimal]:
        """
        Run consensus protocol for a symbol's price.
        Returns the consensus price if successful.
        """
        # Get price estimate from sender (node 0)
        sender_estimate = self.nodes[0].compute_price_estimate(symbol)
        if sender_estimate is None:
            return None
            
        # Run Dolev-Strong consensus
        consensus_results = simulate_consensus(
            n=self.num_nodes,
            f=self.fault_tolerance,
            sender_input=sender_estimate,
            corrupt_nodes=self.corrupt_nodes
        )
        
        # Record consensus results
        consensus_value = None
        if consensus_results and all(r == consensus_results[0] for r in consensus_results):
            consensus_value = Decimal(consensus_results[0]) / 100  # Convert back to decimal
            consensus_result = {
                'timestamp': current_time,
                'value': consensus_value
            }
            for node in self.nodes:
                if not node.is_corrupt:
                    node.consensus_results[symbol] = consensus_result
                    node.last_consensus_time[symbol] = current_time
                    # Clear price history after consensus
                    node.price_history[symbol] = []
        
        return consensus_value

def create_price_consensus_network(
    num_nodes: int = 5,
    fault_tolerance: int = 1,
    consensus_interval: timedelta = timedelta(days=7)
) -> NetworkPriceConsensus:
    """Create a new price consensus network."""
    return NetworkPriceConsensus(
        num_nodes=num_nodes,
        fault_tolerance=fault_tolerance,
        consensus_interval=consensus_interval
    ) 