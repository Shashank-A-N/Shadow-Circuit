import re
from lcapy import V, I, R, C, L
from app import parse_number

def test_heuristic_parser(prompt):
    print(f"Prompt: {prompt}")
    
    components = []
    
    # Extract Voltage Sources
    v_matches = re.finditer(r'([\d.eE-]+)\s*([kKmMuU]?)\s*v(?:olt(?:s)?)?(?:\s+source)?', prompt, re.IGNORECASE)
    for i, match in enumerate(v_matches):
        val = parse_number(match.group(0), r'v(?:olt(?:s)?)?')
        components.append(('V', val))

    # Extract Resistors
    r_matches = re.finditer(r'([\d.eE-]+)\s*([kKmMuU]?)\s*(?:ohm(?:s)?|resistor)', prompt, re.IGNORECASE)
    for i, match in enumerate(r_matches):
        val = parse_number(match.group(0), r'(?:ohm(?:s)?|resistor)')
        components.append(('R', val))

    # Extract Capacitors
    c_matches = re.finditer(r'([\d.eE-]+)\s*([kKmMuU]?)\s*f(?:arad(?:s)?)?(?:\s+capacitor)?', prompt, re.IGNORECASE)
    for i, match in enumerate(c_matches):
        val = parse_number(match.group(0), r'f(?:arad(?:s)?)?')
        components.append(('C', val))

    # Extract Inductors
    l_matches = re.finditer(r'([\d.eE-]+)\s*([kKmMuU]?)\s*h(?:enry)?(?:\s+inductor)?', prompt, re.IGNORECASE)
    for i, match in enumerate(l_matches):
        val = parse_number(match.group(0), r'h(?:enry)?')
        components.append(('L', val))

    print(f"Components found: {components}")
    
    if not components:
        print("No components parsed.")
        return
        
    # Build generic expression
    # E.g., if there's "parallel" in prompt, group them in parallel, else series.
    # We can split by "parallel" or "series" keywords to do basic topology.
    # For now: if "parallel" is in the text, put everything in parallel with the source?
    
    # Create lcapy objects
    lcapy_objs = []
    for comp_type, val in components:
        if comp_type == 'V': lcapy_objs.append(V(val))
        elif comp_type == 'R': lcapy_objs.append(R(val))
        elif comp_type == 'C': lcapy_objs.append(C(val))
        elif comp_type == 'L': lcapy_objs.append(L(val))

    if not lcapy_objs:
        return

    expr = lcapy_objs[0]
    is_parallel = 'parallel' in prompt.lower()
    
    for obj in lcapy_objs[1:]:
        if is_parallel:
            expr = expr | obj
        else:
            expr = expr + obj
            
    try:
        cct = expr
        cct.draw('test_generic.png')
        print("Successfully drew generic circuit!")
    except Exception as e:
        print("Fail:", e)

if __name__ == '__main__':
    test_heuristic_parser("a 12V source with 500 ohm resistor and 1k ohm resistor and 10uF capacitor in series")
    test_heuristic_parser("A 5V source connected to a 586 ohm resistor, a 6.79e-03 Henry inductor, and a 1.44e-04 Farad capacitor in parallel.")
