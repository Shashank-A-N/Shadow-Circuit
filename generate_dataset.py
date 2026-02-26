import os
import random
import csv
from lcapy import Circuit, R, L, C, V

def parse_number(prompt, unit_regex):
    import re
    match = re.search(r'([\d.eE-]+)\s*([kKmMuU]?)\s*' + unit_regex, prompt, re.IGNORECASE)
    if not match: return None
    val = float(match.group(1))
    prefix = match.group(2).lower()
    if prefix == 'k': val *= 1000
    elif prefix == 'm': val *= 1e-3
    elif prefix == 'u': val *= 1e-6
    elif match.group(2) == 'M': val *= 1e6
    return val

def generate_custom_circuit(circuit_id, overrides=None, prompt=None):
    import re
    from lcapy import V, R, C, L
    
    # If no prompt is provided in this arg, maybe it's passed down from app.py
    if prompt is None and isinstance(overrides, str):
        prompt = overrides
    elif prompt is None:
        prompt = ""
        
    dataset_path = 'circuit_dataset'
    images_path = os.path.join(dataset_path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    components = []
    
    v_matches = re.finditer(r'([\d.eE-]+)\s*([kKmMuU]?)\s*v(?:olt(?:s)?)?(?:\s+source)?', prompt, re.IGNORECASE)
    for match in v_matches:
        val = parse_number(match.group(0), r'v(?:olt(?:s)?)?')
        if val is not None: components.append(('V', val))

    r_matches = re.finditer(r'([\d.eE-]+)\s*([kKmMuU]?)\s*(?:ohm(?:s)?|resistor)', prompt, re.IGNORECASE)
    for match in r_matches:
        val = parse_number(match.group(0), r'(?:ohm(?:s)?|resistor)')
        if val is not None: components.append(('R', val))

    c_matches = re.finditer(r'([\d.eE-]+)\s*([kKmMuU]?)\s*f(?:arad(?:s)?)?(?:\s+capacitor)?', prompt, re.IGNORECASE)
    for match in c_matches:
        val = parse_number(match.group(0), r'f(?:arad(?:s)?)?')
        if val is not None: components.append(('C', val))

    l_matches = re.finditer(r'([\d.eE-]+)\s*([kKmMuU]?)\s*h(?:enry)?(?:\s+inductor)?', prompt, re.IGNORECASE)
    for match in l_matches:
        val = parse_number(match.group(0), r'h(?:enry)?')
        if val is not None: components.append(('L', val))

    if not components:
        # Fallback to random basic RLC values if totally generic prompt
        components = [('V', 5), ('R', 100), ('L', 0.01), ('C', 0.0001)]

    lcapy_objs = []
    for comp_type, val in components:
        if comp_type == 'V': lcapy_objs.append(V(val))
        elif comp_type == 'R': lcapy_objs.append(R(val))
        elif comp_type == 'C': lcapy_objs.append(C(val))
        elif comp_type == 'L': lcapy_objs.append(L(val))

    expr = lcapy_objs[0]
    is_parallel = 'parallel' in prompt.lower()
    
    for obj in lcapy_objs[1:]:
        if is_parallel:
            expr = expr | obj
        else:
            expr = expr + obj

    description = f"Custom circuit natively compiled with {len(components)} parsed modules."
    filename = f'circuit_{circuit_id}.png'
    filepath = os.path.join(images_path, filename)
    try:
        expr.draw(filepath, style='american')
        print(f"Successfully generated custom circuit: {filename}")
        return filename, description
    except Exception as e:
        print(f"Could not draw {filename}. Error: {e}. Skipping.")
        return None, None

def generate_simple_rlc_circuit(circuit_id, overrides=None):
    if overrides is None:
        overrides = {}
        
    dataset_path = 'circuit_dataset'
    images_path = os.path.join(dataset_path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    voltage = overrides.get('voltage', random.randint(5, 24))
    resistance = overrides.get('resistance', random.randint(100, 1000))
    capacitance_val = overrides.get('capacitance', random.uniform(1e-5, 1e-3))
    inductance_val = overrides.get('inductance', random.uniform(1e-4, 1e-2))

    cct = Circuit(f"""
    V1 1 0 {{{voltage}}}; down
    W1 1 2; right
    W2 0 0a; right
    R1 2 0a {{{resistance}}}; down
    W3 2 3; right
    W4 0a 0b; right
    L1 3 0b {{{inductance_val:.2e}}}; down
    W5 3 4; right
    W6 0b 0c; right
    C1 4 0c {{{capacitance_val:.2e}}}; down
    """)

    description = f"A {voltage}V source connected to a {resistance} ohm resistor, a {inductance_val:.2e} Henry inductor, and a {capacitance_val:.2e} Farad capacitor in parallel."
    filename = f'circuit_{circuit_id}.png'
    filepath = os.path.join(images_path, filename)
    try:
        cct.draw(filepath, style='american', draw_nodes=False, node_spacing=2.5)
        print(f"Successfully generated RLC circuit: {filename}")
        return filename, description
    except Exception as e:
        print(f"Could not draw {filename}. Error: {e}. Skipping.")
        return None, None

def generate_bjt_amplifier_circuit(circuit_id, overrides=None):
    if overrides is None:
        overrides = {}

    dataset_path = 'circuit_dataset'
    images_path = os.path.join(dataset_path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    vdc = overrides.get('vdc', random.randint(9, 15))
    vac = overrides.get('vac', random.uniform(0.1, 1.0))
    r1_val = overrides.get('r1', random.randint(8, 15) * 1000)
    r2_val = overrides.get('r2', random.randint(1, 5) * 1000)
    r3_val = overrides.get('r3', random.randint(500, 2000))
    r4_val = overrides.get('r4', random.randint(100, 500))
    rl_val = overrides.get('rl', random.randint(5, 20) * 1000)
    c1_val = overrides.get('c1', random.uniform(1e-6, 10e-6))
    c2_val = overrides.get('c2', random.uniform(1e-6, 10e-6))

    cct = Circuit(f"""
    Vac in inGND ac {{{vac:.2f}}}; down
    W1 in inC; right, size=1.5
    W2 inGND bGND; right, size=1.5
    C1 inC B {{{c1_val:.2e}}}; right, size=1.5
    W3 bGND bGND2; right, size=1.5
    
    R2 B bGND2 {{{r2_val}}}; down
    W4 B qb; right, size=1.5
    W5 bGND2 bGND3; right, size=1.5
    
    V1 PVcc VccGND {{{vdc}}}; down
    W6 PVcc Vcc2; right, size=1.5
    W7 VccGND bGND3; right, size=1.5
    
    R1 Vcc2 qb {{{r1_val}}}; down
    Q1 qc qb qe npn; right, size=1.5
    
    W8 Vcc2 Vcc3; right, size=2.0
    W9 bGND3 qGND; right, size=2.0
    
    R4 qe qGND {{{r4_val}}}; down
    R3 Vcc3 qc {{{r3_val}}}; down
    
    W10 qc outC; right, size=2.0
    W11 qGND outGND; right, size=2.0
    C2 outC out {{{c2_val:.2e}}}; right, size=1.5
    W12 outGND outGND2; right, size=1.5
    
    RL out outGND2 {{{rl_val}}}; down
    """)

    description = f"A common-emitter BJT amplifier circuit powered by a {vdc}V DC source. The NPN transistor is biased by a voltage divider with R1={r1_val} ohms and R2={r2_val} ohms. An AC signal of {vac:.2f}V is coupled to the base through a {c1_val:.2e}F capacitor (C1). The collector resistor R3 is {r3_val} ohms and the emitter resistor R4 is {r4_val} ohms. The amplified output is coupled through C2 ({c2_val:.2e}F) to a load resistor RL of {rl_val} ohms."

    filename = f'circuit_{circuit_id}.png'
    filepath = os.path.join(images_path, filename)
    try:
        cct.draw(filepath, style='american', draw_nodes=False, node_spacing=2.5)
        print(f"Successfully generated BJT amplifier: {filename}")
        return filename, description
    except Exception as e:
        print(f"Could not draw {filename}. Error: {e}. Skipping.")
        return None, None

def generate_diode_rectifier_circuit(circuit_id, overrides=None):
    if overrides is None:
        overrides = {}

    dataset_path = 'circuit_dataset'
    images_path = os.path.join(dataset_path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    vac = overrides.get('vac', random.randint(12, 120))
    rl_val = overrides.get('rl', random.randint(100, 1000))
    c_val = overrides.get('c', random.uniform(10e-6, 1000e-6))

    cct = Circuit(f"""
    Vac 1 0 ac {{{vac}}}; down
    
    D1 4 2; down
    D2 2 5; down
    
    W3 4 4a; right, size=2.5
    W4 5 5a; right, size=2.5
    
    D3 4a 3; down
    D4 3 5a; down
    
    W1 1 2
    W2 0 3
    
    W5 4a 8; right, size=2.5
    W6 5a 9; right, size=2.5
    C1 8 9 {{{c_val:.2e}}}; down
    
    W7 8 10; right, size=2.0
    W8 9 11; right, size=2.0
    RL 10 11 {{{rl_val}}}; down
    """)

    description = f"A full-wave diode bridge rectifier circuit powered by a {vac}V AC source. It includes a smoothing capacitor C1 of {c_val:.2e}F and a load resistor RL of {rl_val} ohms."

    filename = f'circuit_{circuit_id}.png'
    filepath = os.path.join(images_path, filename)
    try:
        cct.draw(filepath, style='american', draw_nodes=False, node_spacing=2.5)
        print(f"Successfully generated diode rectifier: {filename}")
        return filename, description
    except Exception as e:
        print(f"Could not draw {filename}. Error: {e}. Skipping.")
        return None, None

def generate_opamp_circuit(circuit_id, overrides=None):
    if overrides is None:
        overrides = {}

    dataset_path = 'circuit_dataset'
    images_path = os.path.join(dataset_path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    vin = overrides.get('vin', random.uniform(0.1, 5.0))
    rin = overrides.get('rin', random.randint(1, 10) * 1000)
    rf = overrides.get('rf', random.randint(10, 100) * 1000)

    cct = Circuit(f"""
    Vin 1 0 {{{vin:.2f}}}; down
    W1 1 2; right, size=1.5
    W2 0 0a; right, size=1.5
    
    Rin 2 3 {{{rin}}}; right, size=2.0
    W3 0a 0b; right, size=2.0
    
    W4 3 3a; up
    Rf 3a 4a {{{rf}}}; right, size=2.5
    W5 4a 4; down
    
    E1 4 0b 0b 3 opamp; right
    """)

    description = f"An inverting operational amplifier circuit with an input voltage of {vin:.2f}V. The input resistor Rin is {rin} ohms and the feedback resistor Rf is {rf} ohms."

    filename = f'circuit_{circuit_id}.png'
    filepath = os.path.join(images_path, filename)
    try:
        cct.draw(filepath, style='american', draw_nodes=False, node_spacing=2.5)
        print(f"Successfully generated op-amp circuit: {filename}")
        return filename, description
    except Exception as e:
        print(f"Could not draw {filename}. Error: {e}. Skipping.")
        return None, None

def generate_mosfet_circuit(circuit_id, overrides=None):
    if overrides is None:
        overrides = {}

    dataset_path = 'circuit_dataset'
    images_path = os.path.join(dataset_path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    vdd = overrides.get('vdd', random.randint(5, 24))
    rg1 = overrides.get('rg1', random.randint(10, 100) * 1000)
    rg2 = overrides.get('rg2', random.randint(10, 100) * 1000)
    rd = overrides.get('rd', random.randint(1, 10) * 1000)
    rs = overrides.get('rs', random.randint(100, 1000))
    
    cct = Circuit(f"""
    V1 PVdd Pgnd {{{vdd}}}; down
    W1 PVdd PVdd2; right, size=1.5
    W2 Pgnd Pgnd2; right, size=1.5
    
    Rg1 PVdd2 G {{{rg1}}}; down
    Rg2 G Pgnd2 {{{rg2}}}; down
    
    W3 PVdd2 PVdd3; right, size=2.0
    W4 Pgnd2 Pgnd3; right, size=2.0
    W5 G gmos; right, size=2.0
    
    Rd PVdd3 D {{{rd}}}; down
    M1 D gmos S nmos; right
    Rs S Pgnd3 {{{rs}}}; down
    """)

    description = f"A common-source NMOS amplifier circuit powered by a {vdd}V DC source. The gate is biased using a voltage divider with Rg1={rg1} ohms and Rg2={rg2} ohms. The drain resistor Rd is {rd} ohms and the source resistor Rs is {rs} ohms."

    filename = f'circuit_{circuit_id}.png'
    filepath = os.path.join(images_path, filename)
    try:
        cct.draw(filepath, style='american', draw_nodes=False, node_spacing=2.5)
        print(f"Successfully generated MOSFET circuit: {filename}")
        return filename, description
    except Exception as e:
        print(f"Could not draw {filename}. Error: {e}. Skipping.")
        return None, None

def generate_filter_circuit(circuit_id, overrides=None):
    if overrides is None:
        overrides = {}

    dataset_path = 'circuit_dataset'
    images_path = os.path.join(dataset_path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    vin = overrides.get('vin', random.randint(5, 15))
    c1 = overrides.get('c1', random.uniform(1e-6, 10e-6))
    c2 = overrides.get('c2', random.uniform(1e-6, 10e-6))
    l1 = overrides.get('l1', random.uniform(1e-3, 10e-3))
    rl = overrides.get('rl', random.randint(100, 1000))

    cct = Circuit(f"""
    Vin 1 0 {{{vin}}}; down
    W1 1 2; right, size=1.5
    W2 0 0a; right, size=1.5
    
    C1 2 0a {{{c1:.2e}}}; down
    
    L1 2 3 {{{l1:.2e}}}; right, size=2.5
    W3 0a 0b; right, size=2.5
    
    C2 3 0b {{{c2:.2e}}}; down
    
    W4 3 4; right, size=2.0
    W5 0b 0c; right, size=2.0
    
    RL 4 0c {{{rl}}}; down
    """)

    description = f"A passive low-pass Pi-filter circuit connected to a {vin}V source. It consists of two shunt capacitors C1 ({c1:.2e}F) and C2 ({c2:.2e}F), and a series inductor L1 ({l1:.2e}H). The load resistor RL is {rl} ohms."

    filename = f'circuit_{circuit_id}.png'
    filepath = os.path.join(images_path, filename)
    try:
        cct.draw(filepath, style='american', draw_nodes=False, node_spacing=2.5)
        print(f"Successfully generated Pi-filter circuit: {filename}")
        return filename, description
    except Exception as e:
        print(f"Could not draw {filename}. Error: {e}. Skipping.")
        return None, None

def generate_transformer_circuit(circuit_id, overrides=None):
    if overrides is None:
        overrides = {}

    dataset_path = 'circuit_dataset'
    images_path = os.path.join(dataset_path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    vac = overrides.get('vac', random.randint(110, 240))
    l1 = overrides.get('l1', random.uniform(1.0, 5.0))
    l2 = overrides.get('l2', random.uniform(0.1, 0.5))
    k = overrides.get('k', random.uniform(0.95, 0.99))
    rl = overrides.get('rl', random.randint(10, 100))

    cct = Circuit(f"""
    Vac 1 0 ac {{{vac}}}; down
    W1 1 2; right, size=2.0
    W2 0 0a; right, size=2.0
    
    L1 2 0a {{{l1:.2f}}}; down
    L2 3 0b {{{l2:.2f}}}; down
    K1 L1 L2 {{{k:.3f}}}
    
    W3 3 4; right, size=2.0
    W4 0b 0c; right, size=2.0
    
    RL 4 0c {{{rl}}}; down
    """)

    description = f"A step-down transformer circuit with a {vac}V AC primary source. The primary inductance is {l1:.2f}H and the secondary is {l2:.2f}H, with a coupling coefficient of {k:.3f}. The secondary is connected to a {rl} ohm load."

    filename = f'circuit_{circuit_id}.png'
    filepath = os.path.join(images_path, filename)
    try:
        cct.draw(filepath, style='american', draw_nodes=False, node_spacing=2.5)
        print(f"Successfully generated transformer circuit: {filename}")
        return filename, description
    except Exception as e:
        print(f"Could not draw {filename}. Error: {e}. Skipping.")
        return None, None

def create_dataset(num_images):
    dataset_path = 'circuit_dataset'
    labels_file = os.path.join(dataset_path, 'labels.csv')

    print(f"Generating {num_images} mixed circuit images in '{dataset_path}/images'...")
    
    circuit_generators = [
        generate_simple_rlc_circuit, 
        generate_bjt_amplifier_circuit,
        generate_diode_rectifier_circuit,
        generate_opamp_circuit,
        generate_mosfet_circuit,
        generate_filter_circuit,
        generate_transformer_circuit
    ]

    with open(labels_file, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        generated_count = 0
        for i in range(num_images):
            # Deterministically cycle through them for varied testing
            generator_func = circuit_generators[i % len(circuit_generators)]
            filename, description = generator_func(i)
            
            if filename and description:
                writer.writerow({'filename': filename, 'description': description})
                generated_count += 1

    print("\\n--------------------")
    print(f"Dataset generation complete. {generated_count} images created.")
    print(f"Images are in: '{os.path.join(dataset_path, 'images')}'")
    print(f"Labels are in: '{labels_file}'")
    print("--------------------")

if __name__ == '__main__':
    number_of_images_to_generate = 50 
    create_dataset(number_of_images_to_generate)
