from typing import List, Dict, Set
import hashlib

class Node:
    def __init__(self, node_id: int, is_corrupt: bool = False):
        self.node_id = node_id
        self.is_corrupt = is_corrupt
        self.extracted_set: Set[int] = set()
        self.received_messages: List[Dict] = []

    def sign_message(self, message: int, signatures: List[Dict]) -> Dict:
        """
        Simulates a digital signature using SHA-256 hashing.
        Each signature includes the node_id and a hash based on message content.
        """
        content = f"{message}-{self.node_id}"
        signature = hashlib.sha256(content.encode()).hexdigest()
        return {
            "message": message,
            "signatures": signatures + [{"node_id": self.node_id, "signature": signature}]
        }

    def receive_message(self, msg: Dict):
        """Stores an incoming message for later processing."""
        self.received_messages.append(msg)

    def send_messages(self, round_number: int, total_nodes: int) -> List[Dict]:
        """
        Processes received messages and sends new ones if valid.
        A message is forwarded only if it has exactly 'round_number' signatures
        and includes a valid signature from the sender (node 0).
        """
        new_messages = []
        for msg in self.received_messages:
            message, signatures = msg["message"], msg["signatures"]
            if len(signatures) != round_number:
                continue
            if not any(s["node_id"] == 0 for s in signatures):
                continue  # Sender (node 0) signature missing
            if message not in self.extracted_set:
                self.extracted_set.add(message)
                new_msg = self.sign_message(message, signatures)
                new_messages.append(new_msg)
        return new_messages

def simulate_consensus(n: int, f: int, sender_input: int, corrupt_nodes: List[int]) -> List[int]:
    """
    Simulates the Dolev-Strong consensus protocol with f Byzantine faults.

    Args:
        n (int): Total number of nodes.
        f (int): Number of tolerated Byzantine nodes.
        sender_input (int): Initial message (bit) proposed by sender (node 0).
        corrupt_nodes (List[int]): IDs of corrupt nodes.

    Returns:
        List[int]: Output values decided by each honest node.
    """
    nodes = [Node(i, is_corrupt=(i in corrupt_nodes)) for i in range(n)]
    sender = nodes[0]

    # Round 0: Sender sends the initial message
    init_msg = sender.sign_message(sender_input, [])
    for node in nodes:
        node.receive_message(init_msg)

    # Rounds 1 to f+1
    for round_number in range(1, f + 2):
        all_messages = []
        for node in nodes:
            if not node.is_corrupt:
                msgs = node.send_messages(round_number, n)
                all_messages.extend(msgs)
        for node in nodes:
            for msg in all_messages:
                node.receive_message(msg)

    # Final decision: each honest node outputs the unique extracted value, or 0 if undecided
    outputs = []
    for node in nodes:
        if not node.is_corrupt:
            if len(node.extracted_set) == 1:
                outputs.append(next(iter(node.extracted_set)))
            else:
                outputs.append(0)
    return outputs
