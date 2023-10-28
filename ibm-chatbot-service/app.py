from flask import Flask, request, jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import config
import redis  # Import the Redis library
import json
app = Flask(__name__)

# Initialize IBM Watson Assistant
authenticator = IAMAuthenticator(config.IBM_API_KEY)
assistant = AssistantV2(
    version='2023-07-22',
    authenticator=authenticator
)

assistant.set_service_url(config.IBM_SERVICE_URL)
assistant_id = config.IBM_ASSISTANT_ID

# Initialize the Redis client
redis_client = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)  

# Initialize the context in Redis with 'docker' set to 0
initial_context = {
    'docker': 0
}
redis_client.set('context', json.dumps(initial_context))

# ************************Stateful session************************
# # Create a session
# @app.route('/create_session', methods=['POST'])
# def create_session():
#     try:
#         response = assistant.create_session(assistant_id)
#         session_id = response.get_result()['session_id']
#         return jsonify({'session_id': session_id})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# # Delete a session
# @app.route('/delete_session/<session_id>', methods=['DELETE'])
# def delete_session(session_id):
#     try:
#         assistant.delete_session(assistant_id, session_id)
#         return jsonify({'message': 'Session deleted'})
#     except Exception as e:
#         return jsonify({'error': str(e)})


# # Send a message to the chatbot
# @app.route('/send_message', methods=['GET'])
# def send_message():
#     session_id = request.args.get('session_id')
#     message = request.args.get('message')
#     try:
#         response = assistant.message(assistant_id, session_id, input={'message_type': 'text', 'text': message})
#         return jsonify({'response': response.get_result()})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# ************************Stateless session************************        
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    message_text = data['message']

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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
