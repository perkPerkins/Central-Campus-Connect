"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""
from __future__ import print_function
from search_function import search_fun
from web_function import start_web
from web_function import Db_session
from canvas_function import Canvas_Session
import web_function
import canvas_function
import sys
import logging
import pymysql
import bs4

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

"""
Get response function which will get the hours or location for an intent
"""
def get_hours_response(intent):

    session_attributes = {}
    
    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Hours"

    # How to get slot values from what the user said
    # item slot is the specific place the user is requesting information on
    # whatTime slot will delineate between a request for when a building opens vs. closes
    itemName = intent['slots']['item']['value'] # building name

    #TEST DB CODE
    #REMEMBER! I TURN OFF DB WHEN NOT IN USE
    # db_session = web_function.Db_session()
    # db_session.connect_to_db(db_session.rds_host, db_session.name, db_session.password, db_session.db_name)
    #Samuelson already added, here is the format to add new buildings to the db
    #(Building name, location of bulding, open time, close time, purpose tag)
    #db_session.add_building("Samuelson", "Near the Bistro", "08:00:00", "19:00:00", "classes")

    if 'day' in intent['slots']:
        if 'value' in intent['slots']['day']:
            itemDay = intent['slots']['day']['value']
            slot_list = [itemName, 'hours', itemDay]
            speech_output = "The " + itemName + " is available from " + start_web(list(slot_list))
        else:
            slot_list = [itemName, 'hours']
            speech_output = "The " + itemName + " is available from " + start_web(list(slot_list))    
    else:
        slot_list = [itemName, 'hours']
        speech_output = "The " + itemName + " is available from " + start_web(list(slot_list))   
    
    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = False

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


"""
Get response function which will find what an intent is
"""
def get_fact_response(intent):
    session_attributes = {}

    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Hours"

    #For example: What does the ACM club do?
    # Output
    speech_output = "query to database that has table of facts?"

    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = False

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
"""
Get response function that returns the description of clubs
"""
def get_club_Description_response(intent):
    session_attributes = {}

    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Club Description"
    
    club = intent['slots']['club_name']['value']
    
    db_session = web_function.Db_session()
    if db_session.connect_to_db(db_session.rds_host, db_session.name, db_session.password, db_session.db_name):
        results = db_session.get_row_from_table("Clubs", club)
        speech_output = club + " is " + results[3]
    else:
        speech_output = "I'm sorry, we can't contact the database at the moment. Try again later."


    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = True

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_user_classes_response(intent):
    session_attributes = {}

    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Classes"
    
    speech_output = ""
    
    db_session = web_function.Db_session()
    if db_session.connect_to_db(db_session.rds_host, db_session.name, db_session.password, db_session.db_name):
        results = db_session.get_row_from_table("Students", 1234567)
        
        token = results[4]
        
        canvas = canvas_function.Canvas_Session(token)
        class_list = canvas.get_courses()
    
        speech_output = "your current classes are "
        for n in class_list:
            speech_output += n + ", "
    else:
        speech_output = "I'm sorry, we can't contact the database at the moment. Try again later."
    
    
    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = True

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

def get_user_assignments_response(intent):
    session_attributes = {}
    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Classes"
    
    speech_output = ""
    
    db_session = web_function.Db_session()
    if db_session.connect_to_db(db_session.rds_host, db_session.name, db_session.password, db_session.db_name):
        results = db_session.get_row_from_table("Students", 1234567)
        
        token = results[4]
        
        canvas = canvas_function.Canvas_Session(token)
        assignment_list = canvas.get_assignments_on_day("2020-02-06")
    
        speech_output = "The assignments due are: "
        for n in assignment_list:
            speech_output += n[1]  + " for the class " + n[0] + ", "
    else:
        speech_output = "I'm sorry, we can't contact the database at the moment. Try again later."
    
    
    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = True

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

