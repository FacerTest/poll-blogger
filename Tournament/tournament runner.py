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
                print("You have to have more than 2 competitors!")
        except ValueError:
            print("That's not even an integer!")
    powerOf2UpperBound = 1
    while powerOf2UpperBound < competitorQuantity:
        powerOf2LowerBound = powerOf2UpperBound
        powerOf2UpperBound = powerOf2UpperBound*2
    byesButBad = powerOf2UpperBound - competitorQuantity
    if byesButBad == 0:
        byes = competitorQuantity
    else:
        byes = byesButBad
    match byes:
        case 0:
            print("The amount of competitors is a power of 2, so all of them will get byed from round 0.")
        case 1:
            print("1 bye will be used for round 0!")
        case _:
            print(f"{byes} byes will be used for round 0!")
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
    propagandaPlaceholder = "(no propaganda submitted)"
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
    seedList = []
    for x in range(competitorQuantity):
        seedList.append(x+1)
    # setting up byes
    possibleFakeSeeds = []
    if byes == 0:
        possibleFakeSeedQuantity = competitorQuantity*2
    else:
        possibleFakeSeedQuantity = powerOf2UpperBound
    for x in range(possibleFakeSeedQuantity):
        possibleFakeSeeds.append(x+1)
    print("possible fake seeds:", possibleFakeSeeds)
    fakeSeeds = []
    for x in possibleFakeSeeds:
        if x not in seedList:
            fakeSeeds.append(x)
    print("fake seeds:", fakeSeeds)
    if byes == competitorQuantity:
        safeSeeds = seedList
    else:
        safeSeeds = seedList[0:powerOf2LowerBound]
    print("safe seeds:", safeSeeds)
    unsafeSeeds = []
    for x in seedList:
        if x not in safeSeeds:
            unsafeSeeds.append(x)
    print("unsafe seeds:", unsafeSeeds)
    print(byes, len(unsafeSeeds)*2)
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
    match seedingMethod:
        case 1:
            #returns order the competitors were put in
            unsafeSeedingMethod = "Insert After"
            intermediateSeedList = possibleFakeSeeds
        case 2:
            #returns the competitors in a random order
            unsafeSeedingMethod = "Random"
            intermediateSeedList = []
            seedsToAssign = possibleFakeSeeds
            while len(seedsToAssign) > 0:
                randomCompetitor = random.choice(seedsToAssign)
                seedsToAssign.remove(randomCompetitor)
                intermediateSeedList.append(randomCompetitor)
        case 3:
            #implements what I beleive to be standard seeding, where the 1st seed goes against the last seed and the 2nd seed goes against the 2nd lst seed and so on
            unsafeSeedingMethod = "Highest Safe to Lowest Unsafe"
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
            unsafeSeedingMethod = "To Lowest Cohort"
            cohorts ={
                1: []
            }
            cohortAmount = int(math.log2(len(possibleFakeSeeds)))
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
            seedCohorts = cohorts
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
            while len(cohortPositions) < powerOf2UpperBound:
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
    if byes != competitorQuantity:
        # positioning unsafe seeds intelligently
        finalSeedList = intermediateSeedList
        for x in intermediateSeedList:
            if x in fakeSeeds:
                finalSeedList.remove(x)
        seedsToNotBye = []
        for x in unsafeSeeds:
            seedsToNotBye.append(x)
        unsafeSeedListPos = 0
        while len(seedsToNotBye) < competitorQuantity-byes:
            unsafeSeedToFind = unsafeSeeds[unsafeSeedListPos]
            print(f"finding location of seed {unsafeSeedToFind}")
            safeSeedCollateral = finalSeedList.index(unsafeSeedToFind)-1
            safeSeedToNotBye = finalSeedList[safeSeedCollateral]
            print(f"seed {unsafeSeedToFind} is in a matchup with {safeSeedToNotBye}.")
            unsafeSeedListPos = unsafeSeedListPos - 1
            seedsToNotBye.append(finalSeedList[safeSeedCollateral])
        print("seeds to not bye:", seedsToNotBye)
        seedsToBye = []
        for x in seedList:
            if x not in seedsToNotBye:
                seedsToBye.append(x)
        print("seeds to bye:", seedsToBye)
    else:
        seedsToBye = []
        finalSeedList = intermediateSeedList
        currentRoundMatchupList = []
        for x in range(int(competitorQuantity/2)):
            matchup = []
            for y in range(2):
                matchup.append(finalSeedList[(2*x)+y])
            currentRoundMatchupList.append(matchup)
        print("Matchps:", currentRoundMatchupList)
    # saving various competition info
    competitorDict = {
        "tournamentInfo": {
            "type": tournamentType,
            "useCompetitorImages": useCompetitorImages,
            "headerStyle": headerStyle,
            "headerText": headerText,
            "defaultPropaganda": propagandaPlaceholder,
            "pollQuestion": pollQuestion,
            "pollTags": pollTags,
            "byedSeeds": seedsToBye
        }
    }
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
        competitionSettings = competitorList["tournamentInfo"]
        competitionType = competitionSettings["type"]
        useCompetitorImages = competitionSettings["useCompetitorImages"]
        headerStyle = competitionSettings["headerStyle"]
        if headerStyle == "text":
            headerText = competitionSettings["headerText"]
        propagandaPlaceholder = competitionSettings["defaultPropaganda"]
        pollQuestion = competitionSettings["pollQuestion"]
        pollTags = competitionSettings["pollTags"]
        # Finding some more information
        powerOf2UpperBound = 1
        while powerOf2UpperBound < competitorQuantity:
            powerOf2LowerBound = powerOf2UpperBound
            powerOf2UpperBound = powerOf2UpperBound * 2
        # finding all the competitors that made it to whatever round and printing a list
        finalOrder = []
        finalOrderPos = []
        finalSeedList = []
        originalSeedList = []
        originalNameList = []
        round0Positions = []
        competitorCounter = 0
        notByed = []
        byes = 0
        # finding bye info
        for x in range(powerOf2UpperBound):
            try:
                dictSection = competitorList[f"competitor{x+1}"]
                if dictSection["gotBye"] == True:
                    print(f"competitor {x} has a bye!")
                    byes = byes+1
                    notByed.append(False)
                else:
                    print(f"competitor {x} exists and doesn't have a bye!")
                    notByed.append(dictSection["name"])
            except KeyError:
                print(f"competitor {x} doesn't exist!")
                notByed.append(False)
        # finding info for current round
        while tempCounter < competitorQuantity:
            tempCounter = tempCounter + 1
            dictSection = competitorList["competitor"+str(tempCounter)]
            originalSeedList.append(dictSection["seed"])
            originalNameList.append(dictSection["name"])
            if dictSection["lastRound"] >= roundNumber:
                if roundNumber == 0:
                    gotBye = dictSection["gotBye"]
                    if gotBye == False:
                        competitorCounter = competitorCounter + 1
                        finalOrder.append(dictSection["name"])
                        finalOrderPos.append(dictSection["position"])
                        finalSeedList.append(dictSection["seed"])
                else:
                    competitorCounter = competitorCounter + 1
                    finalOrder.append(dictSection["name"])
                    finalOrderPos.append(dictSection["position"])
                    finalSeedList.append(dictSection["seed"])
        currentRoundCompetitorQuantity = len(finalOrder)
        print(f"Here are all the competitors that made it to round {roundNumber}:")
        for x in range(currentRoundCompetitorQuantity):
            print(f"{x+1}. {finalOrder[x]}")
        # What comes after info is found
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
                    # finding the longest name
                    firstRoundCompetitors = []
                    maxNameLength = 0
                    for x in range(1, competitorQuantity+1):
                        dictSection = competitorList["competitor"+str(x)]
                        if len(str(dictSection["name"])) > maxNameLength:
                            maxNameLength = len(str(dictSection["name"]))
                    #setting up dimensions for image
                    centerNodeOffset = int(totalRounds)
                    lengthPerCharacterSize = 8
                    fontSize = int(2.5*lengthPerCharacterSize)
                    lineWidth = 4
                    deadspaceWidth = lineWidth*4
                    possibleXPositions = [deadspaceWidth]
                    possibleYPositions = [deadspaceWidth]
                    pointRadius=int(lineWidth*1.5)
                    verticalCompetitorSpacing = 2*lengthPerCharacterSize
                    if maxNameLength < 5:
                        horizontalCompetitorSpacing = 5*(lengthPerCharacterSize+2)
                    else:
                        horizontalCompetitorSpacing = (lengthPerCharacterSize+2)*maxNameLength
                    # there has to be a better way than two very similar cases... Oh well! That's a problem for later me!
                    if byes == competitorQuantity:
                        # if competitors are a perfect power of 2
                        imageHeight = (2*verticalCompetitorSpacing*powerOf2UpperBound) + 2*deadspaceWidth
                        imageLength = 4*(horizontalCompetitorSpacing*(int(totalRounds))) + 2*deadspaceWidth
                        # setting up a grid where every possible matchup is on...
                        for x in range(1,(4*(int(totalRounds)))+1):
                            possibleXPositions.append(deadspaceWidth+(x*horizontalCompetitorSpacing))
                        for x in range(1,int((2*competitorQuantity))+1):
                            possibleYPositions.append(deadspaceWidth+(x*verticalCompetitorSpacing))
                        svgMarkup =f'<svg width="{imageLength}" height="{imageHeight}" xmlns="http://www.w3.org/2000/svg">\n<rect width="{imageLength}" height="{imageHeight}" x="0" y ="0" fill="white" />\n'
                        rounds = {
                        }
                        for x in range(totalRounds+2):
                            roundList = []
                            if x <= roundNumber:
                                for z in range(competitorQuantity):
                                    dictSection=competitorList[f"competitor{z+1}"]
                                    if dictSection["lastRound"] >= x:
                                        roundList.append(dictSection["name"])
                            else:
                                for y in range(competitorQuantity):
                                    roundList.append("")
                            rounds[x] = roundList
                        print(rounds)
                        #defining relevant nodes
                        possiblyRelevantNodes = {}
                        leftSide = True
                        universalNodeID = 0
                        posInLayer = []
                        maxLevel = int(len(possibleXPositions)/4)+1
                        for x in range(maxLevel+1):
                            posInLayer.append(0)
                        for x in range(int(len(possibleXPositions)/2)+1):
                            layer = int(len(possibleXPositions)/4)-abs(x-int(len(possibleXPositions)/4))+1
                            print(f"layer: {layer}")
                            if layer == maxLevel:
                                leftSide = False
                            if leftSide == True:
                                side = "left"
                            else:
                                side = "right"
                            nodesToSkip = pow(2, layer)
                            for y in range(int(len(possibleYPositions))):
                                if nodesToSkip == 0:
                                    nodesToSkip = pow(2, layer+1) - 1
                                    if layer == maxLevel:
                                        #checking if the node is the center node
                                        possiblyRelevantNodes[universalNodeID] = {
                                            "xPos": 2*x,
                                            "yPos": int(len(possibleYPositions)/2)+centerNodeOffset,
                                            "layer": maxLevel,
                                            "posInLayer": posInLayer[layer],
                                            "side": "middle",
                                        }
                                    else:
                                        possiblyRelevantNodes[universalNodeID] = {
                                            "xPos": 2*x,
                                            "yPos": y,
                                            "layer": layer,
                                            "posInLayer": posInLayer[layer],
                                            "side": side,
                                        }
                                    universalNodeID = universalNodeID+1
                                    posInLayer[layer] = posInLayer[layer] + 1
                                else:
                                    nodesToSkip = nodesToSkip - 1
                        for x in possiblyRelevantNodes:
                            node = possiblyRelevantNodes[x]
                            print(x, node)
                        print(maxLevel)
                        relevantNodes = {}
                        for x in possiblyRelevantNodes:
                            node = possiblyRelevantNodes[x]
                            node["competitor"] = rounds[node["layer"]][node["posInLayer"]]
                            relevantNodes[x] = node
                        for x in relevantNodes:
                            node = relevantNodes[x]
                            print(x, node)
                        for x in relevantNodes:
                            node = possiblyRelevantNodes[x]
                            svgMarkup += f'<circle cx="{possibleXPositions[node["xPos"]]}" cy="{possibleYPositions[node["yPos"]]}" r="{pointRadius}" fill="black" />\n'
                        # sorting nodes into side-based lists
                        leftNodes = []
                        centerNodes = []
                        rightNodes = []
                        for x in relevantNodes:
                            node=relevantNodes[x]
                            match node["side"]:
                                case "left":
                                    leftNodes.append(x)
                                case "middle":
                                    centerNodes.append(x)
                                case "right":
                                    centerNodes.append(x)
                        # sorting nodes into a list by layer
                        nodesByLayer = []
                        for x in range(maxLevel+1):
                            currentLayer = []
                            for y in possiblyRelevantNodes:
                                node = possiblyRelevantNodes[y]
                                if node["layer"] == x:
                                    currentLayer.append(y)
                            nodesByLayer.append(currentLayer)
                        print(nodesByLayer)
                        # adding name and drawing lines
                        svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)+centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                        svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)-1]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)+1]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                        for x in range(len(nodesByLayer)-1):
                            currentLayer = nodesByLayer[x]
                            nextLayer = nodesByLayer[x+1]
                            for y in range(len(currentLayer)):
                                currentNodeID = currentLayer[y]
                                try:
                                    currentNode = relevantNodes[currentNodeID]
                                    print(f"node {currentNodeID} does exist!")
                                    nodeExists = True
                                except KeyError:
                                    nodeExists = False
                                if nodeExists == True:
                                    nextNodeID = nextLayer[math.floor(y/2)]
                                    nextNode = relevantNodes[nextNodeID]
                                    svgMarkup += f'<path stroke="black" stroke-width="{lineWidth}" fill="none" d="M {possibleXPositions[currentNode["xPos"]]} {possibleYPositions[currentNode["yPos"]]} L {possibleXPositions[int((currentNode["xPos"]+nextNode["xPos"])/2)]} {possibleYPositions[currentNode["yPos"]]} L {possibleXPositions[nextNode["xPos"]]} {possibleYPositions[nextNode["yPos"]]}" />\n'
                                    if currentNode["competitor"] == False:
                                        textToRender = ""
                                    else:
                                        textToRender = currentNode["competitor"]
                                    if currentNode["side"]=="left":
                                        svgMarkup += f'<text x="{possibleXPositions[currentNode["xPos"]]+pointRadius}" y="{possibleYPositions[currentNode["yPos"]-1]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{textToRender}</text>\n'
                                    if currentNode["side"]=="right":
                                        svgMarkup += f'<text x="{possibleXPositions[currentNode["xPos"]-1]+pointRadius}" y="{possibleYPositions[currentNode["yPos"]-1]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{textToRender}</text>\n'
                                    if roundNumber > int(totalRounds):
                                        competitionVictor = finalOrder[0]
                                        svgMarkup += f'<text x="{possibleXPositions[int(len(possibleXPositions)/2)]}" y="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset-1]+lineWidth}" fill="black" stroke="black" text-anchor="middle" font-size="{2*fontSize}">{str(competitionVictor)}</text>\n'
                                else:
                                    print(f"node {currentNodeID} does not exist!")
                    else:
                        # if they aren't
                        imageHeight = (verticalCompetitorSpacing*(powerOf2UpperBound)) + 2*deadspaceWidth
                        imageLength = 4*(horizontalCompetitorSpacing*(int(totalRounds+1))) + 2*deadspaceWidth
                        # setting up a grid where every possible matchup is on...
                        for x in range(1,(4*(int(totalRounds)+1))+1):
                            possibleXPositions.append(deadspaceWidth+(x*horizontalCompetitorSpacing))
                        for x in range(1,int((powerOf2UpperBound))+1):
                            possibleYPositions.append(deadspaceWidth+(x*verticalCompetitorSpacing))
                        svgMarkup =f'<svg width="{imageLength}" height="{imageHeight}" xmlns="http://www.w3.org/2000/svg">\n<rect width="{imageLength}" height="{imageHeight}" x="0" y ="0" fill="white" />\n'
                        rounds = {
                        0: notByed
                        }
                        for x in range(1, totalRounds+2):
                            roundList = []
                            if x <= roundNumber:
                                for z in range(competitorQuantity):
                                    dictSection=competitorList[f"competitor{z+1}"]
                                    if dictSection["lastRound"] >= x:
                                        roundList.append(dictSection["name"])
                            else:
                                for y in range(competitorQuantity):
                                    roundList.append("")
                            rounds[x] = roundList
                        print(rounds)
                        #defining relevant nodes
                        possiblyRelevantNodes = {}
                        leftSide = True
                        universalNodeID = 0
                        posInLayer = []
                        maxLevel = int(len(possibleXPositions)/4)
                        for x in range(maxLevel+1):
                            posInLayer.append(0)
                        for x in range(int(len(possibleXPositions)/2)+1):
                            layer = int(len(possibleXPositions)/4)-abs(x-int(len(possibleXPositions)/4))
                            print(f"layer: {layer}")
                            if layer == maxLevel:
                                leftSide = False
                            if leftSide == True:
                                side = "left"
                            else:
                                side = "right"
                            nodesToSkip = pow(2, layer)
                            for y in range(int(len(possibleYPositions))):
                                if nodesToSkip == 0:
                                    nodesToSkip = pow(2, layer+1) - 1
                                    if layer == maxLevel:
                                        #checking if the node is the center node
                                        possiblyRelevantNodes[universalNodeID] = {
                                            "xPos": 2*x,
                                            "yPos": int(len(possibleYPositions)/2)+centerNodeOffset,
                                            "layer": maxLevel,
                                            "posInLayer": posInLayer[layer],
                                            "side": "middle",
                                        }
                                    else:
                                        possiblyRelevantNodes[universalNodeID] = {
                                            "xPos": 2*x,
                                            "yPos": y,
                                            "layer": layer,
                                            "posInLayer": posInLayer[layer],
                                            "side": side,
                                        }
                                    universalNodeID = universalNodeID+1
                                    posInLayer[layer] = posInLayer[layer] + 1
                                else:
                                    nodesToSkip = nodesToSkip - 1
                        for x in possiblyRelevantNodes:
                            node = possiblyRelevantNodes[x]
                            print(x, node)
                        print(maxLevel)
                        relevantNodes = {}
                        for x in possiblyRelevantNodes:
                            node = possiblyRelevantNodes[x]
                            if node["layer"] == 0:
                                if rounds[0][node["posInLayer"]] == False:
                                    print(f"Excluded node {x} in layer 0 because it shouldn't exist!")
                                else:
                                    node["competitor"] = rounds[0][node["posInLayer"]]
                                    relevantNodes[x] = node
                            else:
                                node["competitor"] = rounds[node["layer"]][node["posInLayer"]]
                                relevantNodes[x] = node
                        for x in relevantNodes:
                            node = relevantNodes[x]
                            print(x, node)
                        for x in relevantNodes:
                            node = possiblyRelevantNodes[x]
                            svgMarkup += f'<circle cx="{possibleXPositions[node["xPos"]]}" cy="{possibleYPositions[node["yPos"]]}" r="{pointRadius}" fill="black" />\n'
                        # sorting nodes into side-based lists
                        leftNodes = []
                        centerNodes = []
                        rightNodes = []
                        for x in relevantNodes:
                            node=relevantNodes[x]
                            match node["side"]:
                                case "left":
                                    leftNodes.append(x)
                                case "middle":
                                    centerNodes.append(x)
                                case "right":
                                    centerNodes.append(x)
                        # sorting nodes into a list by layer
                        nodesByLayer = []
                        for x in range(maxLevel+1):
                            currentLayer = []
                            for y in possiblyRelevantNodes:
                                node = possiblyRelevantNodes[y]
                                if node["layer"] == x:
                                    currentLayer.append(y)
                            nodesByLayer.append(currentLayer)
                        print(nodesByLayer)
                        # adding name and drawing lines
                        svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)+centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                        svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)-1]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)+1]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                        for x in range(len(nodesByLayer)-1):
                            currentLayer = nodesByLayer[x]
                            nextLayer = nodesByLayer[x+1]
                            for y in range(len(currentLayer)):
                                currentNodeID = currentLayer[y]
                                try:
                                    currentNode = relevantNodes[currentNodeID]
                                    print(f"node {currentNodeID} does exist!")
                                    nodeExists = True
                                except KeyError:
                                    nodeExists = False
                                if nodeExists == True:
                                    nextNodeID = nextLayer[math.floor(y/2)]
                                    nextNode = relevantNodes[nextNodeID]
                                    svgMarkup += f'<path stroke="black" stroke-width="{lineWidth}" fill="none" d="M {possibleXPositions[currentNode["xPos"]]} {possibleYPositions[currentNode["yPos"]]} L {possibleXPositions[int((currentNode["xPos"]+nextNode["xPos"])/2)]} {possibleYPositions[currentNode["yPos"]]} L {possibleXPositions[nextNode["xPos"]]} {possibleYPositions[nextNode["yPos"]]}" />\n'
                                    if currentNode["competitor"] == False:
                                        textToRender = ""
                                    else:
                                        textToRender = currentNode["competitor"]
                                    if currentNode["side"]=="left":
                                        svgMarkup += f'<text x="{possibleXPositions[currentNode["xPos"]]+pointRadius}" y="{possibleYPositions[currentNode["yPos"]-1]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{textToRender}</text>\n'
                                    if currentNode["side"]=="right":
                                        svgMarkup += f'<text x="{possibleXPositions[currentNode["xPos"]-1]+pointRadius}" y="{possibleYPositions[currentNode["yPos"]-1]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{textToRender}</text>\n'
                                    if roundNumber > int(totalRounds):
                                        competitionVictor = finalOrder[0]
                                        svgMarkup += f'<text x="{possibleXPositions[int(len(possibleXPositions)/2)]}" y="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset-1]+lineWidth}" fill="black" stroke="black" text-anchor="middle" font-size="{2*fontSize}">{str(competitionVictor)}</text>\n'
                                else:
                                    print(f"node {currentNodeID} does not exist!")
                    # for reference. puts a dot at every single "possible position"
                    #for x in possibleXPositions:
                    #    for y in possibleYPositions:
                    #        svgMarkup += f'<circle cx="{x}" cy="{y}" r="5" fill="red" />\n'
                    #setting up list of all competitors at various rounds
                    # defining "relevant nodes," where each matchup actually happens
                    #maxLevel = 1 + int(len(possibleXPositions)/4)
                    #levelNodeCounter = []
                    #for x in range(maxLevel):
                    #    levelNodeCounter.append(0)
                    #relevantNodes = {}
                    #leftSide = True
                    #universalNodeID = 0
                    #unusedNodes = 0
                    #for x in range(int(len(possibleXPositions)/2)+1):
                    #    layer = int(len(possibleXPositions)/4)-abs(x-int(len(possibleXPositions)/4))
                    #    if layer == maxLevel:
                    #        leftSide == False
                    #    posInLayer = 0
                    #    nodesToSkip = pow(2, layer)
                    #    for y in range(int(len(possibleYPositions))):
                    #        if nodesToSkip == 0:
                    #            nodeIsRelevant = True
                    #            if layer == 0:
                    #                try:
                    #                    dictSection = competitorList[f"competitor{y+1}"]
                    #                    if dictSection['gotBye'] == True:
                    #                        nodeIsRelevant = False
                    #                except KeyError:
                    #                    nodeIsRelevant = False
                    ##            if nodeIsRelevant == True:
                    #                if leftSide == True:
                    #                    side = "left"
                    #                else:
                    #                    side = "right"
                    #                if x == int(len(possibleXPositions)/4):
                    #                    relevantNodes[universalNodeID] = {
                    #                        "xPos": 2*x,
                    #                        "yPos": int(len(possibleYPositions)/2)+centerNodeOffset,
                    #                        "layer": layer,
                    #                        "posInLayer": 1,
                    #                        "side": "middle"
                    #                    }
                    #                    svgMarkup += f'<circle cx="{possibleXPositions[2*x]}" cy="{possibleYPositions[int(len(possibleYPositions)/2)+centerNodeOffset]}" r="{pointRadius}" fill="black" />\n'
                    #                else:
                    #                    relevantNodes[universalNodeID] = {
                    #                        "xPos": 2*x,
                    #                        "yPos": y,
                    #                        "layer": layer,
                    #                        "posInLayer": posInLayer,
                    #                        "side": side
                    #                    }
                    #                universalNodeID = universalNodeID + 1
                    #            else:
                    #                unusedNodes = unusedNodes+1
                    #                relevantNodes[-unusedNodes] = {
                    #                        "xPos": 2*x,
                    #                        "yPos": y,
                    #                        "layer": layer,
                    #                        "posInLayer": posInLayer,
                    #                        "side": side
                    #                    }
                    #            levelNodeCounter[layer] = levelNodeCounter[layer]+1
                    #            nodesToSkip = pow(2, layer+1) - 1
                    #            posInLayer = posInLayer + 1
                    #        else:
                    #            nodesToSkip = nodesToSkip - 1
                    # sorting through that ungodly list and returning which nodes are at each layer
                    #nodesSortedByLayer = []
                    #for x in range(maxLevel):
                    #    currentLayerNodes = []
                    #    for y in range(len(relevantNodes)):
                    #        try:
                    #            node = relevantNodes[y]
                    #            if node["layer"] == x:
                    #                currentLayerNodes.append(y)
                    #        except KeyError:
                    #            print(f"Not including node {y} because it doesn't exist!")
                    #    nodesSortedByLayer.append(currentLayerNodes)
                    #print("nodes by layer:", nodesSortedByLayer)
                    # also getting a nice list of the nodes on each side
                    #leftNodes = []
                    #rightNodes = []
                    #centerNodes = []
                    #for x in relevantNodes:
                    #    node = relevantNodes[x]
                    #    match node["side"]:
                    #        case "left":
                    #            leftNodes.append(x)
                    #        case "right":
                    #            rightNodes.append(x)
                    #        case "middle":
                    #            centerNodes.append(x)
                            
                    # building the structure of the bracket
                    #for x in range(maxLevel):
                    #    print("Iteration", x+1)
                    #    currentLayer = nodesSortedByLayer[x]
                    #    nextLayer = nodesSortedByLayer[x+1]
                    #    for y in range(len(currentLayer)):
                    #        currentNodeID = currentLayer[y]
                    #        currentNode = relevantNodes[currentNodeID]
                    #        print("current:", currentNode)
                    #        nextNodeID = nextLayer[math.floor(y/2)]
                    #        nextNode = relevantNodes[nextNodeID]
                    #        print("next:", nextNode)
                    #        svgMarkup += f'<circle cx="{possibleXPositions[currentNode["xPos"]]}" cy="{possibleYPositions[currentNode["yPos"]]}" r="{pointRadius}" fill="black" />\n'
                    #        print(f"drew a point at relevant node {currentNodeID}!")
                    #        svgMarkup += f'<path stroke="black" stroke-width="{lineWidth}" fill="none" d="M {possibleXPositions[currentNode["xPos"]]} {possibleYPositions[currentNode["yPos"]]} L {possibleXPositions[int((currentNode["xPos"]+nextNode["xPos"])/2)]} {possibleYPositions[currentNode["yPos"]]} L {possibleXPositions[nextNode["xPos"]]} {possibleYPositions[nextNode["yPos"]]}" />\n'
                    #        print(f"drew a path between node {currentNodeID} and {nextNodeID}!")

                    #drawing lines for winner's "podium"
                    #svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)+centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                    #svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)-1]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)+1]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                    # labelling all the universal node IDs
                    #for x in range(int(len(relevantNodes)/2)):
                    #    try:
                    #        node = relevantNodes[x]
                    #        svgMarkup += f'<text x="{possibleXPositions[node["xPos"]]}" y="{possibleYPositions[node["yPos"]-1]+int(fontSize/2)}" fill="red" stroke="red" font-size="{fontSize}">{str(x)}</text>'
                    #        svgMarkup += f'<text x="{possibleXPositions[len(possibleXPositions)-node["xPos"]-1]-horizontalCompetitorSpacing}" y="{possibleYPositions[len(possibleYPositions)-node["yPos"]-2]+int(fontSize/2)}" fill="red" stroke="red" font-size="{fontSize}">{str(len(relevantNodes)-x)}</text>'
                    #    except KeyError:
                    #        print(f"node {x} doesn't exist!")
                    
                    # putting names of competitors in their places
                    #for x in range(roundNumber):
                    #    print(f"Started getting ready for round {x+1}")
                    #    #getting a list of all nodes in the relevant round
                    #    currentRoundNodes = []
                    #    for y in range(universalNodeID):
                    #        try:
                    #            node = relevantNodes[y]
                    #            if node["layer"] == x:
                    #                currentRoundNodes.append(y)
                    #        except KeyError:
                    #            print(f"node {y} doesn't exist!")
                    #    print("Relevant nodes of the current round", len(currentRoundNodes), currentRoundNodes)
                    #    # getting a list of all competitors in the current round
                    #    currentRoundCompetitorNames = []
                    #    for y in range(len(competitorList)-1):
                    #        competitor = competitorList["competitor"+str(y+1)]
                    #        if competitor["lastRound"] >= x+1:
                    #            currentRoundCompetitorNames.append(competitor["name"])
                    #    print("Relevant competitors in the current round", len(currentRoundCompetitorNames), currentRoundCompetitorNames)
                    #    # putting the competitors' names on the bracket
                    #    for y in range(int(len(currentRoundNodes)/2)):
                    #        currentNode = currentRoundNodes[y]
                    #        node = relevantNodes[currentNode]
                    #        svgMarkup += f'<text x="{possibleXPositions[node["xPos"]]+pointRadius}" y="{possibleYPositions[node["yPos"]-1]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{str(currentRoundCompetitorNames[y])}</text>\n'
                    #        svgMarkup += f'<text x="{possibleXPositions[len(possibleXPositions)-node["xPos"]-1]-horizontalCompetitorSpacing}" y="{possibleYPositions[len(possibleYPositions)-node["yPos"]-2]+int(fontSize/2)}" fill="black" stroke="black" font-size="{fontSize}">{str(currentRoundCompetitorNames[len(currentRoundCompetitorNames)-y-1])}</text>\n'
                    # checking if there is a victor
                    #if roundNumber > int(totalRounds):
                    #    competitionVictor = finalOrder[0]
                    #    svgMarkup += f'<text x="{possibleXPositions[int(len(possibleXPositions)/2)]}" y="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset-1]+lineWidth}" fill="black" stroke="black" text-anchor="middle" font-size="{2*fontSize}">{str(competitionVictor)}</text>\n'
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
