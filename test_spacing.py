from lcapy import Circuit

def test_lcapy():
    cct = Circuit("""
    V1 1 0 {50}; down
    W1 1 2; right=2.0
    W2 0 0a; right=2.0
    R1 2 0a {786}; down
    W3 2 3; right=2.0
    W4 0a 0b; right=2.0
    L1 3 0b {6.79e-3}; down
    W5 3 4; right=2.0
    W6 0b 0c; right=2.0
    C1 4 0c {0.144e-3}; down
    """)
    cct.draw('test_layout.png')
    
if __name__ == '__main__':
    test_lcapy()