"""
Get response function which will find where to get an intent
"""
def get_item_response(intent):
    session_attributes = {}
    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Hours"

    # for example: Where can I get a pizza? Where can I get my books?
    # How to get slot values from what the user said
    itemName = intent['slots']['item']['value']
    getItem = intent['slots']['getItem']['value']

    # Output
    speech_output = "You can " + getItem + "" + itemName + " at " + search_fun(itemName, getItem)

    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = False

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def authenticate(intent):
    
    session_attributes = {}
    
    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Staff"

    # How to get slot values from what the user said
    sid = intent['slots']['StudentID']['value']
    pin = intent['slots']['AuthPIN']['value']

    speech_output = ""
    
    db_session = web_function.Db_session()
    if db_session.connect_to_db(db_session.rds_host, db_session.name, db_session.password, db_session.db_name):
        results = db_session.get_row_from_table("Students", sid)
        
        speech_output = "Hello, " + results[1]
        
        session_attributes.update({"isAuthenticated":True})

    else:
        speech_output = "I'm sorry, we can't contact the database at the moment. Try again later."

    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = False

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

"""
Get response function which will find information about a staff member
"""
def get_staff_response(intent):
    session_attributes = {}
    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Staff"

    # How to get slot values from what the user said
    staffName = intent['slots']['staffName']['value']
    item = intent['slots']['officeHours']['value']

    # Output
    speech_output = staffName + "'s " + item + " is " + search_fun(staffName, item)

    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = False

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


"""
Get response function which will find where an intent is located
"""
def get_location_response(intent):
    session_attributes = {}
    # Some sort of title, doesn't seem to be too important, but should keep accurate
    card_title = "Hours"

    # How to get slot values from what the user said
    # item slot is the specific place the user is requesting information on
    itemName = intent['slots']['item']['value'] # building name
    itemStatus = intent['slots']['where']['value'] # this will just be where, may not be needed

    #TEST DB CODE
    #REMEMBER! I TURN OFF DB WHEN NOT IN USE
    # db_session = web_function.Db_session()
    # db_session.connect_to_db(db_session.rds_host, db_session.name, db_session.password, db_session.db_name)
    #Samuelson already added, here is the format to add new buildings to the db
    #(Building name, location of bulding, open time, close time, purpose tag)
    #db_session.add_building("Samuelson", "Near the Bistro", "08:00:00", "19:00:00", "classes")
    
    speech_output = ""
    
    # If the user didn't say anything, Alexa can yell at you
    reprompt_text = "You never responded to the first test message. Sending another one."

    # If this response should end the skill
    should_end_session = False

    # Return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

"""
Get response function which will welcome the user to the skill
"""
def get_welcome_response():
    session_attributes = {}
    
    card_title = "Welcome"
    
    speech_output = "Welcome to central Connect! Please ask me a question about Central!"
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, please ask me a question about Central!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

#-------------------------Intent to Function Dictionary-----------------

# Dictionary containing all intent definitions that are basic FAQ
intent_dict = { "Amazon.HelpIntent":get_welcome_response,
                "Hours":get_hours_response,
                "Club_Info":get_club_Description_response,
                "Facts":get_fact_response,
                "Staff":get_staff_response,
                "Authenticate":authenticate
                }
    
# Dictionary containing all intent definitions that use PII           
pii_intent_dict = { "Classes":get_user_classes_response,
                    "Assignments":get_user_assignments_response
                    }
# ------------------------ End ------------------------------------------
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying CWU Connect. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------
def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    hasAuth = False
    if 'attributes' in session:
        sessionAtr = session.get('attributes')
        if 'isAuthenticated' in sessionAtr:
            hasAuth = sessionAtr.get('isAuthenticated')
    
    #Be sure to add to the intent_dict once new functions have been added
    
    if intent_name in intent_dict:
        return intent_dict.get(intent_name)(intent)
    elif (intent_name in pii_intent_dict):
        if hasAuth:
            return pii_intent_dict.get(intent_name)(intent)
        else:
            out = "I'm sorry, you have not authenticated yet. Say, \"log me in\" to authenticate"
            return build_response({}, build_speechlet_response("No authentication", out, None, False))
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