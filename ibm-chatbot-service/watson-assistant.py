import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import config 

authenticator = IAMAuthenticator(config.IBM_API_KEY)
assistant = AssistantV2(
    version='2023-07-22',
    authenticator = authenticator
)

assistant.set_service_url(config.IBM_SERVICE_URL)


#create session
response = assistant.create_session(
    config.IBM_ASSISTANT_ID
).get_result()
session_json = json.dumps(response, indent=2)
session_dict = json.loads(session_json)
session_id = session_dict['session_id']
print(session_id)

#delete session
# response = assistant.delete_session(
#     IBM_ASSISTANT_ID,
# ).get_result()
# print("Session deleted...")

#send message

response = assistant.message(
    config.IBM_ASSISTANT_ID,
    session_id,
    input={
        'message_type': 'text',
        'text': 'Hello'
    }
).get_result()
print(json.dumps(response, indent=2))