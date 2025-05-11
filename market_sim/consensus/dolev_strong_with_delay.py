from typing import List, Dict, Set
import hashlib
import time

class Node:
    def __init__(self, node_id: int, is_corrupt: bool = False):
        self.node_id = node_id
        self.is_corrupt = is_corrupt
        self.extracted_set: Set[int] = set()
        self.received_messages: List[Dict] = []

    def sign_message(self, message: int, signatures: List[Dict]) -> Dict:
        """Simulates digital signing using SHA-256."""
        content = f"{message}-{self.node_id}"
        signature = hashlib.sha256(content.encode()).hexdigest()
        return {
            "message": message,
            "signatures": signatures + [{"node_id": self.node_id, "signature": signature}]
        }

    def receive_message(self, msg: Dict):
        """Receives and stores a message."""
        self.received_messages.append(msg)

    def send_messages(self, round_number: int) -> List[Dict]:
        """Processes messages and sends new ones if valid."""
        new_messages = []
        for msg in self.received_messages:
            message, signatures = msg["message"], msg["signatures"]
            if len(signatures) != round_number:
                continue
            if not any(s["node_id"] == 0 for s in signatures):
                continue
            if message not in self.extracted_set:
                self.extracted_set.add(message)
                new_msg = self.sign_message(message, signatures)
                new_messages.append(new_msg)
        return new_messages


def simulate_consensus_with_delay(n: int, f: int, sender_input: int, corrupt_nodes: List[int], delta_ms: int = 0) -> List[int]:
    """
    Simulates Dolev-Strong consensus with simulated network delay (∆).

    Args:
        n (int): Total nodes.
        f (int): Byzantine fault tolerance.
        sender_input (int): Proposed message.
        corrupt_nodes (List[int]): IDs of corrupt nodes.
        delta_ms (int): Simulated network delay in milliseconds.

    Returns:
        List[int]: Decisions of honest nodes.
    """
    nodes = [Node(i, is_corrupt=(i in corrupt_nodes)) for i in range(n)]
    sender = nodes[0]

    # Round 0 — sender sends initial message
    init_msg = sender.sign_message(sender_input, [])
    for node in nodes:
        time.sleep(delta_ms / 1000.0)
        node.receive_message(init_msg)

    # Rounds 1 to f + 1
    for round_number in range(1, f + 2):
        all_messages = []
        for node in nodes:
            if not node.is_corrupt:
                new_msgs = node.send_messages(round_number)
                all_messages.extend(new_msgs)

        # Simulate message delivery delay
        for node in nodes:
            for msg in all_messages:
                time.sleep(delta_ms / 1000.0)
                node.receive_message(msg)

    # Final decision by honest nodes
    outputs = []
    for node in nodes:
        if not node.is_corrupt:
            if len(node.extracted_set) == 1:
                outputs.append(next(iter(node.extracted_set)))
            else:
                outputs.append(0)
    return outputs
