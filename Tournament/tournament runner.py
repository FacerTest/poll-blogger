# Howdy!
# If you're trying to improve my code, I am so very sorry :(

useDummyData = True
autoAltText = True
dataFileName = "tournament_data.json"

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

# defining various functions... yahoo!
def prettyPrintList(listToPrint, indexOffset):
    for entry in range(len(listToPrint)):
        print(f"{entry+indexOffset}: {listToPrint[entry]}")

def prettyPrintDict(dictToPrint, zeroOffset):
    theDetestableCountingVariable = zeroOffset
    for entry in dictToPrint:
        print(f"{theDetestableCountingVariable}. {entry}: {dictToPrint[entry]}")
        theDetestableCountingVariable = theDetestableCountingVariable + 1

def ynQuestion(askedQuestion):
    acceptedYes = ["y", "Y", "yes", "Yes", "yEs", "YEs", "yeS", "YES"]
    acceptedNo = ["n", "N", "no", "No", "nO", "NO"]
    while True:
        inputtedVariable = input(askedQuestion)
        if inputtedVariable in acceptedYes:
            saidYes = True
            break
        if inputtedVariable in acceptedNo:
            saidYes = False
            break
        print("Please respond with \"yes\" or \"no.\"\nSee below for accepted responses")
        print(f"For yes: {acceptedYes}")
        print(f"For no: {acceptedNo}")
    return saidYes


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

validTumblrImageFileFormats = [".png", ".jpeg", ".webp", ".gif"]

def getValidInt(askedQuestion):
    while True:
        try:
            inputtedVariable = int(input(askedQuestion))
            break
        except ValueError:
            print("Please type an integer!")
    return inputtedVariable

def getValidIntGreaterThan(askedQuestion, minimumValue):
    while True:
        try:
            inputtedVariable = int(input(askedQuestion))
            if inputtedVariable >= minimumValue:
                break
            print(f"Please input a value greater than or equal to {minimumValue}.")
        except ValueError:
            print("Please type an integer!")
    return inputtedVariable

def getValidIntLessThan(askedQuestion, maximumValue):
    while True:
        try:
            inputtedVariable = int(input(askedQuestion))
            if inputtedVariable <= maximumValue:
                break
            print(f"Please input a value less than or equal to {maximumValue}.")
        except ValueError:
            print("Please type an integer!")
    return inputtedVariable

def getValidIntInRange(askedQuestion, minimumValue, maximumValue):
    while True:
        try:
            inputtedVariable = int(input(askedQuestion))
            if inputtedVariable <= maximumValue:
                if inputtedVariable >= minimumValue:
                    break
            print(f"Please input a value equal to or between {minimumValue} and {maximumValue}.")
        except ValueError:
            print("Please type an integer!")
    return inputtedVariable

def editList(listToEdit, maximumLength, friendlyListName):
    print(f"Editing the list {friendlyListName}")
    while True:
        print("Here are the entries, arranged by their list index:")
        if len(listToEdit) == 0:
            print("(there are no entries)")
        else:
            for x in range(len(listToEdit)):
                print(str(x)+". \""+listToEdit[x]+"\"")
        listEditMethod = getValidNumberSelection("\nWhat do you want to do?", ["Go Back", "Delete Entry", "Edit Entry", "Add Entry"])
        match listEditMethod:
            case 1:
                break
            case 2:
                relevantIndex = getValidIntLessThan("Enter the index of the entry you wish to delete.\n(type a negative index to clear the list)\n", len(listToEdit)-1)
                if relevantIndex < 0:
                    if ynQuestion("Are you sure you want to clear this list? (y/n)\n") == True:
                        print("OK! Clearing the list...")
                        listToEdit = []
                    else:
                        print("OK! NOT clearing the list...")
                else:
                    listToEdit.pop(relevantIndex)
            case 3:
                relevantIndex = getValidIntInRange("Enter the index of the entry you wish to edit.\n", 0, len(listToEdit)-1)
                listToEdit[relevantIndex] = input(f"What would you like the entry at {relevantIndex} to say?")
            case 4:
                if maximumLength == False:
                    newEntry = input("What entry would you like to add?\n")
                    listToEdit.append(newEntry)
                else:
                    if len(listToEdit) >= maximumLength:
                        if maximumLength == 1:
                            print("This list cannot have more than 1 entry!")
                        else:
                            print(f"This list cannot have more than {maximumLength} entries!")
                    else:
                        newEntry = input("What entry would you like to add?\n")
                        listToEdit.append(newEntry)
    return listToEdit

