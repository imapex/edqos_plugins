"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib2
import urllib
import os
import json


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Event Driven Q.O.S. Manager. " \
                    "You can get the current relevance level of an application by saying, " \
                    "get relevance for facebook. " \
                    "You can also set the relevance of an application by saying, " \
                    "set relevance for facebook, to business relevant."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask to get, or set relevance."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the Event Driven Q.O.S. Manager. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def get_relevance(app_name, policy_scope):
    if not app_name:
        return "Missing search string"
    elif not policy_scope:
        return "Missing policy tag"
    else:
        r = urllib2.urlopen(os.getenv("edqos_url") + "/api/relevance/?app="+app_name+"&policy="+policy_scope)
        response = r.read()
        JSON_object = json.loads(response)
        return JSON_object


def set_relevance(app_name, policy_scope, target_relevance):
    valid_relevance = ["Business-Relevant", "Default", "Business-Irrelevant"]
    if not app_name:
        return "Missing search string"
    elif not policy_scope:
        return "Missing policy tag"
    elif target_relevance not in valid_relevance:
        return "Invalid or missing target relevance"
    else:
        data = urllib.urlencode({'app': app_name, 'policy': policy_scope, 'relevance': target_relevance})
        data = data.encode('ascii')
        r = urllib2.urlopen(os.getenv("edqos_url") + "/api/relevance/", data)
        response = r.read()
        JSON_object = json.loads(response)
        return JSON_object


def set_relevance_intent(intent, session):
    """
    Sets the relevance level of an application.
    """
    session_attributes = {}
    card_title = intent['name']
    should_end_session = True
    reprompt_text = None

    if 'app' in intent['slots']:
        app_name = intent['slots']['app']['value'].lower()
    if 'relevance' in intent['slots']:
        if intent['slots']['relevance']['value'] == "business relevant":
            relevance = "Business-Relevant"
        elif intent['slots']['relevance']['value'] == "business irrelevant":
            relevance = "Business-Irrelevant"
        elif intent['slots']['relevance']['value'] == "default":
            relevance = "Default"
        else:
            relevance = None

    if relevance is None:
        speech_output = "Unable to set the relevance for " + \
                        app_name + \
                        " because " + \
                        intent['slots']['app']['value'] + \
                        " is not a valid relevance."
    else:
        task_id = set_relevance(app_name, os.getenv("scope"), relevance)

    if task_id:
        speech_output = "I have set the relevance for the application, " + \
                        app_name + \
                        ", to " + \
                        relevance
    else:
        speech_output = "I was unable to set the relevance for the application, " + \
                        app_name + \
                        ". Please try again."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_relevance_intent(intent, session):
    """
    Gets the current relevance level of an application.
    """
    session_attributes = {}
    card_title = intent['name']
    reprompt_text = None

    if 'app' in intent['slots']:
        app_name = intent['slots']['app']['value'].lower()

    relevance = get_relevance(app_name, os.getenv("scope"))

    if relevance:
        speech_output = "The current relevance level of the application, " + \
                        app_name + \
                        ", is set to " + \
                        relevance
        should_end_session = True
    else:
        speech_output = "Unable to get the current relevance level of the application, " + \
                        app_name
        should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SetRelevance":
        return set_relevance_intent(intent, session)
    elif intent_name == "GetRelevance":
        return get_relevance_intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
