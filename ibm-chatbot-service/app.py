from flask import Flask, request, jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import config
from flask_cors import CORS
import redis
import json

app = Flask(__name__)

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
CORS(app)

# Initialize IBM Watson Assistant
authenticator = IAMAuthenticator(config.IBM_API_KEY)
assistant = AssistantV2(
    version='2023-07-22',
    authenticator=authenticator
)
assistant.set_service_url(config.IBM_SERVICE_URL)
assistant_id = config.IBM_ASSISTANT_ID

#initial_context = {
#    'docker': 0
#}
#redis_client.set('context', json.dumps(initial_context))

"""
# Create a session
@app.route('/create_session', methods=['POST'])
def create_session():
    try:
        response = assistant.create_session(assistant_id)
        session_id = response.get_result()['session_id']
        return jsonify({'session_id': session_id})
    except Exception as e:
        return jsonify({'error': str(e)})

# Delete a session
@app.route('/delete_session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        assistant.delete_session(assistant_id, session_id)
        return jsonify({'message': 'Session deleted'})
    except Exception as e:
        return jsonify({'error': str(e)})


# Send a message to the chatbot
# Send a message to the chatbot
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    session_id = data['session_id']
    message = data['message']
    
    # Save the message to Redis before sending to the chatbot
    try:
        print("Test")
        # Generate a unique key for each message based on session
        message_key = f"session:{session_id}:message:{int(redis_client.incr('message_id'))}"
        
        print("msgKey",message_key)
        # Store the message in Redis
        redis_client.set(message_key, message)

    except Exception as e:
        return jsonify({'error': f"Failed to store in Redis: {str(e)}"})

    # Send the message to the chatbot
    try:
        response = assistant.message(assistant_id, session_id, input={'message_type': 'text', 'text': message})
        return jsonify({'response': response.get_result()})
    except Exception as e:
        return jsonify({'error': str(e)})
#envoyer un message à l'assistant
@app.route('/message1', methods=['POST'])
def handle_message():
    data = request.get_json()
    message_text = data['message']

    response = assistant.message_stateless(
        assistant_id=assistant_id,
        input={
            'message_type': 'text',
            'text': message_text
        }
    ).get_result()

    return jsonify(response)

@app.route('/get_data/<message_key>', methods=['GET'])
def get_data(message_key):
    try:
        # Retrieve the data from Redis using the message_key
        data = redis_client.get(message_key)

        if data is not None:
            return jsonify({'data': data})
        else:
            return jsonify({'error': 'Data not found'})

    except Exception as e:
        return jsonify({'error': f"Failed to retrieve data from Redis: {str(e)}"})
    
@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    try:
        # Get all keys in the Redis database
        all_keys = redis_client.keys('*')

        # Retrieve data for each key
        data = {}
        for key in all_keys:
            data[key] = redis_client.get(key)

        return jsonify({'data': data})

    except Exception as e:
        return jsonify({'error': f"Failed to retrieve data from Redis: {str(e)}"})





# ************************Stateless Context************************        
@app.route('/message', methods=['POST'])
def handle_message():
    print("test")
    data = request.get_json()
    message_text = data['message']
    print("message_text",message_text)

    # Get the context from Redis and convert it from bytes to a dictionary
    conversation_context = json.loads(redis_client.get('context').decode('utf-8'))

    # Send the message to Watson Assistant with the conversation context in the input
    response = assistant.message_stateless(
        assistant_id=assistant_id,
        input={
            'message_type': 'text',
            'text': message_text,
        },
        
        context=conversation_context  # Include the context in the input
    ).get_result()

    # Update the conversation context with the latest context from the response
    conversation_context = response.get('context', {})

    # Store the updated context back in Redis
    redis_client.set('context', json.dumps(conversation_context))

    # Log the conversation context in the Python console
    print(conversation_context)

    return jsonify(response)
"""
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    message = data['message']

    try:
        # Retrieve the conversation context from Redis
        context_data = redis_client.get('context')  # Modify this to match your context storage
        context = json.loads(context_data) if context_data else {}

        # Send the message to Watson Assistant with the conversation context
        response = assistant.message_stateless(
            assistant_id=assistant_id,
            input={
                'message_type': 'text',
                'text': message
            },
            context=context  # Provide the stored context to Watson Assistant
        ).get_result()

        # Update the conversation context in Redis
        redis_client.set('context', json.dumps(response['context']))  # Modify this to match your context storage

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
