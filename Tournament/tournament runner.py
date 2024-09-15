# Howdy!
# If you're trying to improve my code, I am so very sorry :( 

import json
import random
import math
import os
import pytumblr2
import uuid

# saving credentials for pytumblr2...
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
        #tempNameHolder = tempCounter
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
                print(str(competitorCounter)+". "+dictSection["name"])
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
                            print("1. "+finalOrder[tempCounter - 1])
                            tempCounter = tempCounter + 1
                            response = input("2. "+finalOrder[tempCounter - 1]+"\n3. (skip this matchup)\n")
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
                    # (this option is currently completely nonfunctional... whoops! maybe one day...)
                    #setting up dimensions for image
                    deadspaceWidth = 10
                    verticalCompetitorSpacing = 10
                    horizontalCompetitorSpacing = 5*verticalCompetitorSpacing
                    imageHeight = verticalCompetitorSpacing*totalRounds + 2*deadspaceWidth
                    imageLength = horizontalCompetitorSpacing
                    imageCenterHorizonal = imageLength/2
                    imageCenterVertical = imageHeight/2
                    # setting up a grid where every possible matchup is on...
                    possibleXPositions = [deadspaceWidth]
                    possibleYPositions = [deadspaceWidth]
                    for x in range(1,int(totalRounds)):
                        possibleXPositions.append(deadspaceWidth+(x*horizontalCompetitorSpacing))
                    for x in range(1,competitorQuantity):
                        possibleYPositions.append(deadspaceWidth+(x*verticalCompetitorSpacing))
                    print("and that's all, folks!")
                    print("(no, seriously, this isn't done yet)")
                    break
                case _:
                    print("That's not an option :(")
    except FileNotFoundError:
        print("Well, there isn't a data file...")