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
        break
    except ValueError:
        print
if roundNumber < 0:
    # (the tournament hasn't started yet)
    print("You input a negative number, so we're starting a new competition!")
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
            if competitorQuantity > 2:
                break
            else:
                print("You have to have moe than 2 competitors!")
        except ValueError:
            print("That's not even an integer!")
    powerOf2UpperBound = 1
    while powerOf2UpperBound < competitorQuantity:
        powerOf2LowerBound = powerOf2UpperBound
        powerOf2UpperBound = powerOf2UpperBound*2
    byes = powerOf2UpperBound - competitorQuantity
    match byes:
        case 0:
            print("The amount of competitors is a power of 2, so no byes will be used.")
        case 1:
            print("1 bye will be used!")
        case _:
            print(f"{byes} byes will be used!")
    # adding competitors
    validAnswers = [1,2,3,4,5]
    while True:
        seedingMethod = int(input("By the way... how do you want to seed them?\n1. No Seeding\n2. Random Seeding\n3. Standard Seeding\n4. Cohort Randomized Seeding\n"))
        if seedingMethod in validAnswers:
            break
        else:
            print("That's not an option!")
    tournamentType = "Single Elimination"
    tempCounter = 0
    useCompetitorImages = False
    headerStyle = "none"
    headerText = False
    pollQuestion = "Which competitor deserves to win this competition the most?"
    pollTags = ["tumblr tournament", "poll", "polls"]
    #while True:
    #    response = input("Should there be competitor images in the posted polls? (y/n)\n")
    #    match response:
    #        case "y":
    #            print("OK! Put images in the /images directory of wherever you have this python file!")
    #            useCompetitorImages = True
    #            needsImageDirectory = True
    #            break
    #        case "n":
    #            print("OK! No competitor images will be used!")
    #            useCompetitorImages = False
    #            needsImageDirectory = False
    #            break
    #        case _:
    #            print('Type "y" or "n," please.')
    #while True:
    #    response = input("What Should the header style be?\n1. No header\n2. Text\n3. Image\n")
    #    match response:
    #        case "1":
    #            print("OK! there will be no header!")
    #            headerStyle = "none"
    #            headerText = False
    #            break
    #        case "2":
    #            print("OK!")
    #            headerStyle = "text"
    #            headerText = input("What should the header say?\n")
    #            break
    #        case "3":
    #            print("OK! Put the image you want to use in the /images directory of wherever you have this python file!")
    #            headerStyle = "image"
    #            headerText = False
    #            needsImageDirectory = True
    #            break
    #        case _:
    #            print('Type one of the options, please.')
    print("For best results, put the competitors in order of the highest seed to the lowest seed.")
    propagandaPlaceholder = "(no propaganda submitted)"
    competitorDict = {
        "tournamentSettings": {
            "type": tournamentType,
            "useCompetitorImages": useCompetitorImages,
            "headerStyle": headerStyle,
            "headerText": headerText,
            "defaultPropaganda": propagandaPlaceholder,
            "pollQuestion": pollQuestion,
            "pollTags": pollTags
        }
    }
    while tempCounter < competitorQuantity:
        tempCounter = tempCounter+1
        if useDummyData == True:
            tempNameHolder = str(tempCounter)
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
    for x in range(competitorQuantity):
        seedList.append(x+1)
    # setting up byes
    possibleFakeSeeds = []
    for x in range(powerOf2UpperBound):
        possibleFakeSeeds.append(x+1)
    print("possible fake seeds:", possibleFakeSeeds)
    fakeSeeds = []
    for x in possibleFakeSeeds:
        if x not in seedList:
            fakeSeeds.append(x)
    print("fake seeds:", fakeSeeds)
    if byes == 0:
        safeSeeds = seedList
    else:
        safeSeeds = seedList[0:powerOf2LowerBound]
    print("safe seeds:", safeSeeds)
    unsafeSeeds = []
    for x in seedList:
        if x not in safeSeeds:
            unsafeSeeds.append(x)
    print("unsafe seeds:", unsafeSeeds)
    match seedingMethod:
        case 1:
            #returns order the competitors were put in
            intermediateSeedList = seedList
        case 2:
            #returns the competitors in a random order
            intermediateSeedList = []
            while len(seedList) > 0:
                randomCompetitor = random.choice(seedList)
                seedList.remove(randomCompetitor)
                intermediateSeedList.append(randomCompetitor)
        case 3:
            #implements what I beleive to be standard seeding, where the 1st seed goes against the last seed and the 2nd seed goes against the 2nd lst seed and so on
            constructedSeedList = [1, 2]
            while len(constructedSeedList) < len(possibleFakeSeeds):
                print(constructedSeedList)
                matchupList = []
                for x in constructedSeedList:
                    matchup = [x, 2*len(constructedSeedList)-x+1]
                    matchupList.append(matchup)
                constructedSeedList = []
                for x in range(len(matchupList)):
                    for y in matchupList[x]:
                        constructedSeedList.append(y)
            intermediateSeedList = constructedSeedList
        case 4:
            # Cohort Randomized Seeding
            cohorts ={
                1: []
            }
            if byes == 0:
                amountToSeed = competitorQuantity
            else:
                amountToSeed = powerOf2LowerBound
            cohortAmount = int(math.log2(amountToSeed))
            tempCounter = 0
            while tempCounter < 2:
                cohorts[1].append(possibleFakeSeeds[tempCounter])
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
                    cohortSeedList.append(possibleFakeSeeds[listPos])
                    listPos=listPos+1
                cohorts[tempCounter] = cohortSeedList
            # converting cohorts dict to a list of lists
            cohortList = []
            for x in range(len(cohorts)):
                cohortList.append(cohorts[x+1])
            cohortList2 = cohortList
            print(cohortList)
            print(cohortList2)
            #logic for seeding based on cohorts
            cohortPositions = [1, 1]
            iteration = 0
            while len(cohortPositions) < amountToSeed:
                iteration = iteration+1
                print("Cohort Positions:", cohortPositions)
                cohortMatchupList = []
                for x in cohortPositions:
                    cohortMatchupList.append([x, iteration+1])
                cohortPositions = []
                print("Cohort Matchups:", cohortMatchupList)
                for x in range(len(cohortMatchupList)):
                    for y in cohortMatchupList[x]:
                        cohortPositions.append(y)
            print(cohortPositions)
            intermediateSeedList = []
            seedsToExclude = []
            for x in range(len(cohortPositions)):
                randomCompetitor = random.choice(cohortList[cohortPositions[x]-1])
                intermediateSeedList.append(randomCompetitor)
                cohortList[cohortPositions[x]-1].remove(randomCompetitor)
        case 5:
            #Equal Gap Seeding
            print("nothing here :(")
        case _:
            # catch-all
            print("I haven't done that yet :(")
    # actually assigning byes
    print("intermediate seed list:", intermediateSeedList)
    if byes > 0:
        seedsToNotBye = []
        unsafeSeedIndices = []
        for x in intermediateSeedList:
            if x in unsafeSeeds:
                unsafeSeedIndices.append(intermediateSeedList.index(x))
                seedsToNotBye.append(x)
        print("unsafe indices:", unsafeSeedIndices)
        for x in unsafeSeedIndices:
            if x % 2 == 0:
                # even
                seedsToNotBye.append(intermediateSeedList[x+1])
            else:
                # odd
                seedsToNotBye.append(intermediateSeedList[x-1])
    else:
        seedsToNotBye = []
    print("seeds to not bye:", seedsToNotBye)
    seedsToBye = []
    finalSeedList = []
    for x in intermediateSeedList:
        if x not in fakeSeeds:
            finalSeedList.append(x)
    print("final seed list:", finalSeedList)
    for x in finalSeedList:
        if x not in seedsToNotBye:
            seedsToBye.append(x)
    print("seeds to bye:", seedsToBye)
    # save data to json file
    finalOrder = []
    for x in range(len(finalSeedList)):
            if finalSeedList[x] in seedsToBye:
                startRound = 1
                gotBye = True
            else:
                startRound = 0
                gotBye = False
            dictSection = {
            "position": x+1,
            "seed": finalSeedList[x],
            "lastRound": startRound,
            "gotBye": gotBye,
            "name": competitorNames[int(finalSeedList[x]-1)],
            "propagandaTitle": propagandaTitles[int(finalSeedList[x]-1)],
            "propaganda":[
                propagandaPlaceholder
                ]
            }
            competitorDict["competitor"+str(x+1)] = dictSection
            finalOrder.append(competitorNames[int(finalSeedList[x]-1)])
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
        competitorQuantity = len(competitorList)-1
        totalRounds = int(math.log(competitorQuantity, 2))
        competitionSettings = competitorList["tournamentSettings"]
        competitionType = competitionSettings["type"]
        useCompetitorImages = competitionSettings["useCompetitorImages"]
        headerStyle = competitionSettings["headerStyle"]
        if headerStyle == "text":
            headerText = competitionSettings["headerText"]
        propagandaPlaceholder = competitionSettings["defaultPropaganda"]
        pollQuestion = competitionSettings["pollQuestion"]
        pollTags = competitionSettings["pollTags"]
        
        # finding all the competitors that made it to whatever round and printing a list
        print("Here's all the competitors that made it to round "+str(roundNumber)+":")
        finalOrder = []
        finalOrderPos = []
        finalSeedList = []
        competitorCounter = 0
        while tempCounter < competitorQuantity:
            tempCounter = tempCounter + 1
            dictSection = competitorList["competitor"+str(tempCounter)]
            if dictSection["lastRound"] >= roundNumber:
                if roundNumber == 0:
                    gotBye = dictSection["gotBye"]
                    if gotBye == False:
                        competitorCounter = competitorCounter + 1
                        print(str(competitorCounter)+". "+str(dictSection["name"]))
                        finalOrder.append(dictSection["name"])
                        finalOrderPos.append(dictSection["position"])
                        finalSeedList.append(dictSection["seed"])
                else:
                    competitorCounter = competitorCounter + 1
                    print(str(competitorCounter)+". "+str(dictSection["name"]))
                    finalOrder.append(dictSection["name"])
                    finalOrderPos.append(dictSection["position"])
                    finalSeedList.append(dictSection["seed"])
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
                                "answer_text":str(finalOrder[tempCounter - 1])
                            }
                        ],
                        "settings":{
                            "closed_status": "closed-after",
                            "expire_after": pollTimeLength
                        }
                        }
                        ]
                        pollTags = competitionSettings["pollTags"]
                        pollTags.append(f"round {roundNumber}")
                        pollTags.append(str(finalOrder[tempCounter - 2]))
                        pollTags.append(str(finalOrder[tempCounter - 1]))
                        # there has to be a better way to do this. but it's functional. oh well
                        # this is getting the propaganda
                        contentFormat.append(propagandaHeadingFormat)
                        propagandaCounter = 0
                        blockAmount = blockAmount+len(competitorPropaganda)
                        while propagandaCounter < len(competitorPropaganda):
                            propagandaSection = competitorPropaganda[propagandaCounter]
                            if propagandaSection == propagandaPlaceholder:
                                properganda = propagandaSection
                            else:
                                properganda = f"“{propagandaSection}”"
                            paragraphFormat={
                            "type": "text",
                            "text": properganda,
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
                            if propagandaSection == propagandaPlaceholder:
                                properganda = propagandaSection
                            else:
                                properganda = f"“{propagandaSection}”"
                            paragraphFormat={
                            "type": "text",
                            "text": properganda,
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
                            tags=pollTags,
                            content=contentFormat,
                            layout=postLayout
                        )
                        pollTags.remove(str(finalOrder[tempCounter - 2]))
                        pollTags.remove(str(finalOrder[tempCounter - 1]))
                        print(str(finalOrder[tempCounter - 2])+" vs. "+str(finalOrder[tempCounter - 1])+"\n")
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
                    #setting up dimensions for image
                    centerNodeOffset = int(totalRounds)
                    lengthPerCharacterSize = 8
                    fontSize = int(2.5*lengthPerCharacterSize)
                    lineWidth = 4
                    deadspaceWidth = lineWidth*4
                    pointRadius=int(lineWidth*1.5)
                    verticalCompetitorSpacing = 2*lengthPerCharacterSize
                    if maxNameLength < 5:
                        horizontalCompetitorSpacing = 5*(lengthPerCharacterSize+2)
                    else:
                        horizontalCompetitorSpacing = (lengthPerCharacterSize+2)*maxNameLength
                    imageHeight = (verticalCompetitorSpacing*(competitorQuantity)) + 2*deadspaceWidth
                    imageLength = 4*(horizontalCompetitorSpacing*(int(totalRounds)+1)) + 2*deadspaceWidth
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
                    # defining relevant nodes
                    relevantNodes = {}
                    leftSide = True
                    universalNodeID = 0
                    maxLevel = 1 + int(len(possibleXPositions)/4)
                    for x in range(int(len(possibleXPositions)/2)+1):
                        break
                    # defining "relevant nodes," where each matchup actually happens
                    maxLevel = 1 + int(len(possibleXPositions)/4)
                    levelNodeCounter = []
                    for x in range(maxLevel):
                        levelNodeCounter.append(0)
                    relevantNodes = {}
                    leftSide = True
                    universalNodeID = 0
                    unusedNodes = 0
                    for x in range(int(len(possibleXPositions)/2)+1):
                        layer = int(len(possibleXPositions)/4)-abs(x-int(len(possibleXPositions)/4))
                        if layer == maxLevel:
                            leftSide == False
                        posInLayer = 0
                        nodesToSkip = pow(2, layer)
                        for y in range(int(len(possibleYPositions))):
                            if nodesToSkip == 0:
                                nodeIsRelevant = True
                                if layer == 0:
                                    try:
                                        dictSection = competitorList[f"competitor{y+1}"]
                                        if dictSection['gotBye'] == True:
                                            nodeIsRelevant = False
                                    except KeyError:
                                        nodeIsRelevant = False
                                if nodeIsRelevant == True:
                                    if leftSide == True:
                                        side = "left"
                                    else:
                                        side = "right"
                                    if x == int(len(possibleXPositions)/4):
                                        relevantNodes[universalNodeID] = {
                                            "xPos": 2*x,
                                            "yPos": int(len(possibleYPositions)/2)+centerNodeOffset,
                                            "layer": layer,
                                            "posInLayer": 1,
                                            "side": "middle"
                                        }
                                        svgMarkup += f'<circle cx="{possibleXPositions[2*x]}" cy="{possibleYPositions[int(len(possibleYPositions)/2)+centerNodeOffset]}" r="{pointRadius}" fill="black" />\n'
                                    else:
                                        relevantNodes[universalNodeID] = {
                                            "xPos": 2*x,
                                            "yPos": y,
                                            "layer": layer,
                                            "posInLayer": posInLayer,
                                            "side": side
                                        }
                                    universalNodeID = universalNodeID + 1
                                else:
                                    unusedNodes = unusedNodes+1
                                    relevantNodes[-unusedNodes] = {
                                            "xPos": 2*x,
                                            "yPos": y,
                                            "layer": layer,
                                            "posInLayer": posInLayer,
                                            "side": side
                                        }
                                levelNodeCounter[layer] = levelNodeCounter[layer]+1
                                nodesToSkip = pow(2, layer+1) - 1
                                posInLayer = posInLayer + 1
                            else:
                                nodesToSkip = nodesToSkip - 1
                    # sorting through that ungodly list and returning which nodes are at each layer
                    nodesSortedByLayer = []
                    for x in range(maxLevel):
                        currentLayerNodes = []
                        for y in range(len(relevantNodes)):
                            try:
                                node = relevantNodes[y]
                                if node["layer"] == x:
                                    currentLayerNodes.append(y)
                            except KeyError:
                                print(f"Not including node {y} because it doesn't exist!")
                        nodesSortedByLayer.append(currentLayerNodes)
                    print("nodes by layer:", nodesSortedByLayer)
                    # also getting a nice list of the nodes on each side
                    leftNodes = []
                    rightNodes = []
                    centerNodes = []
                    for x in relevantNodes:
                        node = relevantNodes[x]
                        match node["side"]:
                            case "left":
                                leftNodes.append(x)
                            case "right":
                                rightNodes.append(x)
                            case "middle":
                                centerNodes.append(x)
                            
                    # building the structure of the bracket
                    for x in range(maxLevel):
                        print("Iteration", x+1)
                        currentLayer = nodesSortedByLayer[x]
                        nextLayer = nodesSortedByLayer[x+1]
                        for y in range(len(currentLayer)):
                            currentNodeID = currentLayer[y]
                            currentNode = relevantNodes[currentNodeID]
                            print("current:", currentNode)
                            nextNodeID = nextLayer[math.floor(y/2)]
                            nextNode = relevantNodes[nextNodeID]
                            print("next:", nextNode)
                            svgMarkup += f'<circle cx="{possibleXPositions[currentNode["xPos"]]}" cy="{possibleYPositions[currentNode["yPos"]]}" r="{pointRadius}" fill="black" />\n'
                            print(f"drew a point at relevant node {currentNodeID}!")
                            svgMarkup += f'<path stroke="black" stroke-width="{lineWidth}" fill="none" d="M {possibleXPositions[currentNode["xPos"]]} {possibleYPositions[currentNode["yPos"]]} L {possibleXPositions[int((currentNode["xPos"]+nextNode["xPos"])/2)]} {possibleYPositions[currentNode["yPos"]]} L {possibleXPositions[nextNode["xPos"]]} {possibleYPositions[nextNode["yPos"]]}" />\n'
                            print(f"drew a path between node {currentNodeID} and {nextNodeID}!")

                    #drawing lines for winner's "podium"
                    svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)+centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                    svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)-1]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)+1]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                    # labelling all the universal node IDs
                    #for x in range(int(len(relevantNodes)/2)):
                    #    try:
                    #        node = relevantNodes[x]
                    #        svgMarkup += f'<text x="{possibleXPositions[node["xPos"]]}" y="{possibleYPositions[node["yPos"]-1]+int(fontSize/2)}" fill="red" stroke="red" font-size="{fontSize}">{str(x)}</text>'
                    #        svgMarkup += f'<text x="{possibleXPositions[len(possibleXPositions)-node["xPos"]-1]-horizontalCompetitorSpacing}" y="{possibleYPositions[len(possibleYPositions)-node["yPos"]-2]+int(fontSize/2)}" fill="red" stroke="red" font-size="{fontSize}">{str(len(relevantNodes)-x)}</text>'
                    #    except KeyError:
                    #        print(f"node {x} doesn't exist!")
                    
                    # putting names of competitors in their places
                    for x in range(roundNumber):
                        print(f"Started getting ready for round {x+1}")
                        #getting a list of all nodes in the relevant round
                        currentRoundNodes = []
                        for y in range(universalNodeID):
                            try:
                                node = relevantNodes[y]
                                if node["layer"] == x:
                                    currentRoundNodes.append(y)
                            except KeyError:
                                print(f"node {y} doesn't exist!")
                        print("Relevant nodes of the current round", len(currentRoundNodes), currentRoundNodes)
                        # getting a list of all competitors in the current round
                        currentRoundCompetitorNames = []
                        for y in range(len(competitorList)-1):
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
