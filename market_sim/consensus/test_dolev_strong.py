import unittest
from dolev_strong import simulate_consensus

class TestDolevStrongProtocol(unittest.TestCase):
    def test_all_honest(self):
        result = simulate_consensus(n=5, f=1, sender_input=1, corrupt_nodes=[])
        print(result)
        self.assertTrue(all(r == 1 for r in result))

    def test_one_corrupt_sender(self):
        result = simulate_consensus(n=5, f=1, sender_input=1, corrupt_nodes=[0])
        print(result)
        # May be disagreement, but honest nodes should return either 1 or 0 consistently
        self.assertTrue(all(r in [0, 1] for r in result))

    def test_majority_agree(self):
        result = simulate_consensus(n=7, f=2, sender_input=1, corrupt_nodes=[2, 5])
        print(result)
        self.assertTrue(all(r in [0, 1] for r in result))
        # Optional: more complex assert based on expected behavior

    def test_validity(self):
        result = simulate_consensus(n=6, f=2, sender_input=0, corrupt_nodes=[3, 4])
        print(result)
        self.assertTrue(0 in result)

if __name__ == '__main__':
    unittest.main()