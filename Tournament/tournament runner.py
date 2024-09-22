# Howdy!
# If you're trying to improve my code, I am so very sorry :(

useDummyData = True

import json
import random
import math
import os
try:
    import pytumblr2
    pytumblr2Installed = True
except ModuleNotFoundError:
    print("You don't have pytumblr2 installed!")
    pytumblr2Installed = False
import uuid

# saving credentials for pytumblr2...
if pytumblr2Installed == False:
    print("Skipping saving Tumblr credentials, because you don't have pytumblr2 installed!")
else:
    try:
        x = open("credentials.json","x")
        x.close()
        while True:
            response = input("Do you have valid credentials for accessing the Tumblr API? (y/n)\n")
            match response:
                case "y":
                    validTumblrCredentials = True
                    print("OK! (You probably want to copy/paste these)")
                    consumerKey=input("What is your consumer key?\n")
                    consumerSecret=input("What is your consumer secret?\n")
                    oauthToken=input("What is your oauth token?\n")
                    oauthSecret=input("What is your oauth secret?\n")
                    postedBlog=input("Now... what is the url of the blog are these polls goint to be posted to?\n")
                    clientInfo = {
                        "hasCredentials": validTumblrCredentials,
                        "consumerKey": consumerKey,
                        "consumerSecret": consumerSecret,
                        "oauthToken": oauthToken,
                        "oauthSecret": oauthSecret,
                        "postedBlog": postedBlog
                    }
                    break
                case "n":
                    validTumblrCredentials = False
                    print("OK! You won't be able to post polls... obviously.")
                    clientInfo = {
                        "hasCredentials": validTumblrCredentials
                    }
                    break
                case _:
                    print("Type \"y\" or \"n\" please")
        # dunno how I feel about storing this stuff in plaintext... but it's not like there's anything else I can really do
        with open("credentials.json", "w") as f:
            json.dump(clientInfo, f)
    except FileExistsError:
        # loading saved credentials file
        print("Using saved credentials...")
        r = open("credentials.json")
        clientInfo = json.load(r)
        validTumblrCredentials = clientInfo["hasCredentials"]
        if validTumblrCredentials == True:
            consumerKey=clientInfo["consumerKey"]
            consumerSecret=clientInfo["consumerSecret"]
            oauthToken=clientInfo["oauthToken"]
            oauthSecret=clientInfo["oauthSecret"]
            postedBlog=clientInfo["postedBlog"]
            client = pytumblr2.TumblrRestClient(
                consumerKey,
                consumerSecret,
                oauthToken,
                oauthSecret
            )
            client.info()

competitorQuantity = 0
competitorNames = []
propagandaTitles = []
while True:
    # getting what round it is
    try:
        roundNumber = int(input("What round is is it?\n"))
        if roundNumber >= 0:
            break
        else:
            print("You can't have a negative round!")
    except ValueError:
        print
