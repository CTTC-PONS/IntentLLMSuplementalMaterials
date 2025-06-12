import json
import random
import datetime
import boto3
import intentExplainer
import intentGeneration
import jsonTemplates

def validateInputs(intent, slots):

    validDescriptionTypes = ["locations", "network limitations", "all"]
    
    if intent == "explainIntent":
        if not slots['intentID']:
            
            return {'isValid': False, 'violatedSlot': 'intentID'}
        
        if not slots['descriptionType']:
            return { 'isValid': False, 'violatedSlot': 'descriptionType'}
        
        if slots['descriptionType']['value']['originalValue'].lower() not in  validDescriptionTypes:
            
            return { 'isValid': False, 'violatedSlot': 'descriptionType', 'message': 'I am sorry I don´t understand {} as a valid description type. It has to be one of these: locations, network limitations or all'.format(", ".join(valid_cities)) }
    elif intent == "SearchForIntents":
        #si no hay atributos
        if not slots['attributeName']:
            return { 'isValid': False, 'violatedSlot': 'attributeName' }
        elif not slots['attributeValue']:
            return { 'isValid': False, 'violatedSlot': 'attributeValue' }
        
        #si los atributos son none
        attributeList = [ "jsonid", "intentid", "endpointsid", "time", "no" ]
        #if slots['attributeName']["value"]["originalValue"] == 'none':
        if slots['attributeName']["value"]["originalValue"] not in attributeList:
            return { 'isValid': False, 'violatedSlot': 'attributeName' }
        elif slots['attributeValue']["value"]["originalValue"] == 'none':
            if slots['attributeName']["value"]["originalValue"] == 'no':
                slots['attributeValue']["value"] = slots['attributeName']["value"]
                return {'isValid': True}
            else:
                return { 'isValid': False, 'violatedSlot': 'attributeValue' }
            
    elif intent == "generateIntents":
        
        if not slots['action']:
            return { 'isValid': False, 'violatedSlot': 'action' }
        
        if not slots['locationDescription']:
            return { 'isValid': False, 'violatedSlot': 'locationDescription' }
        
        if not slots['restrictionsDescription']:
            return { 'isValid': False, 'violatedSlot': 'restrictionsDescription' }

    return {'isValid': True}
    
###############################
#  Retrieve intents from the database:
###############################

dynamoDBClient = boto3.resource("dynamodb")
table = dynamoDBClient.Table('JsonIntents')

def lambda_handler(event, context):
    
    slots = event["sessionState"]["intent"]["slots"]
    intent = event["sessionState"]["intent"]["name"]
    validation_result = validateInputs(intent, event['sessionState']['intent']['slots'])
    #print(event)
    print(slots)
    #print(intent)
    
    #this section occurs when the data has not been completely included yet
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit': validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                    }
                }
            }
            
        return response
        
    print( "Event" + event['invocationSource'] )
        
    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        print("The end condition has been accomplished!")
        
        if intent == "explainIntent":
            print("Inside explainIntent")
            print(slots['intentID']['value'])
            retrievedJson = table.get_item(Key={'jsonid': int(slots['intentID']['value']['originalValue'])})
            #This is the part where the intent explainer code carries on:
            networkRequest = retrievedJson["Item"]["jsonObject"]
            print(str(networkRequest))
            print(type(networkRequest))
            #networkRequest = json.loads(networkRequest)
            message = intentExplainer.intentExplainer.createMessageIntentExplainer(slots, networkRequest)
        elif intent == "SearchForIntents":
            message = "default message"
            print("Inside SearchForIntents")
            print(slots)
            response = table.scan()
            if slots['attributeValue']['value']["originalValue"] == 'no':
                message = str(response['Items'])
            else:
                filteredResponse = ""
                for item in response['Items']:
                    print(str(item['jsonid']))
                    print(str(item))
                    if slots['attributeName']['value']["originalValue"] == "jsonid":
                        if str(item['jsonid']) == slots['attributeValue']['value']["originalValue"]:
                            filteredResponse = filteredResponse + str(item)
                    elif slots['attributeName']['value']["originalValue"] == "intentid":
                        intentId = item['jsonObject']
                        intentId = intentId.split('"service_uuid": {"uuid": "')[1]
                        print(intentId)
                        intentId = intentId.split('"')[0]
                        print(intentId)
                        if intentId == slots['attributeValue']['value']["originalValue"]:
                            filteredResponse = filteredResponse + str(item)
                    elif slots['attributeName']['value']["originalValue"] == "time":
                        totalTime = item['jsonObject']
                        if "time[sec]" in totalTime:
                            totalTime = totalTime.split('"time[sec]", "constraint_value": "')[1]
                        print(totalTime)
                        totalTime = totalTime.split('"')[0]
                        print(totalTime)
                        if totalTime == slots['attributeValue']['value']["originalValue"]:
                            filteredResponse = filteredResponse + str(item)
                    elif slots['attributeName']['value']["originalValue"] == "endpointsid":
                        endpointsid = item['jsonObject']
                        if "device_uuid" in endpointsid:
                            endpointsid = endpointsid.split('{"device_id": {"device_uuid": {"uuid": "')[1]
                            for i in range(1,len(endpointsid)):
                                endpointsid = endpointsid.split('"')[0]
                                if endpointsid == slots['attributeValue']['value']["originalValue"]:
                                    filteredResponse =  str(item)
                
                if filteredResponse == []:
                    message = "There were no registered items matching your criteria on the database"
                else:
                    message = str(filteredResponse)
        elif intent == "generateIntents":
            print("Inside generateIntent")
            print( slots )
            
            action = slots["action"]["value"]["originalValue"]
            locationsDescription = slots["locationDescription"]["value"]["originalValue"]
            restrictionsDescription = slots["restrictionsDescription"]["value"]["originalValue"]
            
            resources = intentGeneration.intentGeneration.reconizeResources(restrictionsDescription)
            locations = intentGeneration.intentGeneration.reconizeLocations(locationsDescription)
            times = intentGeneration.intentGeneration.recognizeTimes(restrictionsDescription)
            totalTime = intentGeneration.intentGeneration.calculateTotalTimeSeconds(times)
            bandwidth = intentGeneration.intentGeneration.reconizeOtherRestrictions(restrictionsDescription)
            quality = intentGeneration.intentGeneration.recognizeQuality(restrictionsDescription)
            json = intentGeneration.intentGeneration.generateConnectionService(locations, totalTime, bandwidth)
            
            message = str(json)
            
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name':intent,
                    'slots': slots,
                    'state':'Fulfilled'
                    
                    }
            
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": message
                }
            ]
        }
        
        return response
