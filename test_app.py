import requests

def test_app():
    try:
        url = 'http://127.0.0.1:5000/api/generate_circuit'
        payload = {'prompt': 'A 5V source connected to a 586 ohm resistor, a 6.79e-03 Henry inductor, and a 1.44e-04 Farad capacitor in parallel.'}
        response = requests.post(url, json=payload)
        print(response.json())
    except Exception as e:
        print(f"Error testing app: {e}")

if __name__ == '__main__':
    test_app()