def editString(stringToEdit, friendlyStringName):
    print(f"Current value of {friendlyStringName}:")
    if len(stringToEdit) > 0:
        print(f'"{stringToEdit}"')
    else:
        print('"" (empty)')
    stringToEdit = input("What should the new value be?\n")
    return stringToEdit

def flipBool(boolToFlip):
    if boolToFlip == True:
        boolToFlip = False
    else:
        boolToFlip = True
    return boolToFlip

def getValidNumberSelection(askedQuestion, optionList):
    validAnswers = []
    for options in range(len(optionList)):
        validAnswers.append(options+1)
    while True:
        try:
            print(askedQuestion)
            for x in range(len(optionList)-1):
                print(f"{x+1}. {optionList[x]}")
            inputtedVariable = int(input(f"{len(optionList)}. {optionList[-1]}\n"))
            if inputtedVariable in validAnswers:
                break
            print(f"Please input a valid answer.")
        except ValueError:
            print("Please type an integer!")
    return inputtedVariable
    
# saving credentials for pytumblr2...
if pytumblr2Installed == False:
    print("Skipping saving Tumblr credentials, because you don't have pytumblr2 installed!")
else:
    try:
        x = open("credentials.json","x")
        x.close()
        if ynQuestion("Do you have valid credentials for accessing the Tumblr API? (y/n)\n") == True:
            print("OK! (You probably want to copy/paste these)")
            consumerKey=input("What is your consumer key?\n")
            consumerSecret=input("What is your consumer secret?\n")
            oauthToken=input("What is your oauth token?\n")
            oauthSecret=input("What is your oauth secret?\n")
            postedBlog=input("Now... what is the url of the blog are these polls goint to be posted to?\n")
            clientInfo = {
                "hasCredentials": True,
                "consumerKey": consumerKey,
                "consumerSecret": consumerSecret,
                "oauthToken": oauthToken,
                "oauthSecret": oauthSecret,
                "postedBlog": postedBlog
            }
        else:
            clientInfo = {"hasCredentials": False}
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

extantRoundNumber = False
competitorQuantity = 0
competitorNames = []
propagandaTitles = []

# checking if a tournament data file exists
try:
    r = open(dataFileName, "r")
    dataFileExists = True
    competitorList = json.load(r)
except FileNotFoundError:
    dataFileExists = False

# automatically starting a new competition if there is no file
if dataFileExists == False:
    roundNumber = -1
else:
    # getting the highest round
    lastOverallRound = 1
    for x in range(1, len(competitorList)):
        dictSection = competitorList[f"competitor{x}"]
        if dictSection["lastRound"] > lastOverallRound:
            lastOverallRound = dictSection["lastRound"]
    roundNumber = getValidInt(f"What round is is it? Round {lastOverallRound} is the latest one with competitors in it.\n(inputting a negative round will start a new competition)\n")