if roundNumber == 0:
    # (the tournament hasn't started yet)
    while True:
        # Creating the data file
        try:
            f = open("tourny_data.json","x")
            break
        except FileExistsError:
            print("There's already a file there...")
            response = input("Delete it? (y/n)")
            if response == "y":
                print("Deleting it...")
                os.remove("tourny_data.json")
    while True:
        # (getting how many competitors there are)
        try:
            competitorQuantity = int(input("How many competitors are there?\n"))
        except ValueError:
            print("That's not even an integer!")
            while True:
                try:
                    competitorQuantity = int(input("How many competitors are there?\n"))
                    break
                except ValueError:
                    print("Again, that's not even an integer.")
        if competitorQuantity >= 0:
            totalRounds = math.log(competitorQuantity, 2)
            if totalRounds.is_integer() == True:
                break
            else:
                print("The amount of competitiors has to be a power of 2.")
        else:
            print("There can't be 0 or fewer competitors.")
    # adding competitors
    validAnswers = [1,2,3,4,5]
    while True:
        seedingMethod = int(input("By the way... how do you want to seed them?\n1. No Seeding\n2. Random Seeding\n3. Standard Seeding\n4. Cohort Randomized Seeding\n"))
        if seedingMethod in validAnswers:
            break
        else:
            print("That's not an option!")
    tempCounter = 0
    print("For best results, put the competitors in order of the highest seed to the lowest seed.")
    competitorDict = dict({})
    while tempCounter < competitorQuantity:
        tempCounter = tempCounter+1
        if useDummyData == True:
            tempNameHolder = tempCounter
        else:
            tempNameHolder = input("What is the name of competitor "+str(tempCounter)+"?\n")
        competitorNames.append(tempNameHolder)
        tempPropagandaTitle = tempNameHolder
        #while True:
        #    response = str(input("Should the title above the relevant propaganda be different? (y/n)\n"))
        #    match response:
        #        case "n":
        #            tempPropagandaTitle = tempNameHolder
        #            break
        #        case "y":
        #            tempPropagandaTitle = input("What should "+tempNameHolder+"'s title be?")
        #            break
        #        case _:
        #            print("Type \"y\" or \"n\" please.")
        propagandaTitles.append(tempPropagandaTitle)
    listPos = 0
    seedList = []
    tempCounter = 0
    while tempCounter < competitorQuantity:
        tempCounter = tempCounter + 1
        seedList.append(tempCounter)
    match seedingMethod:
        case 1:
            #returns order the competitors were put in
            while listPos < competitorQuantity:
              listPos = listPos+1
              dictSection = {
                "position": listPos,
                "seed": listPos,
                "lastRound": 1,
                "name": competitorNames[listPos-1],
                "propagandaTitle": propagandaTitles[listPos-1],
                "propaganda":[
                    "(no propaganda submitted)"
                    ]
                }
              competitorDict["competitor"+str(listPos)] = dictSection
            finalOrder=competitorNames
        case 2:
            #returns the competitors in a random order
            finalSeedList = []
            finalOrder = []
            while len(seedList) > 0:
                randomCompetitor = random.choice(seedList)
                seedList.remove(randomCompetitor)
                finalSeedList.append(randomCompetitor)
            while listPos < competitorQuantity:
                listPos = listPos+1
                finalOrder.append([int(finalSeedList[listPos-1])])
                dictSection = {
                "position": listPos,
                "seed": finalSeedList[listPos-1],
                "lastRound": 1,
                "name": competitorNames[int(finalSeedList[listPos-1]-1)],
                "propagandaTitle": propagandaTitles[int(finalSeedList[listPos-1]-1)],
                "propaganda":[
                    "(no propaganda submitted)"
                    ]
                }
                competitorDict["competitor"+str(listPos)] = dictSection
        case 3:
            #implements what I beleive to be standard seeding, where the 1st seed goes against the last seed and the 2nd seed goes against the 2nd lst seed and so on
            constructedSeedList = [1, 2]
            while len(constructedSeedList) < len(seedList):
                print(constructedSeedList)
                matchupList = []
                for x in constructedSeedList:
                    matchup = [x, 2*len(constructedSeedList)-x+1]
                    matchupList.append(matchup)
                constructedSeedList = []
                for x in range(len(matchupList)):
                    for y in matchupList[x]:
                        constructedSeedList.append(y)
            finalSeedList = constructedSeedList
            finalOrder = []
            for x in range(len(finalSeedList)):
                finalOrder.append(competitorNames[int(finalSeedList[x]-1)])
                dictSection = {
                "position": x+1,
                "seed": finalSeedList[x],
                "lastRound": 1,
                "name": competitorNames[int(finalSeedList[x]-1)],
                "propagandaTitle": propagandaTitles[int(finalSeedList[x]-1)],
                "propaganda":[
                    "(no propaganda submitted)"
                    ]
                }
                competitorDict["competitor"+str(x+1)] = dictSection

        case 4:
            # Randomised cohort seeding
            # Sets up cohort 1
            cohorts ={
                "cohort1": []
            }
            cohortAmount = int(math.log2(competitorQuantity))
            tempCounter = 0
            while tempCounter < 2:
                cohorts["cohort1"].append(seedList[tempCounter])
                tempCounter = tempCounter + 1
            tempCounter = 1
            listPos = 2
            # dynamically creates cohorts based on number of competitors
            while tempCounter < cohortAmount:
                cohortSize = pow(2, tempCounter)
                tempCounter = tempCounter + 1
                cohortSeedList=[]
                cohortCounter = 0
                while cohortCounter < cohortSize:
                    cohortCounter = cohortCounter + 1
                    cohortSeedList.append(seedList[listPos])
                    listPos=listPos+1
                cohorts["cohort"+str(tempCounter)] = cohortSeedList
            print(str(cohorts))
            #logic for seeding based on cohorts
            availablePositions = []
            cohortPosition = []
            tempCounter = 0
            while tempCounter < competitorQuantity:
                tempCounter = tempCounter + 1
                availablePositions.append(tempCounter)
                cohortPosition.append(-1)
            tempCounter = len(cohorts)
            while len(availablePositions) > 4:
                # for each cohort over cohort 2
                useThisPosition = False
                cohortCounter = 0
                while True:
                    try:
                        print(cohortCounter, useThisPosition)
                        if useThisPosition == True:
                            useThisPosition = False
                            cohortPosition[availablePositions[cohortCounter]-1] = "cohort"+str(tempCounter)
                            availablePositions[cohortCounter] = -1
                        else:
                            useThisPosition = True
                        cohortCounter = cohortCounter + 1
                    except IndexError:
                        break
                removalcount = 0
                while True:
                    print("Removed "+str(removalcount)+" occupied positions!")
                    if -1 in availablePositions:
                        removalcount = removalcount + 1
                        availablePositions.remove(-1)
                    else:
                        break
                print("Finished assigning positions to cohort"+str(tempCounter))
                tempCounter = tempCounter - 1
                print(availablePositions)
                print(cohortPosition)
            # for cohorts 1 and 2
            cohortPosition[availablePositions[0]-1] = "cohort1"
            cohortPosition[availablePositions[1]-1] = "cohort2"
            cohortPosition[availablePositions[2]-1] = "cohort1"
            cohortPosition[availablePositions[3]-1] = "cohort2"
            print(availablePositions)
            print(cohortPosition)
            # creating the final order
            finalSeedList = []
            finalOrder = []
            tempCounter = 0
            for x in range(len(cohortPosition)):
                randomCohortMember = random.choice(cohorts[str(cohortPosition[x])])
                cohorts[cohortPosition[x]].remove(randomCohortMember)
                finalSeedList.append(randomCohortMember)
                finalOrder.append(competitorNames[int(randomCohortMember-1)])
            for x in range(len(finalSeedList)):
                dictSection = {
                "position": x+1,
                "seed": finalSeedList[x],
                "lastRound": 1,
                "name": competitorNames[int(finalSeedList[x]-1)],
                "propagandaTitle": propagandaTitles[int(finalSeedList[x]-1)],
                "propaganda":[
                    "(no propaganda submitted)"
                    ]
                }
                competitorDict["competitor"+str(x+1)] = dictSection
        case _:
            # catch-all
            print("I haven't done that yet :(")
    # save data to json file
    competitorList = json.dumps(competitorDict, indent=2)
    f = open("tourny_data.json", "w")
    f.write(competitorList+"\n")
    f.close()
    tempCounter = 0
    while tempCounter < competitorQuantity:
        tempCounter = tempCounter + 1
        print(str(tempCounter)+". "+ str(finalOrder[tempCounter - 1]))
