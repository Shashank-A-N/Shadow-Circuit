from lcapy import Circuit

def test():
    # Diode Bridge
    c1 = Circuit("""
    V1 1 0 {12}; down
    W 1 2; right
    D1 2 3; right+down
    D2 0 3; right+up
    D3 4 2; right+up
    D4 4 0; right+down
    R1 3 4; down
    """)
    c1.draw('test_diode.png')

    # Op-Amp
    c2 = Circuit("""
    Vi 1 0 {1}; down
    R1 1 2 {10k}; right
    Rf 2 3 {100k}; right
    E1 3 0 0 2 opamp
    """)
    try:
        c2.draw('test_opamp.png')
    except Exception as e:
        print("Opamp E1 error:", e)

    c2_alt = Circuit("""
    Vi 1 0 {1}; down
    R1 1 2 {10k}; right
    Rf 2 3 {100k}; right
    O1 3 0 2 opamp; right
    """)
    try:
        c2_alt.draw('test_opamp_alt.png')
    except Exception as e:
        print("Opamp O1 error:", e)

    # MOSFET
    c3 = Circuit("""
    M1 2 1 0 nmos; right
    R1 3 2 {1k}; down
    V1 3 0 {10}; down
    """)
    try:
        c3.draw('test_mosfet.png')
    except Exception as e:
        print("MOSFET error:", e)

    # Transformer
    c4 = Circuit("""
    V1 1 0 {120}; down
    TX1 1 0 2 0; right
    R1 2 0 {10}; down
    """)
    try:
        c4.draw('test_tx.png')
    except Exception as e:
        print("Transformer error:", e)

    print("Done")

test()
