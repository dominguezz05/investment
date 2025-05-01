import pytest
from dolev_strong import simulate_consensus

def test_all_honest():
    result = simulate_consensus(n=5, f=1, sender_input=1, corrupt_nodes=[])
    print(result)
    assert all(r == 1 for r in result)

def test_one_corrupt_sender():
    result = simulate_consensus(n=5, f=1, sender_input=1, corrupt_nodes=[0])
    print(result)
    # May be disagreement, but honest nodes should return either 1 or 0 consistently
    assert all(r in [0, 1] for r in result)

def test_majority_agree():
    result = simulate_consensus(n=7, f=2, sender_input=1, corrupt_nodes=[2, 5])
    print(result)
    assert all(r in [0, 1] for r in result)

def test_validity():
    result = simulate_consensus(n=6, f=2, sender_input=0, corrupt_nodes=[3, 4])
    print(result)
    assert 0 in result

# Additional pytest-specific tests that showcase pytest features

@pytest.mark.parametrize("n,f,sender_input,corrupt_nodes,expected", [
    (5, 1, 1, [], [1, 1, 1, 1, 1]),  # All honest
    (4, 1, 0, [2], [0, 0, 0]),       # One corrupt
    (3, 1, 1, [0], [0, 0])           # Corrupt sender
])
def test_consensus_scenarios(n, f, sender_input, corrupt_nodes, expected):
    result = simulate_consensus(n=n, f=f, sender_input=sender_input, corrupt_nodes=corrupt_nodes)
    # Check length matches expected (excluding corrupt nodes)
    assert len(result) == len(expected)
    # Check values match expected
    assert all(r == e for r, e in zip(result, expected))

@pytest.fixture
def basic_network():
    return {
        'n': 5,
        'f': 1,
        'sender_input': 1,
        'corrupt_nodes': []
    }

def test_with_fixture(basic_network):
    result = simulate_consensus(
        n=basic_network['n'],
        f=basic_network['f'],
        sender_input=basic_network['sender_input'],
        corrupt_nodes=basic_network['corrupt_nodes']
    )
    assert len(result) == basic_network['n']
    assert all(r == basic_network['sender_input'] for r in result) 