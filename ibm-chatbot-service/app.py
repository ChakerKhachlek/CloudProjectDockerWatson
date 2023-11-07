from flask import Flask, request, jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import config
from flask_cors import CORS
import json


app = Flask(__name__)

CORS(app)

# Initialize IBM Watson Assistant
authenticator = IAMAuthenticator(config.IBM_API_KEY)
assistant = AssistantV2(
    version='2023-07-22',
    authenticator=authenticator
)
assistant.set_service_url(config.IBM_SERVICE_URL)
assistant_id = config.IBM_ASSISTANT_ID

@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    message = data['message']
    context = data.get('context', {})  # Retrieve the context from the request
    print(context)
    try:
        # Send the message to Watson Assistant with the provided context
        response = assistant.message_stateless(
            assistant_id=assistant_id,
            input={
                'message_type': 'text',
                'text': message
            },
            context=context  # Provide the context to Watson Assistant
        ).get_result()

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