# starting a new tournament
if roundNumber < 0:
    startedNewTournament = True
    print("Starting a new tournament!")
    if dataFileExists == True:
        print("...but there's already a competition file that exists.")
        if ynQuestion("Do you want to delete it? (y/n)\n") == True:
            print("OK! deleting it...")
            w = open(dataFileName, "w")
        else:
            while True:
                try:
                    roundNumber = int(input(f"What round is is it? Round {lastOverallRound} is the latest one with competitors in it.\n"))
                    if roundNumber < 0:
                        print("No. You didn't want to delete this file, remember?")
                    else:
                        startedNewTournament = False
                        break
                except ValueError:
                    print("Type an integer, please!")
    else:
        w = open(dataFileName, "x")
    if startedNewTournament == True:
        # setting a bunch of random default data
        tournamentType = "Single Elimination"
        pollQuestion = "Which competitor deserves to win this competition the most?"
        pollTags = ["tumblr tournament", "poll", "polls"]
        propagandaPlaceholder = "(no propaganda submitted)"
        if autoAltText == True:
            placehoderImageAltText = "A placeholder image; the intended one could not be found."
            headerAltText = "The post header."
        else:
            placehoderImageAltText = ""
            headerAltText = ""
        # getting number of competitors
        while True:
            try:
                competitorQuantity = int(input(f"How many competitors are there?\n"))
                if competitorQuantity < 2:
                    print("You can't have a competition with less than 2 competitors!")
                else:
                    break
            except ValueError:
                print("Type an integer, please!")
        # figuring out byes
        powerOf2UpperBound = 1
        while powerOf2UpperBound < competitorQuantity:
            powerOf2LowerBound = powerOf2UpperBound
            powerOf2UpperBound = powerOf2UpperBound*2
        byesButBad = powerOf2UpperBound - competitorQuantity
        if byesButBad == 0:
            byes = competitorQuantity
        else:
            byes = byesButBad
        match byesButBad:
            case 0:
                print("The amount of competitors is a power of 2, so all of them will get byed from round 0!")
                lowestRound = 1
            case 1:
                print("1 bye will be used for round 0!")
                lowestRound = 0
            case _:
                print(f"{byes} byes will be used for round 0!")
                lowestRound = 0
        # getting seeding method
        seedingMethod = getValidNumberSelection("How should the competitors be seeded?", ["No Seeding", "Random Seeding", "Standard Seeding", "Cohort Randomized Seeding", "Equal Gap Seeding"])
        # setting some formatting data
        if ynQuestion("Should there be competitor images in the posted polls? (y/n)\n") == True:
            print("OK! Put images in the /images directory of wherever you have this python file!")
            useCompetitorImages = True
            needsImageDirectory = True
        else:
            print("OK! No competitor images will be used!")
            useCompetitorImages = False
            needsImageDirectory = False
        response = getValidNumberSelection("What Should the header style be?", ["No Header", "Text Header", "Image Header"])
        match response:
            case 1:
                print("OK! there will be no header!")
                headerStyle = "none"
                headerText = False
            case 2:
                print("OK!")
                headerStyle = "text"
                headerText = input("What should the header say?\n")
            case 3:
                print("OK! Put the image you want to use in the /images directory of wherever you have this python file!")
                headerStyle = "image"
                headerText = False
                needsImageDirectory = True
        # setting up seed stuff
        seedList = []
        for x in range(competitorQuantity):
            seedList.append(x+1)
        possibleFakeSeeds = []
        for x in range(powerOf2UpperBound):
            possibleFakeSeeds.append(x+1)
        fakeSeeds = []
        for x in possibleFakeSeeds:
            if x not in seedList:
                fakeSeeds.append(x)
        if byes == competitorQuantity:
            safeSeeds = seedList
        else:
            safeSeeds = seedList[0:powerOf2LowerBound]
        unsafeSeeds = []
        for x in seedList:
            if x not in safeSeeds:
                unsafeSeeds.append(x)
        # competitor entry
        for x in range(competitorQuantity):
            if useDummyData == True:
                currentCompetitor = str(x+1)
            else:
                currentCompetitor = input(f"What is the name of competitor {x+1}?\n")
            competitorNames.append(currentCompetitor)
            currentCompetitorPropagandaTitle = currentCompetitor
            propagandaTitles.append(currentCompetitorPropagandaTitle)
        # arrangement of seeds via seeding methods
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
        # dealing with byes, if applicable
        if byes != competitorQuantity:
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
            elif seedingMethod == 2:
                #random seeding
                for x in intermediateSeedList:
                    if x in fakeSeeds:
                        finalSeedList.remove(x)
                seedsToNotBye = []
                numberOfUnsafeSeeds = len(unsafeSeeds)
                unsafeSeeds = []
                possibleUnsafeSeeds = []
                for x in range(math.floor(competitorQuantity/2)):
                    possibleUnsafeSeeds.append(intermediateSeedList[2*x])
                while len(unsafeSeeds) < numberOfUnsafeSeeds:
                    unsafeSeedToAdd = random.choice(possibleUnsafeSeeds)
                    possibleUnsafeSeeds.remove(unsafeSeedToAdd)
                    unsafeSeeds.append(unsafeSeedToAdd)
                for x in unsafeSeeds:
                    seedsToNotBye.append(x)
                unsafeSeedListPos = 0
                while len(seedsToNotBye) < competitorQuantity-byes:
                    unsafeSeedToFind = unsafeSeeds[unsafeSeedListPos]
                    print(f"finding location of seed {unsafeSeedToFind}")
                    safeSeedCollateral = finalSeedList.index(unsafeSeedToFind)+1
                    safeSeedToNotBye = finalSeedList[safeSeedCollateral]
                    print(f"seed {unsafeSeedToFind} is in a matchup with {safeSeedToNotBye}.")
                    unsafeSeedListPos = unsafeSeedListPos +1
                    seedsToNotBye.append(finalSeedList[safeSeedCollateral])
                print("seeds to not bye:", seedsToNotBye, len(seedsToNotBye))
                seedsToBye = []
                for x in seedList:
                    if x not in seedsToNotBye:
                        seedsToBye.append(x)
            else:
                # anything else
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
        # saving tournament data to a variable
        competitorList = {
            "Tournament Info": {
                "Constants": {
                    "type": tournamentType,
                    "byedSeeds": seedsToBye,
                    "totalRounds": int(math.log(powerOf2UpperBound, 2))
                },
                "Parameters": {
                    "useCompetitorImages": useCompetitorImages,
                    "headerStyle": headerStyle,
                    "headerImageAltText": headerAltText,
                    "placeholderImageAltText": placehoderImageAltText,
                    "headerText": headerText,
                    "defaultPropaganda": propagandaPlaceholder,
                    "pollQuestion": pollQuestion,
                    "pollTags": pollTags,
                    "extraAnswers": [],
                    "postData": {
                        "content": [],
                        "layout": [],
                        "mediaSources": []
                    }
                }
            }
        }
        finalOrder = []
        for x in range(len(finalSeedList)):
            if autoAltText == True:
                altText = f"{competitorNames[int(finalSeedList[x]-1)]}"
            else:
                altText = ""
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
            "altText": altText
            }
            competitorList["competitor"+str(x+1)] = dictSection
            finalOrder.append(competitorNames[int(finalSeedList[x]-1)])
        competitorDict = json.dumps(competitorList, indent=2)
        w.write(competitorDict)
        w.close()
        roundNumber = lowestRound


