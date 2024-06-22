from flask import Flask, request, jsonify
import time
from collections import deque
import requests
import random

app = Flask(__name__)
window_size = 10
window = deque(maxlen=window_size)

# Simulated third-party API response
def fetch_numbers(numberid):
    if numberid == 'p':
        # Simulate fetching prime numbers
        return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    elif numberid == 'f':
        # Simulate fetching Fibonacci numbers
        return [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    elif numberid == 'e':
        # Simulate fetching even numbers
        return [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    elif numberid == 'r':
        # Simulate fetching random numbers
        return random.sample(range(1, 101), 10)
    else:
        return []

@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    start_time = time.time()
    
    # Fetch numbers from simulated third-party API
    numbers = fetch_numbers(numberid)
    
    if not numbers:
        return jsonify({"error": "Invalid number ID"}), 400
    
    # Update window state
    prev_window_state = list(window)
    for num in numbers:
        window.append(num)
    curr_window_state = list(window)
    
    # Calculate average
    avg = sum(curr_window_state) / len(curr_window_state) if curr_window_state else 0
    
    # Prepare response
    response = {
        "windowPrevState": prev_window_state,
        "windowCurrState": curr_window_state,
        "numbers": numbers,
        "avg": round(avg, 2)
    }
    
    # Ensure response time is within 500 ms
    elapsed_time = time.time() - start_time
    if elapsed_time > 0.5:
        return jsonify({"error": "Request took too long to process"}), 500
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9876)
