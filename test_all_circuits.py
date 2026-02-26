import os
from generate_dataset import *

def test_all():
    # create test directory if not exist
    if not os.path.exists("test_outputs"):
        os.makedirs("test_outputs")

    overrides = {
        'voltage': 10, 'resistance': 100, 'inductance': 1e-3, 'capacitance': 1e-4,
        'vdc': 15, 'vac': 2, 'r1': 1000, 'r2': 2000, 'r3': 3000, 'r4': 4000, 'rl': 5000, 'c1': 1e-5, 'c2': 1e-5,
        'c': 1e-4, 'vin': 5, 'rin': 1000, 'rf': 10000, 'vdd': 20, 'rg1': 100, 'rg2': 200, 'rd': 300, 'rs': 400,
        'l1': 1e-3, 'l2': 2e-3, 'k': 0.98
    }

    funcs = [
        ("rlc", generate_simple_rlc_circuit),
        ("bjt", generate_bjt_amplifier_circuit),
        ("diode", generate_diode_rectifier_circuit),
        ("opamp", generate_opamp_circuit),
        ("mosfet", generate_mosfet_circuit),
        ("filter", generate_filter_circuit),
        ("transformer", generate_transformer_circuit)
    ]

    for name, f in funcs:
        try:
            print(f"Testing {name} ...")
            f(f"test_{name}", overrides)
        except Exception as e:
            print(f"FAILED {name}: {e}")

if __name__ == "__main__":
    test_all()