# dealing with a competition in progress
if roundNumber >= 0:
    # loading competition data
    f = open(dataFileName)
    competitorList = json.load(f)
    f.close()
    tournamentInfo = competitorList["Tournament Info"]
    tournamentOptions = tournamentInfo["Parameters"]
    tournamentConstants = tournamentInfo["Constants"]
    competitorQuantity = len(competitorList)-1

    totalRounds = tournamentConstants["totalRounds"]
    competitionType = tournamentConstants["type"]
    useCompetitorImages = tournamentOptions["useCompetitorImages"]
    headerStyle = tournamentOptions["headerStyle"]
    headerText = tournamentOptions["headerText"]
    headerAltText = tournamentOptions["headerImageAltText"]
    placehoderImageAltText = tournamentOptions["placeholderImageAltText"]
    propagandaPlaceholder = tournamentOptions["defaultPropaganda"]
    pollQuestion = tournamentOptions["pollQuestion"]
    pollTags = tournamentOptions["pollTags"]
    extraAnswers = tournamentOptions["extraAnswers"]
    # calculating some more info on the fly
    powerOf2UpperBound = 1
    while powerOf2UpperBound < competitorQuantity:
        powerOf2LowerBound = powerOf2UpperBound
        powerOf2UpperBound = powerOf2UpperBound * 2
    # Setting up variables for creating a list of competitors
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
    print(f"Here are all the competitors that are in round {roundNumber}:")
    for x in range(currentRoundCompetitorQuantity):
        print(f"{x+1}. {finalOrder[x]}")
    while True:
        response = getValidNumberSelection("\n What do you want to do?", ["Post polls for these competitors", "Record results of this round", "Render chart for this round", "Edit tournament and competitor data"])
        match response:
            case 1:
                # posting polls for existing matchup
                pollTimeLength = getValidIntGreaterThan("How many seconds should the polls run for?\n604800 (7 days) is the max value and 86400 (1 day) is the minimum\n", 0)
                while True:
                    try:
                        firstMatchup = getValidInt(f"What poll do you want to start at?\n(poll 1 is the first poll of this round and poll {int(currentRoundCompetitorQuantity/2)} is the last.)\n")
                        lastMatchup = getValidInt(f"What poll do you want to end at?\n(poll 1 is the first poll of this round and poll {int(currentRoundCompetitorQuantity/2)} is the last.)\n")
                        validStartAndEndPoints = False
                        if firstMatchup<=int(currentRoundCompetitorQuantity/2):
                            if lastMatchup<=int(currentRoundCompetitorQuantity/2):
                                if firstMatchup<=lastMatchup:
                                    break
                        print("Make sure that both bounds are in the amount of matchups there are, and that the final poll is after or the same as the first one!")
                    except ValueError:
                        print("Make sure you typed an integer!")
                    getValidNumberSelection("What should happen to these polls?", ["Immediately publish them", "Save them as drafts", "Put them in the queue"])
                    match response:
                        case 1:
                            postMethod = "published"
                        case 2:
                            postMethod = "draft"
                        case 3:
                            postMethod = "queue"
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
                        if len(extraAnswers) > 0:
                            for y in extraAnswers:
                                pollOptions.append({
                                    "answer_text": y
                                })
                        postFormat.append({
                            "type": "poll",
                            "question": pollQuestion,
                            "client_id": "Tumblr forces you to give a poll UUID, but then ignores it and creates its own. Isn't that odd?",
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
                            headerFilePath = findFile("images/header", validTumblrImageFileFormats)
                            if headerFilePath == False:
                                print("There isn't a valid heading image in the \"images\" directory:\n1. Make sure there is a folder named \"images\" in the folder that contains this program and confirm that the heading image is in there.\n2. Make sure that the heading image is called \"heading\"\n3. Make sure that the heading image is a file type supported by Tumblr")
                            else:
                                postMediaSources["heading"] = headerFilePath
                        if useCompetitorImages == True:
                            topCompetitorFilePath = headerFilePath = findFile(f"images/{topCompetitorPosition+1}", validTumblrImageFileFormats)
                            if topCompetitorFilePath == False:
                                print(f"There isn't a valid image for competitor {topCompetitorPosition+1}... Attempting to use a placeholder image.")
                                placeholderFilePath = headerFilePath = findFile("images/placeholder", validTumblrImageFileFormats)
                                if placeholderFilePath == False:
                                    print("There isn't a valid placeholder image in the \"images\" directory:\n1. Make sure there is a folder named \"images\" in the folder that contains this program and confirm that the heading image is in there.\n2. Make sure that the heading image is called \"placeholder\"\n3. Make sure that the heading image is a file type supported by Tumblr")
                                else:
                                    postMediaSources["topcompetitor"] = placeholderFilePath
                            else:
                                postMediaSources["topcompetitor"] = topCompetitorFilePath
                            bottomCompetitorFilePath = headerFilePath = findFile(f"images/{bottomCompetitorPosition+1}", validTumblrImageFileFormats)
                            if bottomCompetitorFilePath == False:
                                print(f"There isn't a valid image for competitor {bottomCompetitorPosition+1}... Attempting to use a placeholder image.")
                                placeholderFilePath = headerFilePath = findFile("images/placeholder", validTumblrImageFileFormats)
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
            case 2:
                # updating matchup
                print("OK! just type the number next to the WINNING competitor!")
                for x in range(int(currentRoundCompetitorQuantity/2)):
                    getValidNumberSelection(f"Matchup {x + 1}:", [finalOrder[2*x], finalOrder[1+(2*x)], "Skip this matchup"])
                    match response:
                        case 1:
                            competitorList[f"competitor{finalOrderPos[x*2]}"]["lastRound"] = roundNumber + 1
                            competitorList[f"competitor{finalOrderPos[1+(x*2)]}"]["lastRound"] = roundNumber
                        case 2:
                            competitorList[f"competitor{finalOrderPos[x*2]}"]["lastRound"] = roundNumber
                            competitorList[f"competitor{finalOrderPos[1+(x*2)]}"]["lastRound"] = roundNumber + 1
                        case 3:
                            pass
                competitorDict = json.dumps(competitorList, indent=2)
                f = open(dataFileName, "w")
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
                print(f"\nAnd here is the updated competitor list, for round {roundNumber}:")
                for x in range(len(finalOrder)):
                    print(f"{x+1}. {finalOrder[x]}")
            case 3:
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
                        lastXPos = deadspaceWidth
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
                            # setting up a grid where every possible matchup is on...
                            alternatingFactor = 1
                            for x in range(1, (4*(int(totalRounds)))+1):
                                if x == 2*(int(totalRounds))+1:
                                    alternatingFactor = 0
                                if x % 2 == alternatingFactor:
                                    possibleXPositions.append(lastXPos+horizontalCompetitorSpacing)
                                else:
                                    possibleXPositions.append(lastXPos+5*(lengthPerCharacterSize+2))
                                lastXPos = possibleXPositions[-1]
                            for x in range(1,int((2*competitorQuantity))+1):
                                possibleYPositions.append(deadspaceWidth+(x*verticalCompetitorSpacing))
                            imageHeight = deadspaceWidth*2+possibleYPositions[-1]
                            imageLength = possibleXPositions[-1] + 2*deadspaceWidth
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
                            svgMarkup += f'<line x1="{possibleXPositions[int((len(possibleXPositions))/2)]-horizontalCompetitorSpacing}" y1="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" x2="{possibleXPositions[int((len(possibleXPositions))/2)]+horizontalCompetitorSpacing}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
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
                            # setting up a grid where every possible matchup is on...
                            alternatingFactor = 1
                            for x in range(1,(4*(int(totalRounds)+1))+1):
                                if x == 2*(int(totalRounds)+1)+1:
                                    alternatingFactor = 0
                                if x % 2 == alternatingFactor:
                                    possibleXPositions.append(lastXPos+horizontalCompetitorSpacing)
                                else:
                                    possibleXPositions.append(lastXPos+5*(lengthPerCharacterSize+2))
                                lastXPos = possibleXPositions[-1]
                            for x in range(1,int((powerOf2UpperBound))+1):
                                possibleYPositions.append(deadspaceWidth+(x*verticalCompetitorSpacing))
                            imageHeight = deadspaceWidth*2+possibleYPositions[-1]
                            imageLength = possibleXPositions[-1] + 2*deadspaceWidth
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
                            svgMarkup += f'<line x1="{possibleXPositions[int((len(possibleXPositions))/2)]-horizontalCompetitorSpacing}" y1="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" x2="{possibleXPositions[int((len(possibleXPositions))/2)]+horizontalCompetitorSpacing}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
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
            case 4:
                # updating tournament data
                optionList = ["Nothing. Take me back!"]
                # you know... there's got to be a better way to do this. oh well!
                dummyString = ""
                dummyList = []
                dummyBoolean = False
                for x in tournamentOptions:
                    optionList.append(x)
                while True:
                    response = getValidNumberSelection("What would you like to edit?", ["Tournament Data", "Competitor Data", "Nothing. Let me out!"])
                    match response:
                        case 1:
                            # editing tournament data
                            while True:
                                print("Constants (for reference, you can't edit these):")
                                prettyPrintDict(tournamentConstants, 1)
                                print("Editable Settings:")
                                prettyPrintDict(tournamentOptions, 1)
                                variableToEdit = getValidNumberSelection("What value do you wish to edit?", optionList)
                                match variableToEdit:
                                    case 1:
                                        break
                                    case 11:
                                        print("That isn't supported right now :(")
                                    case _:
                                        relevantIndex = variableToEdit - 1
                                        variableToEdit = optionList[relevantIndex]
                                        variableType = type(tournamentOptions[variableToEdit])
                                        if variableType == type(dummyString):
                                            print(f"Current value of ")
                                        if variableType == type(dummyList):
                                            match variableToEdit:
                                                case "pollTags":
                                                    maxLength = 27
                                                case "extraAnswers":
                                                    maxLength = 10
                                                case _:
                                                    maxLength = False
                                            tournamentOptions[variableToEdit] = editList(tournamentOptions[variableToEdit], maxLength, tournamentOptions[variableToEdit])
                                        if variableType == type(dummyString):
                                            tournamentOptions[variableToEdit] = editString(tournamentOptions[variableToEdit], tournamentOptions[variableToEdit])
                                        if variableType == dummyBoolean:
                                            tournamentOptions[variableToEdit] = flipBool(tournamentOptions[variableToEdit])
                        case 2:
                            # editing competitor data
                            relevantCompetitor = getValidNumberSelection("Input the position of the competitor you wish to edit the information of:", finalOrder)
                            dictSection = competitorList[f"competitor{relevantCompetitor}"]
                            immutableCharacteristics = ["lastRound", "seed", "position", "gotBye"]
                            while True:
                                print("Here is all the data associated with that competitor:")
                                optionList = ["Nothing. Take me back!"]
                                for x in dictSection:
                                    if x in immutableCharacteristics:
                                        print(f"{x}: {dictSection[x]} (Cannot be changed)")
                                    else:
                                        print(f"{x}: {dictSection[x]}")
                                        optionList.append(x)
                                variableToEdit = getValidNumberSelection("What variable should be edited?", optionList)
                                match variableToEdit:
                                    case 1:
                                        break
                                    case _:
                                        relevantIndex = variableToEdit - 1
                                        variableToEdit = optionList[relevantIndex]
                                        variableType = type(dictSection[variableToEdit])
                                        if variableType == type(dummyString):
                                            print(f"Current value of ")
                                        if variableType == type(dummyList):
                                            dictSection[variableToEdit] = editList(dictSection[variableToEdit], False, dictSection[variableToEdit])
                                        if variableType == type(dummyString):
                                            dictSection[variableToEdit] = editString(dictSection[variableToEdit], dictSection[variableToEdit])
                                        if variableType == dummyBoolean:
                                            dictSection[variableToEdit] = flipBool(dictSection[variableToEdit])
                            competitorList[f"competitor{relevantCompetitor}"] = dictSection

                        case 3:
                            break
                    # saving updated tournament info
                    tournamentInfo["Constants"] = tournamentConstants
                    tournamentInfo["Parameters"] = tournamentOptions
                    competitorList["Tournament Info"] = tournamentInfo
                    with open(dataFileName, "w") as f:
                        json.dump(competitorList, f)
        break