import os
from lcapy import Circuit

def test_rlc():
    cct = Circuit("""
    V1 1 0 12; up
    W1 1 2; right
    W2 0 0a; right
    R1 2 0a 100; down
    W3 2 3; right
    W4 0a 0b; right
    L1 3 0b 1e-3; down
    W5 3 4; right
    W6 0b 0c; right
    C1 4 0c 1e-6; down
    """)
    cct.draw('test_1_rlc.png')

def test_bjt():
    cct = Circuit("""
    Vac in in_gnd ac 0.1; down
    W1 in in_C; right
    W2 in_gnd b_gnd; right
    C1 in_C B 1e-6; right
    
    R2 B b_gnd 2200; down
    W3 B q_b; right
    
    V1 P_Vcc P_Vcc_gnd 15; down
    W4 P_Vcc P_Vcc2; right
    W5 P_Vcc_gnd b_gnd2; right
    W6 b_gnd b_gnd2; right
    
    R1 P_Vcc2 q_b 10000; down
    
    Q1 q_c q_b q_e npn; right
    
    W7 P_Vcc2 P_Vcc3; right
    W8 b_gnd2 q_gnd; right
    
    R4 q_e q_gnd 100; down
    R3 P_Vcc3 q_c 1000; down
    
    W9 q_c out_c; right
    W10 q_gnd out_gnd; right
    C2 out_c out 1e-6; right
    
    RL out out_gnd 5000; down
    """)
    cct.draw('test_2_bjt.png')

def test_diode():
    cct = Circuit("""
    Vac 1 0 ac 24; up
    W1 1 top; right
    W2 0 bot; right

    D1 top right_node; right+down
    D2 bot right_node; right+up
    D3 left_node top; right+up
    D4 left_node bot; right+down

    W3 left_node ac_in_l; left
    W4 ac_in_l ac_in_v; down
    W_wait_how_to_ac 0 bot; 

    # Wait, just use standard bridge:
    """)

def test_diode2():
    cct = Circuit("""
    Vac 1 0 ac 24; up
    D1 1 2; right+down
    D2 0 2; right+up
    D3 3 1; right+up
    D4 3 0; right+down
    
    W1 2 2_r; right
    W2 3 3_r; left
    
    C1 2_r 0_r 1e-5; down
    """)
    try:
        cct.draw('test_3_diode.png')
    except Exception as e:
        print("Diode failed:", e)

def test_opamp():
    cct = Circuit("""
    Vin 1 0 1; down
    W1 1 2; right
    W2 0 0a; right
    Rin 2 3 1000; right
    W3 0a 0b; right
    W4 3 3a; up
    Rf 3a 4a 10000; right
    W5 4a 4; down
    O1 4 0b 3 opamp; right
    """)
    try:
        cct.draw('test_4_opamp.png')
    except Exception as e:
        print("Opamp failed:", e)

def test_mosfet():
    cct = Circuit("""
    V1 P_Vdd P_gnd 15; down
    W1 P_Vdd P_Vdd2; right
    W2 P_gnd P_gnd2; right
    Rg1 P_Vdd2 G 10000; down
    Rg2 G P_gnd2 10000; down
    W3 P_Vdd2 P_Vdd3; right
    W4 P_gnd2 P_gnd3; right
    W5 G g_mos; right
    Rd P_Vdd3 D 1000; down
    M1 D g_mos S nmos; right
    R_s S P_gnd3 100; down
    """)
    try:
        cct.draw('test_5_mosfet.png')
    except Exception as e:
        print("Mosfet failed:", e)

def test_filter():
    cct = Circuit("""
    Vin 1 0 10; up
    W1 1 2; right
    W2 0 0a; right
    C1 2 0a 1e-6; down
    L1 2 3 1e-3; right
    W3 0a 0b; right
    C2 3 0b 1e-6; down
    W4 3 4; right
    W5 0b 0c; right
    RL 4 0c 100; down
    """)
    try:
        cct.draw('test_6_filter.png')
    except Exception as e:
        print("Filter failed:", e)

def test_tx():
    cct = Circuit("""
    Vac 1 0 ac 120; up
    W1 1 2; right
    W2 0 0a; right
    L1 2 0a 1.0; down
    L2 3 0b 0.1; down
    K1 L1 L2 0.95
    W3 3 4; right
    W4 0b 0c; right
    RL 4 0c 10; down
    """)
    try:
        cct.draw('test_7_tx.png')
    except Exception as e:
        print("TX failed:", e)

if __name__ == '__main__':
    test_rlc()
    test_bjt()
    test_diode2()
    test_opamp()
    test_mosfet()
    test_filter()
    test_tx()
    print("Test run finished.")
