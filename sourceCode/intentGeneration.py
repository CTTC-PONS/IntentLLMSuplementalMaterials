import json
import jsonTemplates

class intentGeneration():
    
    def reconizeResources(givenOrder):
        resources = ["connectivity service", "connection",
                         "link", "nodes", "port", "bandwidth"]
        recognizedResource = ""
    
        givenOrder = str(givenOrder)
        givenOrder = givenOrder.lower()
    
        for resource in resources:
            if resource in givenOrder:
                recognizedResource = resource
                break
        return recognizedResource

    def reconizeLocations(givenOrder):
        tokenizedOrder = givenOrder
        recognizedLocations = dict()
    
        locations = ["origin", "destination", "domain"]
    
        tokenizedOrder = str(tokenizedOrder)
        tokenizedOrderMayusc = tokenizedOrder.upper()
        tokenizedOrder = tokenizedOrder.lower()
    
        tokenizedOrder = tokenizedOrder.split()
        tokenizedOrderMayusc = tokenizedOrderMayusc.split()
    
        for index, word in enumerate(tokenizedOrder):
            if word in locations:
                recognizedLocations[word] = tokenizedOrderMayusc[index + 1]
            elif word == "port":
                portLocation = list(recognizedLocations)[ -1 ]
                recognizedLocations[ portLocation + word ] = tokenizedOrderMayusc[index + 1]
    
        return recognizedLocations
        
    def recognizeTimes(givenOrder):
        recognizedTimes = dict()
        prevWord = ""
        hourAbbreviations = ["hour", "hours", "hr", "hrs", "h", "hs"]
        minuteAbbreviations = ["minute", "minutes", "min", "mins", "m", "ms"]
        secondAbbreviations = ["second", "seconds", "sec", "secs", "s"]
    
        givenOrder = str(givenOrder)
        givenOrder = givenOrder.lower()
        tokenizedOrder = givenOrder.split()
        prevWord = ""
            
        for index, word in enumerate(tokenizedOrder):
            if str(word) in hourAbbreviations:
                if prevWord.isdigit():
                    recognizedTimes["hours"] = str(prevWord)
            elif str(word) in minuteAbbreviations:
                if prevWord.isdigit():
                    recognizedTimes["minutes"] = str(prevWord)
            elif str(word) in secondAbbreviations:
                if prevWord.isdigit():
                    recognizedTimes["seconds"] = str(prevWord)
    
            prevWord = word
    
        return recognizedTimes
    
        # calculate the total number of seconds based on the extracted units and amounts
    def calculateTotalTimeSeconds(recognizedTimes):
        totalseconds = 0
    
        if len(recognizedTimes) > 0:
            if "hours" in recognizedTimes:
                totalseconds = totalseconds + \
                    int(recognizedTimes["hours"]) * 3600
            if "minutes" in recognizedTimes:
                totalseconds = totalseconds + \
                    int(recognizedTimes["minutes"]) * 60
            if "seconds" in recognizedTimes:
                totalseconds = totalseconds + int(recognizedTimes["seconds"])
    
        return totalseconds
        
    def reconizeOtherRestrictions(givenOrder):
        recognizedLimitations = dict()
    
        givenOrder = str(givenOrder)
        givenOrder = givenOrder.lower()
        tokenizedOrder = givenOrder.split()
    
        #we need to seek for the word bandwidth which it is surrounded by the words low, medium or high
        for i in range(0, len(tokenizedOrder)):
            bandwidths = ["bandwidth", "bw", "band", "frequency", "bandwith"]
                            
            #in the case where the word bandwidth is at the very beginning or at the very end, 
            #we need to asjust the word positions to avoid an error.
            pos1 = i - 2; pos2 = i - 1
                
            if (pos1 < 0):
                pos1 = 0
            if (pos2 < 0):
                pos2 = 0
    
            # Remember to include the comprobations if it is or not at the end or at the beginning of the sentence
            if tokenizedOrder[i] in bandwidths:
                if (tokenizedOrder[pos1] == "low") | (tokenizedOrder[pos2] == "low"):
                    recognizedLimitations["bandwidth"] = "10.0"
                elif (tokenizedOrder[pos1] == "medium") | (tokenizedOrder[pos2] == "medium"):
                    recognizedLimitations["bandwidth"] = "20.0"
                elif (tokenizedOrder[pos1] == "high") | (tokenizedOrder[pos2] == "high"):
                    recognizedLimitations["bandwidth"] = "30.0"
    
        return recognizedLimitations
        
    def recognizeQuality ( givenOrder ):
        recognizedQuality = [("", "", "" ),("", "", "" )]
            
        givenOrder = str(givenOrder)
        givenOrder = givenOrder.lower()
        tokenizedOrder = givenOrder.split()
        
        for i in range (0, len(tokenizedOrder) ):
            bandwidths = ["quality", "qos", "condition", "quality of service", "availability", "capacity" ]
                
            #Remember to include the comprobations if it is or not at the end or at the beginning of the sentence
            if tokenizedOrder[i] in bandwidths:
                    
                pos0 = i - 3; pos1 = i - 2; pos2 = i - 1
                    
                if (pos0 < 0):
                    pos0 = 0
                if (pos1 < 0):
                    pos1 = 0
                if (pos2 < 0):
                    pos2 = 0
                    
                if ( (tokenizedOrder[pos0] == "very") & (tokenizedOrder[pos1] == "low") ) | ( (tokenizedOrder[pos1] == "very") & (tokenizedOrder[pos2] == "low") ):
                    if tokenizedOrder[i] == "availability":
                        recognizedQuality[0] = ("very low", "10.0", "%" )
                    elif tokenizedOrder[i] == "capacity":
                        recognizedQuality[1] = ("very low", "10", "Gbps" )
                    else:
                        recognizedQuality[0] = ("very low", "10.0", "%" )
                        recognizedQuality[1] = ("very low", "10", "Gbps" )
                elif (tokenizedOrder[pos1] == "low") | (tokenizedOrder[pos2] == "low"):
                    if tokenizedOrder[i] == "availability":
                        recognizedQuality[0] = ("low", "30.0", "%" )
                    elif tokenizedOrder[i] == "capacity":
                        recognizedQuality[1] = ("low", "40", "Gbps" )
                    else:
                        recognizedQuality[0] = ("low", "30.0", "%" )
                        recognizedQuality[1] = ("low", "40", "Gbps" )
                elif (tokenizedOrder[pos1] == "medium") | (tokenizedOrder[pos2] == "medium"):
                    if tokenizedOrder[i] == "availability":
                        recognizedQuality[0] = ("medium", "70.0", "%" )
                    elif tokenizedOrder[i] == "capacity":
                        recognizedQuality[1] = ("medium", "50", "Gbps" )
                    else:
                        recognizedQuality[0] = ("medium", "70.0", "%" )
                        recognizedQuality[1] = ("medium", "50", "Gbps" )
                elif (tokenizedOrder[pos1] == "high") | (tokenizedOrder[pos2] == "high"):
                    if tokenizedOrder[i] == "availability":
                        recognizedQuality[0] = ("high", "99.0", "%" )
                    elif tokenizedOrder[i] == "capacity":
                        recognizedQuality[1] = ("high", "100", "Gbps" )
                    else:
                        recognizedQuality[0] = ("high", "99.0", "%" )
                        recognizedQuality[1] = ("high", "100", "Gbps" )
            
        return recognizedQuality
        
    def generateConnectionService(recognizedLocations, totalseconds, recognizedLimitations):
        jsonEndPoints = []
    
        for x in recognizedLocations:
            data = jsonTemplates.jsonTemplates.serviceEndPointsTemplate
            #data = json.load(f)
            
            print("how does data looks like?")
            print(data)
            
            if not x.endswith("port"):
                endPoint = "1/2"
    
                if recognizedLocations.get(x+"port") is not None:
                    endPoint = recognizedLocations[x+"port"]
    
                data['device_id']['device_uuid']['uuid'] = recognizedLocations[x]
                data['endpoint_uuid']['uuid'] = endPoint
    
                jsonEndPoints.append( data )
    
        jsonConstraints = []
        #Secondly, we add the time constraints when we have them
        data = jsonTemplates.jsonTemplates.serviceConstraints
        #data = json.load(f)
    
        if totalseconds > 0:
            data['custom']['constraint_type'] = "time[sec]"
            data['custom']['constraint_value'] = totalseconds
            jsonConstraints.append( data )
    
        for x in recognizedLimitations:
            data = jsonTemplates.jsonTemplates.serviceConstraints
            #data = json.load(f)
    
            data['custom']['constraint_type'] = str(x)
            data['custom']['constraint_value'] = recognizedLimitations[x]
            jsonConstraints.append( data )
    
        f = jsonTemplates.jsonTemplates.serviceTemplate
        f["services"][0]["service_id"]["service_uuid"]["uuid"] = "intent-01"
        f["services"][0]["service_endpoint_ids"] = jsonEndPoints
        f["services"][0]["service_constraints"] = jsonConstraints
    
        return f
