from typing import List, Dict, Set
import random

class Node:
    def __init__(self, node_id: int, is_corrupt: bool = False):
        self.node_id = node_id
        self.is_corrupt = is_corrupt
        self.extracted_set: Set[int] = set()
        self.received_messages: List[Dict] = []

    def sign_message(self, message: int, signatures: List[int]) -> Dict:
        return {
            "message": message,
            "signatures": signatures + [self.node_id]
        }

    def receive_message(self, msg: Dict):
        self.received_messages.append(msg)

    def send_messages(self, round_number: int, total_nodes: int) -> List[Dict]:
        new_messages = []
        for msg in self.received_messages:
            message, signatures = msg["message"], msg["signatures"]
            if len(signatures) != round_number:
                continue
            if 1 not in signatures:
                continue  # Sender signature missing
            if message not in self.extracted_set:
                self.extracted_set.add(message)
                new_msg = self.sign_message(message, signatures)
                new_messages.append(new_msg)
        return new_messages

def simulate_consensus(n: int, f: int, sender_input: int, corrupt_nodes: List[int]) -> List[int]:
    nodes = [Node(i, is_corrupt=(i in corrupt_nodes)) for i in range(n)]
    sender = nodes[0]

    # Round 0: Sender sends initial message
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

    # Final output
    outputs = []
    for node in nodes:
        if not node.is_corrupt:
            if len(node.extracted_set) == 1:
                outputs.append(next(iter(node.extracted_set)))
            else:
                outputs.append(0)
    return outputs
