# orchestrator_app.py
from flask import Flask, request, jsonify
import requests
import redis
import json
app = Flask(__name__)

# URL of the original app that connects to Watson Assistant
ORIGINAL_APP_URL = "http://localhost:5000"  # Replace with the actual host of the original app

# Redis connection
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    message = data['message']

    # Retrieve the conversation context from Redis
    context_data = redis_client.get('context')
    context = json.loads(context_data) if context_data else {}

    # Include the context in the data to be sent to the original app
    data['context'] = context

    try:
        # Send the message and context to the original app
        response = requests.post(f"{ORIGINAL_APP_URL}/message", json=data)

        if response.status_code == 200:
            response_data = response.json()
            # Update the conversation context in Redis
            redis_client.set('context', json.dumps(response_data.get('context', {})))
            return jsonify(response_data)
        else:
            return jsonify({'error': 'Original app error'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
