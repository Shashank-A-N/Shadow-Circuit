from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import time
import re
import traceback

# Import generator functions
from generate_dataset import (
    generate_simple_rlc_circuit,
    generate_bjt_amplifier_circuit,
    generate_diode_rectifier_circuit,
    generate_opamp_circuit,
    generate_mosfet_circuit,
    generate_filter_circuit,
    generate_transformer_circuit,
    generate_custom_circuit,
    parse_number
)

app = Flask(__name__, static_folder='static', template_folder='.')

# Create necessary directories
DATASET_PATH = 'circuit_dataset'
IMAGES_PATH = os.path.join(DATASET_PATH, 'images')
if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_PATH, filename)

@app.route('/api/generate_circuit', methods=['POST'])
def generate_circuit_api():
    data = request.json
    prompt = data.get('prompt', '').lower()
    
    if not prompt:
        return jsonify({'error': 'No prompt provided.'}), 400

    # Basic NLP routing
    generator_func = None
    circuit_type = "Unknown"
    overrides = {}
    
    if "bjt" in prompt or "amplifier" in prompt or "transistor" in prompt:
        generator_func = generate_bjt_amplifier_circuit
        circuit_type = "BJT Amplifier"
        v = parse_number(prompt, r'v(?:olt(?:s)?)?')
        r = parse_number(prompt, r'(?:ohm(?:s)?|resistor)')
        if v is not None: overrides['vdc'] = int(v)
        if r is not None: overrides['r1'] = int(r)
    elif "mosfet" in prompt or "nmos" in prompt or "pmos" in prompt:
        generator_func = generate_mosfet_circuit
        circuit_type = "MOSFET Amplifier"
        v = parse_number(prompt, r'v(?:olt(?:s)?)?')
        r = parse_number(prompt, r'(?:ohm(?:s)?|resistor)')
        if v is not None: overrides['vdd'] = int(v)
        if r is not None: overrides['rd'] = int(r)
    elif "opamp" in prompt or "op-amp" in prompt or "operational amplifier" in prompt:
        generator_func = generate_opamp_circuit
        circuit_type = "Operational Amplifier"
        v = parse_number(prompt, r'v(?:olt(?:s)?)?')
        r = parse_number(prompt, r'(?:ohm(?:s)?|resistor)')
        if v is not None: overrides['vin'] = float(v)
        if r is not None: overrides['rf'] = int(r)
    elif "diode" in prompt or "rectifier" in prompt or "bridge" in prompt:
        generator_func = generate_diode_rectifier_circuit
        circuit_type = "Diode Rectifier"
        v = parse_number(prompt, r'v(?:olt(?:s)?)?')
        r = parse_number(prompt, r'(?:ohm(?:s)?|resistor)')
        c = parse_number(prompt, r'f(?:arad(?:s)?)?')
        if v is not None: overrides['vac'] = int(v)
        if r is not None: overrides['rl'] = int(r)
        if c is not None: overrides['c'] = float(c)
    elif "filter" in prompt or "low pass" in prompt or "high pass" in prompt:
        generator_func = generate_filter_circuit
        circuit_type = "Passive Filter"
        v = parse_number(prompt, r'v(?:olt(?:s)?)?')
        r = parse_number(prompt, r'(?:ohm(?:s)?|resistor)')
        ind = parse_number(prompt, r'h(?:enry)?')
        cap = parse_number(prompt, r'f(?:arad(?:s)?)?')
        if v is not None: overrides['vin'] = int(v)
        if r is not None: overrides['rl'] = int(r)
        if ind is not None: overrides['l1'] = float(ind)
        if cap is not None: overrides['c1'] = float(cap)
    elif "transformer" in prompt or "step-down" in prompt or "step-up" in prompt:
        generator_func = generate_transformer_circuit
        circuit_type = "Transformer"
        v = parse_number(prompt, r'v(?:olt(?:s)?)?')
        r = parse_number(prompt, r'(?:ohm(?:s)?|resistor)')
        if v is not None: overrides['vac'] = int(v)
        if r is not None: overrides['rl'] = int(r)
    else:
        # Default to Custom Parser
        generator_func = generate_custom_circuit
        circuit_type = "Custom Schematic"
        overrides = prompt # Pass the prompt raw string into overrides

    # Generate a unique ID for the image
    unique_id = f"web_{int(time.time())}"
    
    try:
        filename, description = generator_func(unique_id, overrides)
        if filename and description:
            # Construct a brief verification string
            verification = f"Generated {circuit_type}. Does this meet your requirements? You can ask for a different type by changing keywords."
            return jsonify({
                'success': True,
                'image_url': f"/images/{filename}",
                'description': description,
                'verification': verification,
                'circuit_type': circuit_type
            })
        else:
            return jsonify({'error': 'Failed to generate circuit diagram.'}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
