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

def findFile(fileName, validFileLists):
    fileExists = False
    for fileType in validFileLists:
        fileToFind = fileName+fileType
        try:
            open(fileToFind, "r")
            fileExists = True
            print(f"{fileToFind} exists!")
            break
        except FileNotFoundError:
            print(f"File {fileName} doesn't have the {fileType} file extension!")
    if fileExists == False:
        ValidFileName = False
    else:
        ValidFileName = fileToFind
    return ValidFileName
validTumblrFileFormats = [".png", ".jpeg", ".webp", ".gif"]


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
        roundNumber = int(input("What round is is it?\n(inputting a negative round will start a new competition)\n"))
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
        seedingMethod = int(input("By the way... how do you want to seed them?\n1. No Seeding\n2. Random Seeding\n3. Standard Seeding\n4. Cohort Randomized Seeding\n5. Equal Gap Seeding\n"))
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
    while True:
        response = input("Should there be competitor images in the posted polls? (y/n)\n")
        match response:
            case "y":
                print("OK! Put images in the /images directory of wherever you have this python file!")
                useCompetitorImages = True
                needsImageDirectory = True
                break
            case "n":
                print("OK! No competitor images will be used!")
                useCompetitorImages = False
                needsImageDirectory = False
                break
            case _:
                print('Type "y" or "n," please.')
    while True:
        response = input("What Should the header style be?\n1. No header\n2. Text\n3. Image\n")
        match response:
            case "1":
                print("OK! there will be no header!")
                headerStyle = "none"
                headerText = False
                break
            case "2":
                print("OK!")
                headerStyle = "text"
                headerText = input("What should the header say?\n")
                break
            case "3":
                print("OK! Put the image you want to use in the /images directory of wherever you have this python file!")
                headerStyle = "image"
                headerText = False
                needsImageDirectory = True
                break
            case _:
                print('Type one of the options, please.')
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
        propagandaTitles.append(tempPropagandaTitle)
    listPos = 0
    match seedingMethod:
        case 1:
            #returns order the competitors were put in
            unsafeSeedingMethod = "Insert After"
            intermediateSeedList = seedList
        case 2:
            #returns the competitors in a random order
            unsafeSeedingMethod = "Random"
            intermediateSeedList = []
            seedsToAssign = []
            for x in range(competitorQuantity):
                seedsToAssign.append(x+1)
            while len(seedsToAssign) > 0:
                randomCompetitor = random.choice(seedsToAssign)
                seedsToAssign.remove(randomCompetitor)
                intermediateSeedList.append(randomCompetitor)
        case 3:
            #implements what I beleive to be standard seeding, where the 1st seed goes against the last seed and the 2nd seed goes against the 2nd lst seed and so on
            unsafeSeedingMethod = "Via Fake Seeds"
            iteration = 1
            constructedSeedList = [1, 2]
            while len(constructedSeedList) < len(possibleFakeSeeds):
                iteration = iteration + 1
                print(constructedSeedList)
                matchupList = []
                for x in constructedSeedList:
                    matchup = [x, pow(2, iteration)-x+1]
                    matchupList.append(matchup)
                constructedSeedList = []
                for x in range(len(matchupList)):
                    for y in matchupList[x]:
                        constructedSeedList.append(y)
            intermediateSeedList = constructedSeedList
        case 4:
            # Cohort Randomized Seeding
            unsafeSeedingMethod = "Via Fake Seeds"
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
            unsafeSeedingMethod = "Via Fake Seeds"
            iteration = 1
            constructedSeedList = [1, 2]
            while len(constructedSeedList) < len(possibleFakeSeeds):
                iteration = iteration + 1
                print(constructedSeedList)
                matchupList = []
                for x in constructedSeedList:
                    matchup = [x, x+pow(2, iteration-1)]
                    matchupList.append(matchup)
                constructedSeedList = []
                for x in range(len(matchupList)):
                    for y in matchupList[x]:
                        constructedSeedList.append(y)
            intermediateSeedList = constructedSeedList
        case _:
            # catch-all
            print("I haven't done that yet :(")
    if byes != competitorQuantity:
        # positioning unsafe seeds intelligently
        print("Intermediate seed list:", intermediateSeedList)
        finalSeedList = intermediateSeedList
        if seedingMethod in [3, 4, 5]:
            # fake seed method
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
            print("seeds to not bye:", seedsToNotBye, len(seedsToNotBye))
            seedsToBye = []
            for x in seedList:
                if x not in seedsToNotBye:
                    seedsToBye.append(x)
        else:
            finalSeedList = intermediateSeedList
            actuallyUnsafeSeeds = []
            seedsToNotBye = []
            listPos = len(seedList) - 1
            while len(unsafeSeeds) > len(actuallyUnsafeSeeds):
                actuallyUnsafeSeeds.append(finalSeedList[listPos])
                seedsToNotBye.append(finalSeedList[listPos])
                listPos = listPos-2
            unsafeSeedListPos = 0
            while len(seedsToNotBye) < competitorQuantity-byes:
                unsafeSeedToFind = actuallyUnsafeSeeds[unsafeSeedListPos]
                print(f"finding location of seed {unsafeSeedToFind}")
                safeSeedCollateral = finalSeedList.index(unsafeSeedToFind)-1
                safeSeedToNotBye = finalSeedList[safeSeedCollateral]
                print(f"seed {unsafeSeedToFind} is in a matchup with {safeSeedToNotBye}.")
                unsafeSeedListPos = unsafeSeedListPos - 1
                seedsToNotBye.append(finalSeedList[safeSeedCollateral])
            print("seeds to not bye:", seedsToNotBye, len(seedsToNotBye))
            seedsToBye = []
            for x in seedList:
                if x not in seedsToNotBye:
                    seedsToBye.append(x)
            unsafeSeeds = actuallyUnsafeSeeds
    else:
        seedsToBye = seedList
        finalSeedList = intermediateSeedList
    # saving various competition info
    competitorDict = {
        "tournamentInfo": {
            "type": tournamentType,
            "useCompetitorImages": useCompetitorImages,
            "headerStyle": headerStyle,
            "headerImageAltText": False,
            "headerText": headerText,
            "defaultPropaganda": propagandaPlaceholder,
            "pollQuestion": pollQuestion,
            "pollTags": pollTags,
            "extraAnswerQuantity": 0,
            "extraAnswers": [],
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
            "propaganda":[],
            "altText": False
            }
            competitorDict["competitor"+str(x+1)] = dictSection
            finalOrder.append(competitorNames[int(finalSeedList[x]-1)])
    competitorList = json.dumps(competitorDict, indent=2)
    f = open("tourny_data.json", "w")
    f.write(competitorList+"\n")
    f.close()
    for x in range(competitorQuantity):
        if finalSeedList[x] in seedsToBye:
            print(f"{x+1}. {finalOrder[x]} (byed from round 0)")
        else:
            print(f"{x+1}. {finalOrder[x]}")
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
        if headerStyle == "image":
            headerAltText = competitionSettings["headerImageAltText"]
        propagandaPlaceholder = competitionSettings["defaultPropaganda"]
        pollQuestion = competitionSettings["pollQuestion"]
        pollTags = competitionSettings["pollTags"]
        extraAnswerQuantity = competitionSettings["extraAnswerQuantity"]
        extraAnswers = competitionSettings["extraAnswers"]
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
        for x in range(len(competitorList)-1):
            dictSection = competitorList[f"competitor{x+1}"]
            if dictSection["gotBye"] == True:
                print(f"competitor {x} has a bye!")
                byes = byes+1
                notByed.append(False)
                notByed.append(False)
            else:
                print(f"competitor {x} exists and doesn't have a bye!")
                notByed.append(dictSection["name"])
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
        print("")
        # What comes after info is found
        while True:
            response = str(input("1. Post polls for these competitors\n2. Record results of this round\n3. Render chart for this round\n4. Edit tournament and competitor data\n"))
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
                        try:
                            firstMatchup = int(input(f"What poll do you want to start at?\n(poll 1 is the first poll of this round and poll {int(currentRoundCompetitorQuantity/2)} is the last.)\n"))
                            lastMatchup = int(input(f"What poll do you want to end at?\n(poll 1 is the first poll of this round and poll {int(currentRoundCompetitorQuantity/2)} is the last.)\n"))
                            validStartAndEndPoints = False
                            if firstMatchup<=int(currentRoundCompetitorQuantity/2):
                                if lastMatchup<=int(currentRoundCompetitorQuantity/2):
                                    if firstMatchup<=lastMatchup:
                                        break
                            print("Make sure that both bounds are in the amount of matchups there are, and that the final poll is after or the same as the first one!")
                        except ValueError:
                            print("try again!")

                    while True:
                        response = input("What should happen to these polls?\n1. Immediately publish them\n2. Save them as drafts\n3. Put them in the queue\n")
                        match response:
                            case "1":
                                postMethod = "published"
                                break
                            case "2":
                                postMethod = "draft"
                                break
                            case "3":
                                postMethod = "queue"
                                break
                            case _:
                                print("Type the number for a valid option, please!")
                    useAnyImages = False
                    if headerStyle == "image":
                        useAnyImages = True
                    if useCompetitorImages == True:
                        useAnyImages = True
                    for x in range(firstMatchup-1, lastMatchup):
                        matchupPos = 2*x
                        topCompetitor = finalOrder[matchupPos]
                        topCompetitorSeed=finalSeedList[matchupPos]
                        bottomCompetitor = finalOrder[matchupPos+1]
                        bottomCompetitorSeed = finalSeedList[matchupPos+1]
                        topCompetitorPosition = originalSeedList.index(topCompetitorSeed)
                        topCompetitorDict = competitorList[f"competitor{topCompetitorPosition+1}"]
                        bottomCompetitorPosition = originalSeedList.index(bottomCompetitorSeed)
                        bottomCompetitorDict = competitorList[f"competitor{bottomCompetitorPosition+1}"]
                        print(f"Match {x+1}:\n{topCompetitor} vs. {bottomCompetitor}\n")
                        # handling post layout
                        postFormat = []
                        match headerStyle:
                            case "none":
                                blocksBeforePoll = 0
                                useHeaderImage = False
                            case "text":
                                blocksBeforePoll = 1
                                useHeaderImage = False
                                postFormat.append({
                                    "type": "text",
                                    "text": headerText,
                                    "subtype": "heading1"
                                })
                            case "image":
                                blocksBeforePoll = 1
                                useHeaderImage = True
                                if headerAltText == False:
                                    postFormat.append({
                                        "type":"image",
                                        "media": [{
                                            "type": "images/png",
                                            "identifier": "heading"
                                        }],
                                    })
                                else:
                                    postFormat.append({
                                        "type":"image",
                                        "media": [{
                                            "type": "images/png",
                                            "identifier": "heading"
                                        }],
                                        "alt_text": headerAltText
                                    })
                        if useCompetitorImages == True:
                            competitorImageBlocks = [blocksBeforePoll,blocksBeforePoll+1]
                            blocksBeforePoll = blocksBeforePoll + 2
                            if topCompetitorDict["altText"] == False:
                                postFormat.append({
                                        "type":"image",
                                        "media": [{
                                            "type": "images/png",
                                            "identifier": "topcompetitor"
                                        }]
                                    })
                            else:
                                postFormat.append({
                                        "type":"image",
                                        "media": [{
                                            "type": "images/png",
                                            "identifier": "topcompetitor"
                                        }],
                                        "alt_text": topCompetitorDict["altText"]
                                    })
                            if bottomCompetitorDict["altText"] == False:
                                postFormat.append({
                                        "type":"image",
                                        "media": [{
                                            "type": "images/png",
                                            "identifier": "bottomcompetitor"
                                        }]
                                    })
                            else:
                                postFormat.append({
                                        "type":"image",
                                        "media": [{
                                            "type": "images/png",
                                            "identifier": "bottomcompetitor"
                                        }],
                                        "alt_text": bottomCompetitorDict["altText"]
                                    })
                        else:
                            competitorImageBlocks = False
                        actualPollTags = [f"round {roundNumber}", f"{topCompetitor}", f"{bottomCompetitor}"]
                        
                        for y in pollTags:
                            actualPollTags.append(y)
                        
                        pollOptions = [
                            {
                                "answer_text": topCompetitor
                            },
                            {
                                "answer_text": bottomCompetitor
                            }
                        ]
                        if extraAnswerQuantity > 0:
                            for y in range(extraAnswerQuantity):
                                pollOptions.append({
                                    "answer_text": extraAnswers[y]
                                })
                        
                        postFormat.append({
                            "type": "poll",
                            "question": pollQuestion,
                            "client_id": str(uuid.uuid4()),
                            "answers": pollOptions,
                            "settings":{
                                "closed_status": "closed-after",
                                "expire_after": pollTimeLength
                            }
                        })

                        totalBlocks = blocksBeforePoll + 1
                        # also, a reminder to myself... Since tumblr blocks start at 0 and it starts at 1, this "blocksBeforePoll" viariable is ALSO the block that the poll will be on.
                        # setting up propaganda... there still has to be a better way than two very similar things run one after the other
                        # for top competitor
                        totalBlocks = totalBlocks+1
                        postFormat.append({
                            "type": "text",
                            "text": topCompetitorDict["propagandaTitle"],
                            "subtype": "heading2"
                        })
                        if len(topCompetitorDict["propaganda"])>0:
                            for y in topCompetitorDict["propaganda"]:
                                totalBlocks = totalBlocks+1
                                postFormat.append({
                                    "type": "text",
                                    "text": f"“{y}”"
                                })
                        else:
                            totalBlocks = totalBlocks+1
                            postFormat.append({
                                "type": "text",
                                "text": propagandaPlaceholder
                            })
                        # for bottom competitor
                        totalBlocks = totalBlocks+1
                        postFormat.append({
                            "type": "text",
                            "text": bottomCompetitorDict["propagandaTitle"],
                            "subtype": "heading2"
                        })
                        if len(bottomCompetitorDict["propaganda"])>0:
                            for y in bottomCompetitorDict["propaganda"]:
                                totalBlocks = totalBlocks+1
                                postFormat.append({
                                    "type": "text",
                                    "text": f"“{y}”"
                                })
                        else:
                            totalBlocks = totalBlocks+1
                            postFormat.append({
                                "type": "text",
                                "text": propagandaPlaceholder
                            })
                        # setting up post layout
                        postDisplayBlocks = []
                        if headerStyle == "none":
                            currentBlock = 0
                        else:
                            postDisplayBlocks.append({"blocks": [0]})
                            currentBlock = 1
                        if useCompetitorImages == True:
                            postDisplayBlocks.append({"blocks": competitorImageBlocks})
                            currentBlock = competitorImageBlocks[-1]+1
                        for y in range(currentBlock, totalBlocks):
                            postDisplayBlocks.append({"blocks": [y]})
                        postLayout = [
                            {
                                "type": "rows",
                                "display": postDisplayBlocks,
                                "truncate_after": blocksBeforePoll
                            }
                        ]
                        # setting up media sources
                        postMediaSources = {}
                        if headerStyle == "image":
                            headerFilePath = findFile("images/header", validTumblrFileFormats)
                            if headerFilePath == False:
                                print("There isn't a valid heading image in the \"images\" directory:\n1. Make sure there is a folder named \"images\" in the folder that contains this program and confirm that the heading image is in there.\n2. Make sure that the heading image is called \"heading\"\n3. Make sure that the heading image is a file type supported by Tumblr")
                            else:
                                postMediaSources["heading"] = headerFilePath
                        if useCompetitorImages == True:
                            topCompetitorFilePath = headerFilePath = findFile(f"images/{topCompetitorPosition+1}", validTumblrFileFormats)
                            if topCompetitorFilePath == False:
                                print(f"There isn't a valid image for competitor {topCompetitorPosition+1}... Attempting to use a placeholder image.")
                                placeholderFilePath = headerFilePath = findFile("images/placeholder", validTumblrFileFormats)
                                if placeholderFilePath == False:
                                    print("There isn't a valid placeholder image in the \"images\" directory:\n1. Make sure there is a folder named \"images\" in the folder that contains this program and confirm that the heading image is in there.\n2. Make sure that the heading image is called \"placeholder\"\n3. Make sure that the heading image is a file type supported by Tumblr")
                                else:
                                    postMediaSources["topcompetitor"] = placeholderFilePath
                            else:
                                postMediaSources["topcompetitor"] = topCompetitorFilePath
                            bottomCompetitorFilePath = headerFilePath = findFile(f"images/{bottomCompetitorPosition+1}", validTumblrFileFormats)
                            if bottomCompetitorFilePath == False:
                                print(f"There isn't a valid image for competitor {bottomCompetitorPosition+1}... Attempting to use a placeholder image.")
                                placeholderFilePath = headerFilePath = findFile("images/placeholder", validTumblrFileFormats)
                                if placeholderFilePath == False:
                                    print("There isn't a valid placeholder image in the \"images\" directory:\n1. Make sure there is a folder named \"images\" in the folder that contains this program and confirm that the heading image is in there.\n2. Make sure that the heading image is called \"placeholder\"\n3. Make sure that the heading image is a file type supported by Tumblr")
                                else:
                                    postMediaSources["bottomcompetitor"] = placeholderFilePath
                            else:
                                postMediaSources["bottomcompetitor"] = bottomCompetitorFilePath
                        client.create_post(
                            blogname=postedBlog,
                            tags= actualPollTags,
                            state= postMethod,
                            content = postFormat,
                            layout = postLayout,
                            media_sources = postMediaSources
                        )
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
                    roundNumber = roundNumber + 1
                    finalOrder = []
                    finalOrderPos = []
                    finalSeedList = []
                    for x in range(competitorQuantity):
                        dictSection = competitorList[f"competitor{x+1}"]
                        if dictSection["lastRound"] >= roundNumber:
                            finalOrder.append(dictSection["name"])
                            finalOrderPos.append(dictSection["position"])
                            finalSeedList.append(dictSection["seed"])
                    currentRoundCompetitorQuantity = len(finalOrder)
                    print("")
                    print(f"And here is the updated competitor list, for round {roundNumber}:")
                    for x in range(len(finalOrder)):
                        print(f"{x+1}. {finalOrder[x]}")
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
                            0: originalSeedList
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
                                    rightNodes.append(x)
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
                        print("max in each level:", posInLayer)
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
                                try:
                                    node["competitor"] = rounds[node["layer"]][node["posInLayer"]]
                                    relevantNodes[x] = node
                                except IndexError:
                                    print(f"Excluding node {x}!")
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
                case "4":
                    # updating tournament data
                    while True:
                        response = input("What would you like to change?\n1. Tournament Settings\n2. Competitor Information\n")
                        match response:
                            case "1":
                                # change tornament settings
                                while True:
                                    print("Here are the tournament's current settings:")
                                    for x in competitorList["tournamentInfo"]:
                                        print(f'{x}: {competitorList["tournamentInfo"][x]}')
                                    response = input("What do you want to change?\n1. Save updated information\n2. The poll question\n3. The poll tags\n4. The header type\n5. The header text\n6. The header alt text\n7. Toggle whether competitor images are used\n8. Edit additional questions\n9. Edit placeholder propaganda\n")
                                    match response:
                                        case "1":
                                            competitorList["tournamentInfo"] = competitionSettings
                                            competitorDict = json.dumps(competitorList, indent=2)
                                            w=open("tourny_data.json", "w")
                                            w.write(competitorDict)
                                            w.close
                                            print("Saved all changes to file!")
                                            break
                                        case "2":
                                            print("Here is the current poll question:")
                                            print(competitionSettings["pollQuestion"])
                                            newQuestion = input("What do you want the new question to be?\n")
                                            print(f'OK! The new poll question is "{newQuestion}"')
                                            competitionSettings["pollQuestion"] = newQuestion
                                        case "3":
                                            print("Editing the poll tags!\n(note that the round and the competitors' names are added automatically.)")
                                            while True:
                                                print("Here are the tags, arranged by their list index:")
                                                if len(competitionSettings["pollTags"]) == 0:
                                                    print("(no entries)")
                                                else:
                                                    for x in range(len(competitionSettings["pollTags"])):
                                                        #f strings aren't working for some reason here...
                                                        print(str(x)+". \""+competitionSettings["pollTags"][x]+"\"")
                                                listEditMethod = input("\nWhat do you want to do?\n1. Go back\n2. Delete entry\n3. Edit entry\n4. Add entry\n")
                                                match listEditMethod:
                                                    case "1":
                                                        break
                                                    case "2":
                                                        while True:
                                                            try:
                                                                relevantIndex=int(input("Please type the index of the entry you wish to delete.\n(type a negative number to clear the list)\n"))
                                                                if relevantIndex < 0:
                                                                    competitionSettings["pollTags"] = []
                                                                    break
                                                                else:
                                                                    if relevantIndex in range(len(competitionSettings["pollTags"])):
                                                                        print(f"Deleting entry {relevantIndex}")
                                                                        competitionSettings["pollTags"].pop(relevantIndex)
                                                                        break
                                                                    else:
                                                                        print("Please type the index of an entry in the list!")
                                                            except ValueError:
                                                                print("Please type an integer!")
                                                    case "3":
                                                        while True:
                                                            try:
                                                                relevantIndex=int(input("Please type the index of the entry you wish to edit.\n"))
                                                                if relevantIndex in range(len(competitionSettings["pollTags"])):
                                                                    newEntry = input(f"What would you like the entry at {relevantIndex} to say?\n")
                                                                    competitionSettings["pollTags"][relevantIndex] = newEntry
                                                                    break
                                                                else:
                                                                    print("Please type the index of an entry in the list!")
                                                            except ValueError:
                                                                print("Please type an integer!")
                                                    case "4":
                                                        newEntry = input("What entry would you like to add?\n")
                                                        competitionSettings["pollTags"].append(newEntry)
                                                    case _:
                                                        print("Please select a valid option!")
                                        case "4":
                                            while True:
                                                headerOption = input("Which heading style should be used?\n1. None\n2. Text\n3. Image\n")
                                                match headerOption:
                                                    case "1":
                                                        competitionSettings["headerSyle"] = "none"
                                                        break
                                                    case "2":
                                                        competitionSettings["headerSyle"] = "text"
                                                        break
                                                    case "3":
                                                        competitionSettings["headerSyle"] = "image"
                                                        break
                                                    case _:
                                                        print("Please select a valid option!")
                                        case "5":
                                            print("Here is the current header text:")
                                            if competitionSettings["headerText"] == False:
                                                print("(no header text)")
                                            else:
                                                print(competitionSettings["headerText"])
                                            competitionSettings["headerText"] = input("What should the new header text be?\n")
                                        case "6":
                                            if competitionSettings["headerImageAltText"] == False:
                                                print("(no header alt text)")
                                            else:
                                                print(competitionSettings["headerImageAltText"])
                                            competitionSettings["headerImageAltText"] = input("What should the header image's new alt text be?\n")
                                        case "7":
                                            if competitionSettings["useCompetitorImages"] == True:
                                                competitionSettings["useCompetitorImages"] = False
                                                print("No longer using competitor images!")
                                            else:
                                                competitionSettings["useCompetitorImages"] = True
                                                print("Now using competitor images!")
                                        case "8":
                                            print("Editing the extra answers!")
                                            while True:
                                                print("Here are the current extra answers, arranged by their list index:")
                                                if len(competitionSettings["extraAnswers"]) == 0:
                                                    print("(no entries)")
                                                else:
                                                    for x in range(len(competitionSettings["extraAnswers"])):
                                                        #f strings aren't working for some reason here...
                                                        print(str(x)+". \""+competitionSettings["extraAnswers"][x]+"\"")
                                                listEditMethod = input("\nWhat do you want to do?\n1. Go back\n2. Delete entry\n3. Edit entry\n4. Add entry\n")
                                                match listEditMethod:
                                                    case "1":
                                                        break
                                                    case "2":
                                                        while True:
                                                            try:
                                                                relevantIndex=int(input("Please type the index of the entry you wish to delete.\n(type a negative number to clear the list)\n"))
                                                                if relevantIndex < 0:
                                                                    competitionSettings["extraAnswers"] = []
                                                                    break
                                                                else:
                                                                    if relevantIndex in range(len(competitionSettings["extraAnswers"])):
                                                                        print(f"Deleting entry {relevantIndex}")
                                                                        competitionSettings["extraAnswers"].pop(relevantIndex)
                                                                        break
                                                                    else:
                                                                        print("Please type the index of an entry in the list!")
                                                            except ValueError:
                                                                print("Please type an integer!")
                                                    case "3":
                                                        while True:
                                                            try:
                                                                relevantIndex=int(input("Please type the index of the entry you wish to edit.\n"))
                                                                if relevantIndex in range(len(competitionSettings["extraAnswers"])):
                                                                    newEntry = input(f"What would you like the entry at {relevantIndex} to say?\n")
                                                                    competitionSettings["extraAnswers"][relevantIndex] = newEntry
                                                                    break
                                                                else:
                                                                    print("Please type the index of an entry in the list!")
                                                            except ValueError:
                                                                print("Please type an integer!")
                                                    case "4":
                                                        newEntry = input("What entry would you like to add?\n")
                                                        competitionSettings["extraAnswers"].append(newEntry)
                                                    case _:
                                                        print("Please select a valid option!")
                                            competitionSettings["extraAnswerQuantity"] = len(competitionSettings["extraAnswers"])
                                        case "9":
                                            print("Current placeholder propaganda when there is none:")
                                            print(competitionSettings["defaultPropaganda"])
                                            competitionSettings["defaultPropaganda"] = input("What should the new placeholder propaganda be?\n")
                                break
                            case "2":
                                while True:
                                    print("Here is every competitor, ordered by their position value:")
                                    for x in range(len(originalNameList)):
                                        print(f"{x+1}. {originalNameList[x]}")
                                    try:
                                        relevantCompetitorPos = int(input("Type the position of the competitor whose info you wish to edit\n"))
                                        if relevantCompetitorPos <= competitorQuantity:
                                            if relevantCompetitorPos > 0:
                                                print(f"Editing the data of the competitor called {originalNameList[relevantCompetitorPos-1]}")
                                                break
                                        print("Please choose a valid competitor!")
                                    except KeyError:
                                        print("Please type an integer!")
                                dictSection = competitorList[f"competitor{relevantCompetitorPos}"]
                                print("Here is all the information on this competitor:")
                                for x in dictSection:
                                    print(f"{x}: {dictSection[x]}")
                                while True:
                                    response = input("What do you want to edit?\n1. Nothing (save changes)\n2. Name\n3. Propaganda Title\n4. Alt text\n5. Competitor Propaganda\n")
                                    match response:
                                        case "1":
                                            competitorList[f"competitor{relevantCompetitorPos}"] = dictSection
                                            competitorDict = json.dumps(competitorList, indent=2)
                                            w=open("tourny_data.json", "w")
                                            w.write(competitorDict)
                                            w.close
                                            print("Saved all changes to file!")
                                            originalNameList[relevantCompetitorPos-1] = dictSection["name"]
                                            break
                                        case "2":
                                            print("Current name of competitor:")
                                            print(dictSection["name"])
                                            dictSection["name"] = input("What should this competitor's new name be?\n")
                                        case "3":
                                            print("Current propaganda title of competitor:")
                                            print(dictSection["propagandaTitle"])
                                            dictSection["propagandaTitle"] = input("What should this competitor's new propaganda title be?\n")
                                        case "4":
                                            print("Current image alt text of competitor:")
                                            if dictSection["altText"] == False:
                                                print("(no alt text)")
                                            else:
                                                print(dictSection["altText"])
                                            dictSection["altText"] = input("What should this competitor's new image alt text be?\n")
                                        case "5":
                                            print("Editing this competitor's propaganda!")
                                            while True:
                                                print("Here are the current bits of propaganda, arranged by their list index:")
                                                if len(dictSection["propaganda"]) == 0:
                                                    print("(no entries)")
                                                else:
                                                    for x in range(len(dictSection["propaganda"])):
                                                        #f strings aren't working for some reason here...
                                                        print(str(x)+". \""+dictSection["propaganda"][x]+"\"")
                                                listEditMethod = input("\nWhat do you want to do?\n1. Go back\n2. Delete entry\n3. Edit entry\n4. Add entry\n")
                                                match listEditMethod:
                                                    case "1":
                                                        break
                                                    case "2":
                                                        while True:
                                                            try:
                                                                relevantIndex=int(input("Please type the index of the entry you wish to delete.\n(type a negative number to clear the list)\n"))
                                                                if relevantIndex < 0:
                                                                    response = input("Are you sure you want to delete all the propaganda? (y/n)\n")
                                                                    if response == "y":
                                                                        dictSection["propaganda"] = []
                                                                    break
                                                                else:
                                                                    if relevantIndex in range(len(dictSection["propaganda"])):
                                                                        print(f"Deleting entry {relevantIndex}")
                                                                        dictSection["propaganda"].pop(relevantIndex)
                                                                        break
                                                                    else:
                                                                        print("Please type the index of an entry in the list!")
                                                            except ValueError:
                                                                print("Please type an integer!")
                                                    case "3":
                                                        while True:
                                                            try:
                                                                relevantIndex=int(input("Please type the index of the entry you wish to edit.\n"))
                                                                if relevantIndex in range(len(dictSection["propaganda"])):
                                                                    newEntry = input(f"What would you like the entry at {relevantIndex} to say?\n")
                                                                    dictSection["propaganda"][relevantIndex] = newEntry
                                                                    break
                                                                else:
                                                                    print("Please type the index of an entry in the list!")
                                                            except ValueError:
                                                                print("Please type an integer!")
                                                    case "4":
                                                        newEntry = input("What entry would you like to add?\n")
                                                        dictSection["propaganda"].append(newEntry)
                                                    case _:
                                                        print("Please select a valid option!")
                                break
                            case _:
                                print("That's not an option!")
                case _:
                    print("That's not an option :(")
    except FileNotFoundError:
        print("Well, there isn't a data file...")