else:
    # if tournament has started
    try:
        tempCounter = 0
        f = open("tourny_data.json")
        competitorList = json.load(f)
        f.close()
        # (getting how many competitors there are)
        competitorQuantity = len(competitorList)
        totalRounds = math.log(competitorQuantity, 2)
        print("Here's all the competitors that made it to round "+str(roundNumber)+":")
        # finding all the competitors that made it to whatever round and printing a list
        finalOrder = []
        finalOrderPos = []
        competitorCounter = 0
        while tempCounter < competitorQuantity:
            tempCounter = tempCounter + 1
            dictSection = competitorList["competitor"+str(tempCounter)]
            if dictSection["lastRound"] >= roundNumber:
                competitorCounter = competitorCounter + 1
                print(str(competitorCounter)+". "+str(dictSection["name"]))
                finalOrder.append(dictSection["name"])
                finalOrderPos.append(dictSection["position"])
        currentRoundCompetitorQuantity = len(finalOrder)
        # What comes after competitors are found
        while True:
            response = str(input("1. Post polls for these competitors\n2. Record results of this round\n3. Render chart for this round\n"))
            match response:
                case "1":
                    # posting polls for existing matchup
                    while True:
                        try:
                            pollTimeLength = int(input("How many seconds should the polls run for?\n604800 (7 days) is the max value and 86400 (1 day) is the minimum\n"))
                            break
                        except ValueError:
                            print("That isn't a valid answer!")
                    while True:
                        response = input("Do you want to post all of them? (y/n)\n")
                        match response:
                            case "y":
                                tempCounter = 0
                                finalCompetitorPosted = currentRoundCompetitorQuantity-1
                                break
                            case "n":
                                while True:
                                    try:
                                    
                                        tempCounter = 2*(int(input("Which poll should the first one posted? (1 is the first poll of this set)"))-1)
                                        break
                                    except ValueError:
                                        print("That isn't a valid number!")
                                while True:
                                    try:
                                        finalCompetitorPosted = 2*(int(input("Which poll should be the LAST one posted? ("+str(int(currentRoundCompetitorQuantity/2))+" is the last poll of this set)"))-1)
                                        if finalCompetitorPosted < tempCounter:
                                            print("Silly Billy! You can't have the last competitor be before the first one!")
                                        else:
                                            break
                                    except ValueError:
                                        print("Uh oh!")
                                break
                            case _:
                                print("That's not a valid response!")
                    validAnswers = ["published","draft","queue"]
                    while True:
                        postMethod = str(input("Should these posts be published, put in the drafts, or put in the queue?\n"))
                        if postMethod in validAnswers:
                            print("OK!")
                            break
                        else:
                            print("Type either \"published\", \"draft\", or \"queue\", please.")
                    #prepares the format of polls to be posted
                    pollQuestion = "Which competitor deserves to win round "+str(roundNumber)+" the most?"
                    while tempCounter <= finalCompetitorPosted:
                        blockAmount = 3
                        tempCounter = tempCounter+2
                        dictSection = competitorList["competitor"+str(finalOrderPos[tempCounter-2])]
                        competitorPropagandaTitle = dictSection["propagandaTitle"]
                        competitorPropaganda = dictSection["propaganda"]
                        propagandaHeadingFormat={
                            "type": "text",
                            "text": competitorPropagandaTitle,
                            "subtype": "heading1"
                        }
                        contentFormat = [
                            {
                                "type":"poll",
                                "question": pollQuestion,
                                "client_id": str(uuid.uuid4()),
                                "answers":[
                            {
                                "answer_text":str(finalOrder[tempCounter - 2])
                            },
                            {
                                "answer_text":finalOrder[tempCounter - 1]
                            }
                        ],
                        "settings":{
                            "closed_status": "closed-after",
                            "expire_after": pollTimeLength
                        }
                        }
                        ]
                        # there has to be a better way to do this. but it's functional. oh well
                        # this is getting the propaganda
                        contentFormat.append(propagandaHeadingFormat)
                        propagandaCounter = 0
                        blockAmount = blockAmount+len(competitorPropaganda)
                        while propagandaCounter < len(competitorPropaganda):
                            propagandaSection = competitorPropaganda[propagandaCounter]
                            paragraphFormat={
                            "type": "text",
                            "text": propagandaSection,
                            }
                            contentFormat.append(paragraphFormat),
                            propagandaCounter = propagandaCounter + 1
                        dictSection = competitorList["competitor"+str(finalOrderPos[tempCounter-1])]
                        competitorPropagandaTitle = dictSection["propagandaTitle"]
                        competitorPropaganda = dictSection["propaganda"]
                        propagandaHeadingFormat={
                            "type": "text",
                            "text": competitorPropagandaTitle,
                            "subtype": "heading1"
                        }
                        contentFormat.append(propagandaHeadingFormat)
                        propagandaCounter = 0
                        blockAmount = blockAmount+len(competitorPropaganda)
                        while propagandaCounter < len(competitorPropaganda):
                            propagandaSection = competitorPropaganda[propagandaCounter]
                            paragraphFormat={
                            "type": "text",
                            "text": propagandaSection,
                            }
                            contentFormat.append(paragraphFormat),
                            propagandaCounter = propagandaCounter + 1
                        blockCounter = 0
                        postLayout = [
                            {
                                "type": "rows",
                                "display":[],
                                "truncate_after": 0
                            }
                        ]
                        while blockCounter < blockAmount:
                            blockSection = {
                                "blocks":[blockCounter]
                            }
                            layoutBlock = postLayout[0]
                            blockBlock=layoutBlock["display"]
                            blockBlock.append(blockSection)
                            blockCounter = blockCounter+1
                        #creates each poll
                        client.create_post(
                            blogname=clientInfo["postedBlog"],
                            state = postMethod,
                            tags=["round "+str(roundNumber), "tumblr tournament", "polls"],
                            content=contentFormat,
                            layout=postLayout
                        )
                        print(finalOrder[tempCounter - 2]+" vs. "+finalOrder[tempCounter - 1]+"\n")
                    break
                case "2":
                    # updating matchup
                    print("OK! just type the number next to the WINNING competitor!")
                    tempCounter = 0
                    while tempCounter < currentRoundCompetitorQuantity:
                        while True:
                            tempCounter = tempCounter + 1
                            print("1. "+str(finalOrder[tempCounter - 1]))
                            tempCounter = tempCounter + 1
                            response = input("2. "+str(finalOrder[tempCounter - 1])+"\n3. (skip this matchup)\n")
                            match response:
                                case "1":
                                    #moving selected competitor to next round
                                    dictSection = competitorList["competitor"+str(finalOrderPos[tempCounter-2])]
                                    dictSection["lastRound"] = roundNumber + 1
                                    competitorList["competitor"+str(finalOrderPos[tempCounter-2])] = dictSection
                                    #setting losing competitor to current round (just in case)
                                    dictSection = competitorList["competitor"+str(finalOrderPos[tempCounter-1])]
                                    dictSection["lastRound"] = roundNumber
                                    competitorList["competitor"+str(finalOrderPos[tempCounter-1])] = dictSection
                                    break
                                case "2":
                                    #moving selected competitor to next round
                                    dictSection = competitorList["competitor"+str(finalOrderPos[tempCounter-1])]
                                    dictSection["lastRound"] = roundNumber + 1
                                    competitorList["competitor"+str(finalOrderPos[tempCounter-1])] = dictSection
                                    #setting losing competitor to current round (just in case)
                                    dictSection = competitorList["competitor"+str(finalOrderPos[tempCounter-2])]
                                    dictSection["lastRound"] = roundNumber
                                    competitorList["competitor"+str(finalOrderPos[tempCounter-2])] = dictSection
                                    break
                                case "3":
                                    break
                                case _:
                                    print("no.")
                        competitorDict = json.dumps(competitorList, indent=2)
                        f = open("tourny_data.json", "w")
                        f.write(competitorDict)
                    break
                case "3":
                    # finding the longest name and getting a list of all the competitors in the competition
                    firstRoundCompetitors = []
                    maxNameLength = 0
                    for x in range(1, competitorQuantity+1):
                        dictSection = competitorList["competitor"+str(x)]
                        firstRoundCompetitors.append(dictSection["name"])
                        if len(str(dictSection["name"])) > maxNameLength:
                            maxNameLength = len(str(dictSection["name"]))
                    print(firstRoundCompetitors)
                    print(maxNameLength)
                    #setting up dimensions for image
                    centerNodeOffset = int(totalRounds)
                    lengthPerCharacterSize = 10
                    fontSize = int(2*lengthPerCharacterSize)
                    lineWidth = 5
                    deadspaceWidth = lineWidth*4
                    pointRadius=lineWidth*2
                    verticalCompetitorSpacing = 2*lengthPerCharacterSize
                    if maxNameLength < 5:
                        horizontalCompetitorSpacing = 5*(lengthPerCharacterSize+2)
                    else:
                        horizontalCompetitorSpacing = (lengthPerCharacterSize+2)*maxNameLength
                    imageHeight = (verticalCompetitorSpacing*(competitorQuantity)) + 2*deadspaceWidth
                    imageLength = 4*(horizontalCompetitorSpacing*(int(totalRounds))) + 2*deadspaceWidth
                    # setting up a grid where every possible matchup is on...
                    possibleXPositions = [deadspaceWidth]
                    possibleYPositions = [deadspaceWidth]
                    for x in range(1,(4*int(totalRounds))+1):
                        possibleXPositions.append(deadspaceWidth+(x*horizontalCompetitorSpacing))
                    for x in range(1,int((competitorQuantity))+1):
                        possibleYPositions.append(deadspaceWidth+(x*verticalCompetitorSpacing))
                    imageCenterVertical = possibleYPositions[int(len(possibleYPositions)/2)]
                    imageCenterHorizontal = possibleXPositions[int(len(possibleXPositions)/2)]
                    svgMarkup =f'<svg width="{imageLength}" height="{imageHeight}" xmlns="http://www.w3.org/2000/svg">\n<rect width="{imageLength}" height="{imageHeight}" x="0" y ="0" fill="white" />'
                    # for reference. puts a dot at every single "possible position"
                    #for x in possibleXPositions:
                    #    for y in possibleYPositions:
                    #        svgMarkup += f'<circle cx="{x}" cy="{y}" r="5" fill="red" />\n'
                    # defining "relevant nodes," where each matchup actually happens
                    maxLevel = 1 + int(len(possibleXPositions)/4)
                    levelNodeCounter = []
                    for x in range(maxLevel):
                        levelNodeCounter.append(0)
                    relevantNodes = {}
                    universalNodeID = 0
                    for x in range(int(len(possibleXPositions)/2)+1):
                        layer = int(len(possibleXPositions)/4)-abs(x-int(len(possibleXPositions)/4))
                        nodesToSkip = pow(2, layer)
                        for y in range(int(len(possibleYPositions))):
                            if nodesToSkip == 0:
                                if x == int(len(possibleXPositions)/4):
                                    relevantNodes[universalNodeID] = {
                                        "xPos": 2*x,
                                        "yPos": int(len(possibleYPositions)/2)+centerNodeOffset,
                                        "layer": layer,
                                        "posInLayer": levelNodeCounter[layer]
                                    }
                                else:
                                    relevantNodes[universalNodeID] = {
                                        "xPos": 2*x,
                                        "yPos": y,
                                        "layer": layer,
                                        "posInLayer": levelNodeCounter[layer]
                                    }
                                universalNodeID = universalNodeID + 1
                                levelNodeCounter[layer] = levelNodeCounter[layer]+1
                                nodesToSkip = pow(2, layer+1) - 1
                            else:
                                nodesToSkip = nodesToSkip - 1
                    # putting dots on relevant bits
                    for x in range(len(relevantNodes)):
                        node = relevantNodes[x]
                        svgMarkup += f'<circle cx="{possibleXPositions[node["xPos"]]}" cy="{possibleYPositions[node["yPos"]]}" r="{pointRadius}" fill="black" />\n'
                    # sorting through that ungodly list and returning which nodes are at each layer
                    nodesSortedByLayer = []
                    for x in range(maxLevel):
                        currentLayerNodes = []
                        for y in range(len(relevantNodes)):
                            node = relevantNodes[y]
                            if node["layer"] == x:
                                currentLayerNodes.append(y)
                        nodesSortedByLayer.append(currentLayerNodes)
                    # building the structure of the bracket
                    for x in range(maxLevel-1):
                        nextLayer = nodesSortedByLayer[x+1]
                        currentLayerNodes = nodesSortedByLayer[x]
                        leftNodes = currentLayerNodes[0:int(len(currentLayerNodes)/2)]
                        for y in range(len(leftNodes)):
                            currentNode = relevantNodes[leftNodes[y]]
                            if len(currentLayerNodes) > 2:
                                nextNode = relevantNodes[nextLayer[math.floor(y/2)]]
                            else:
                                nextNode = relevantNodes[competitorQuantity -1]
                            svgMarkup += f'<line x1="{possibleXPositions[currentNode["xPos"]]}" y1="{possibleYPositions[currentNode["yPos"]]}" x2="{possibleXPositions[currentNode["xPos"]+1]}" y2="{possibleYPositions[currentNode["yPos"]]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                            svgMarkup += f'<line x1="{possibleXPositions[currentNode["xPos"]+1]}" y1="{possibleYPositions[currentNode["yPos"]]}" x2="{possibleXPositions[nextNode["xPos"]]}" y2="{possibleYPositions[nextNode["yPos"]]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                        rightNodes = currentLayerNodes[int(len(currentLayerNodes)/2):len(currentLayerNodes)]
                        for y in range(len(rightNodes)):
                            currentNode = relevantNodes[rightNodes[y]]
                            if len(currentLayerNodes) > 2:
                                nextNode = relevantNodes[nextLayer[math.floor((y+len(leftNodes))/2)]]
                            else:
                                nextNode = relevantNodes[competitorQuantity-1]
                            svgMarkup += f'<line x1="{possibleXPositions[currentNode["xPos"]]}" y1="{possibleYPositions[currentNode["yPos"]]}" x2="{possibleXPositions[currentNode["xPos"]-1]}" y2="{possibleYPositions[currentNode["yPos"]]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                            svgMarkup += f'<line x1="{possibleXPositions[currentNode["xPos"]-1]}" y1="{possibleYPositions[currentNode["yPos"]]}" x2="{possibleXPositions[nextNode["xPos"]]}" y2="{possibleYPositions[nextNode["yPos"]]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                    #drawing lines for winner's "podium"
                    svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)+centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                    svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)-1]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)+1]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                    # labelling all the universal node IDs
                    #for x in range(int(len(relevantNodes)/2)):
                    #    node = relevantNodes[x]
                    #    svgMarkup += f'<text x="{possibleXPositions[node["xPos"]]}" y="{possibleYPositions[node["yPos"]-1]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{str(x)}</text>'
                    #    svgMarkup += f'<text x="{possibleXPositions[len(possibleXPositions)-node["xPos"]-1]-horizontalCompetitorSpacing}" y="{possibleYPositions[len(possibleYPositions)-node["yPos"]-2]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{str(len(relevantNodes)-x)}</text>'
                    
                    # putting names of competitors in their places
                    for x in range(roundNumber):
                        print(f"Started getting ready for round {x+1}")
                        #getting a list of all nodes in the relevant round
                        currentRoundNodes = []
                        for y in range(universalNodeID):
                            node = relevantNodes[y]
                            if node["layer"] == x:
                                currentRoundNodes.append(y)
                        print("Relevant nodes of the current round", len(currentRoundNodes), currentRoundNodes)
                        # getting a list of all competitors in the current round
                        currentRoundCompetitorNames = []
                        for y in range(len(competitorList)):
                            competitor = competitorList["competitor"+str(y+1)]
                            if competitor["lastRound"] >= x+1:
                                currentRoundCompetitorNames.append(competitor["name"])
                        print("Relevant competitors in the current round", len(currentRoundCompetitorNames), currentRoundCompetitorNames)
                        # putting the competitors' names on the bracket
                        for y in range(int(len(currentRoundNodes)/2)):
                            currentNode = currentRoundNodes[y]
                            node = relevantNodes[currentNode]
                            svgMarkup += f'<text x="{possibleXPositions[node["xPos"]]+pointRadius}" y="{possibleYPositions[node["yPos"]-1]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{str(currentRoundCompetitorNames[y])}</text>\n'
                            svgMarkup += f'<text x="{possibleXPositions[len(possibleXPositions)-node["xPos"]-1]-horizontalCompetitorSpacing}" y="{possibleYPositions[len(possibleYPositions)-node["yPos"]-2]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{str(currentRoundCompetitorNames[len(currentRoundCompetitorNames)-y-1])}</text>\n'
                    # checking if there is a victor
                    if roundNumber > int(totalRounds):
                        competitionVictor = finalOrder[0]
                        svgMarkup += f'<text x="{possibleXPositions[int(len(possibleXPositions)/2)]}" y="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset-1]+lineWidth}" fill="black" stroke="black" text-anchor="middle" font-size="{2*fontSize}">{str(competitionVictor)}</text>\n'
                    #closing the SVG file and saving it
                    svgMarkup += '</svg>'
                    try:
                        f = open("bracket.svg", "x")
                    except FileExistsError:
                        os.remove("bracket.svg")
                        f = open("bracket.svg", "x")
                    w = open("bracket.svg", "w")
                    w.write(str(svgMarkup))
                    w.close()
                    print('Saved bracket image to "bracket.svg"')
                    break
                case _:
                    print("That's not an option :(")
    except FileNotFoundError:
        print("Well, there isn't a data file...")