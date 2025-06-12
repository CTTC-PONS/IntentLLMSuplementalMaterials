import json
import random
import datetime
import boto3

class intentExplainer():
    
    def reconizeLocations(networkRequest):
        locations = networkRequest["services"][0]["service_endpoint_ids"]
    
        recognizedLocations = dict()
        i = 1
        for loc in locations:
            recognizedLocations[ loc['device_id']['device_uuid']['uuid'] ] = loc['endpoint_uuid']['uuid']
            i = i + 1
    
        return recognizedLocations
        
    def reconizeConstraints(networkRequest):
        constraints = networkRequest["services"][0]["service_constraints"]
    
        recognizedConstraints = dict()
        i = 1
    
        for const in constraints:
            recognizedConstraints[const['custom']['constraint_type']] = const['custom']['constraint_value']
            i = i + 1
            
        return recognizedConstraints
        
    def expressLocations(recognizedLocations):    
        locationsTemplate1 = ""
        n = random.random()
        if len(recognizedLocations) == 0:
            if n < 0.33:
                locationsTemplate1 = "The given request does not recognize any specific locations. "
            elif n < 0.66:
                locationsTemplate1 = "The given request does not specify any locations. "
            else:
                locationsTemplate1 = "There are no specified locations on the given request. "
        elif len(recognizedLocations) == 1:
            if n < 0.33:
                locationsTemplate1 = "This network request specifies one location. "
            elif n < 0.66:
                locationsTemplate1 = "Only one location is specified on the network request. "
            else:
                locationsTemplate1 = "This network request contains only one location. "
        else:
            if n < 0.33:
                locationsTemplate1 = f"In this network request, there are locations regarding {len(recognizedLocations)} points: First, "
            elif n < 0.66:
                locationsTemplate1 = f"This network request specifies {len(recognizedLocations)} location points: First, "
            else:
                locationsTemplate1 = f"There are {len(recognizedLocations)} indicated locations points on the specified request: First, "
    
        i = 1
        locationsTemplate2 = ""
        for key in recognizedLocations:
            if i == 2:
                locationsTemplate2 = locationsTemplate2 + "Second, "
            elif i > 2:
                locationsTemplate2 = locationsTemplate2 + "Finally, "
    
            n = random.random()
    
            if n < 0.33:
                locationsTemplate2 = locationsTemplate2 + f"The location labeled as {key} is placed on the port {recognizedLocations[key]}. "
            elif n < 0.66:
                locationsTemplate2 = locationsTemplate2 + f"The location {key} which is located on the port {recognizedLocations[key]}. "
            else:    
                locationsTemplate2 = locationsTemplate2 + f"The location labeled as {key} on the port {recognizedLocations[key]}. "
    
            i = i + 1
    
        return locationsTemplate1 + locationsTemplate2
        
    def expressLimitations(recognizedConstraints):    
        limitationsTemplate1 = ""
        n = random.random()
    
        if len(recognizedConstraints) == 0:
            if n < 0.33:
                limitationsTemplate1 = "The given request does not include any limitations. "
            elif n < 0.66:
                limitationsTemplate1 = "The given request does not contain any specific limitations. "
            else:
                limitationsTemplate1 = "There are no specified limitations on the given network request. "
        elif len(recognizedConstraints) == 1:
            if n < 0.33:
                limitationsTemplate1 = "This network request contains one limitation. "
            elif n < 0.66:
                limitationsTemplate1 = "One limitation is included. "
            else:
                limitationsTemplate1 = "Only one limitation is included on the network request. "
        else:
            if n < 0.33:
                limitationsTemplate1 = f"In this network request, {len(recognizedConstraints)} limitations can be found: First, "
            elif n < 0.66:
                limitationsTemplate1 = f"This network request specifies {len(recognizedConstraints)} limitations: First, "
            else:
                limitationsTemplate1 = f"There are {len(recognizedConstraints)} limitations on the specified request: First, "
    
        i = 1
        limitationsTemplate2 = ""
        for key in recognizedConstraints:
            if i == 2:
                limitationsTemplate2 = limitationsTemplate2 + "Second, "
            elif i > 2:
                limitationsTemplate2 = limitationsTemplate2 + "Finally, "
    
            if key == "time[sec]":
                convertedTime = str(datetime.timedelta(seconds=int(recognizedConstraints["time[sec]"])))
                
                n = random.random()
                if n < 0.33:
                    limitationsTemplate2 = limitationsTemplate2 + f"The request will be valid during {recognizedConstraints['time[sec]']} seconds which is {convertedTime}. "
                elif n < 0.66:
                    limitationsTemplate2 = limitationsTemplate2 + f"A time limitation of {recognizedConstraints['time[sec]']} seconds ({convertedTime}) is specified. "
                else:    
                    limitationsTemplate2 = limitationsTemplate2 + f"A time limit of {recognizedConstraints['time[sec]']} seconds({convertedTime}). "
            
            elif key == "bandwidth":
                
                if recognizedConstraints["bandwidth"] == "10.0":
                    convertedBandwith = "low"
                elif recognizedConstraints["bandwidth"] == "20.0":
                    convertedBandwith = "medium"
                elif recognizedConstraints["bandwidth"] == "40.0":
                    convertedBandwith = "high"
                else:
                    convertedBandwith = "unrecognized"
                    
                n = random.random()
                if n < 0.33:
                    limitationsTemplate2 = limitationsTemplate2 + f"A {convertedBandwith} bandwidth limitation is requested, more accurately {recognizedConstraints['bandwidth']} Mbps. "
                elif n < 0.66:
                    limitationsTemplate2 = limitationsTemplate2 + f"a Bandwidth limitation of {recognizedConstraints['bandwidth']} Mbps is requested which is considered {convertedBandwith} quality. "
                else:    
                    limitationsTemplate2 = limitationsTemplate2 + f"A {convertedBandwith} quality bandwith limitation is included ( {recognizedConstraints['bandwidth']} Mbps.) "
            
            
            i = i + 1
    
        return limitationsTemplate1 + limitationsTemplate2
    
    def createMessageIntentExplainer (slots, networkRequest):
        
        networkRequest = json.loads(networkRequest)
        message = "default message"
            
        if slots['descriptionType']['value']['originalValue'].lower() == "locations":
            recognizedLocations = intentExplainer.reconizeLocations(networkRequest)
            message = intentExplainer.expressLocations(recognizedLocations)
        elif slots['descriptionType']['value']['originalValue'].lower() == "network limitations":
            recognizedConstraints = intentExplainer.reconizeConstraints(networkRequest)
            message = intentExplainer.expressLimitations(recognizedConstraints)
        else:
            recognizedLocations = intentExplainer.reconizeLocations(networkRequest)
            recognizedConstraints = intentExplainer.reconizeConstraints(networkRequest)
            message = intentExplainer.expressLocations(recognizedLocations)
            message = message + intentExplainer.expressLimitations(recognizedConstraints)
            
        return message
