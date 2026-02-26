from lcapy import Circuit

def test_bridge():
    cct = Circuit(f"""
    Vac 1 0 ac; down
    
    D1 4 2; down
    D2 2 5; down
    
    W3 4 4a; right, size=2
    W4 5 5a; right, size=2
    
    D3 4a 3; down
    D4 3 5a; down
    
    # Connecting the source to the bridge
    W1 1 2
    W2 0 3
    
    W5 4a 8; right, size=2
    W6 5a 9; right, size=2
    C1 8 9; down
    """)
    cct.draw('test_bridge.png')
    
def test_bjt():
    cct = Circuit(f"""
    Vac in inGND ac; down
    W1 in inC; right, size=1.5
    W2 inGND bGND; right, size=1.5
    
    C1 inC B; right, size=1.5
    W3 bGND bGND2; right, size=1.5
    
    R2 B bGND2; down
    W4 B qb; right, size=1.5
    W5 bGND2 bGND3; right, size=1.5
    
    V1 PVcc VccGND; down
    W6 PVcc Vcc2; right, size=1.5
    W7 VccGND bGND3; right, size=1.5
    
    R1 Vcc2 qb; down
    Q1 qc qb qe npn; right, size=1.5
    """)
    try:
        cct.draw('test_bjt.png')
    except Exception as e:
        print("BJT FAIL:", e)

if __name__ == '__main__':
    test_bridge()
    test_bjt()
