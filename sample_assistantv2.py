import logging
import json
import base64
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    #authenticate with watson
    authenticator = IAMAuthenticator("Ri7Mx4xbBjxsKan8BxT8aaU6SO75_eho830bReM4azBL")
    assistant = AssistantV2(
        version='2020-02-05',
        authenticator=authenticator
    )

    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/4aac63e2-3730-428d-b87e-21075a9e853e/v2/assistants/95bfa4f0-52dc-41f1-afb6-a46e11ffe94f/sessions')
    session = assistant.create_session("95bfa4f0-52dc-41f1-afb6-a46e11ffe94f").get_result()

    #decode and store message body from alexa
    rawBody = base64.b64decode(dict["__ow_body"])
    jsonBody = json.loads(rawBody)

    #send message to watson and send watson's response back to alexa
    if "intent" in jsonBody['request']:
        request = jsonBody['request']['intent']
        if "slots" in request:
            request = json.dumps(jsonBody['request']['intent']['slots']['EverythingSlot']['value'])
            message = assistant.message("95bfa4f0-52dc-41f1-afb6-a46e11ffe94f",session["session_id"],input= {'message_type': 'text','text': request}).get_result()
            return { 'version': '1.0','response': { 'outputSpeech': { 'type': 'PlainText','text': json.dumps(message['output']['generic'][0]['text'])},'shouldEndSession': 'false'}};
        else:
            message = assistant.message("95bfa4f0-52dc-41f1-afb6-a46e11ffe94f",session["session_id"],input= {'message_type': 'text','text': 'goodbye watson'}).get_result()
            return { 'version': '1.0','response': { 'outputSpeech': { 'type': 'PlainText','text': json.dumps(message['output']['generic'][0]['text'])},'shouldEndSession': 'true'}};
    else:
        message = assistant.message("95bfa4f0-52dc-41f1-afb6-a46e11ffe94f",session["session_id"],input= {'message_type': 'text','text': 'hello from alexa'}).get_result()
        return { 'version': '1.0','response': { 'outputSpeech': { 'type': 'PlainText','text': json.dumps(message['output']['generic'][0]['text'])},'shouldEndSession': 'false'}};

    assistant.delete_session("54907146-52b1-4b82-a89c-4f7a6beaacb8", session["session_id"]).get_result()
