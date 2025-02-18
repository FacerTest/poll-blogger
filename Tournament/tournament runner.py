useDummyData = True
autoAltText = True
actuallyPost = True
dataFileName = "tournamentData.json"
bracketImageName = "bracket.svg"

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

if useDummyData == True:
    print("THE 'useDummyData' PARAMETER IS SET TO TRUE!")

# defining various functions... yahoo!
def formatStringFromJson(stringToFormat):
    # this is mostly because I do not know any other good way to make the variables you can input more universal.
    formattedString = stringToFormat.format(
        topCompetitorName=topCompetitor,
        bottomCompetitorName=bottomCompetitor,

        topCompetitorPosition=topCompetitorPosition+1,
        bottomCompetitorPosition=bottomCompetitorPosition+1,

        topCompetitorSeed=topCompetitorSeed,
        bottomCompetitorSeed=bottomCompetitorSeed,

        topCompetitorPropagandaTitle = topCompetitorDict["propagandaTitle"],
        bottomCompetitorPropagandaTitle = bottomCompetitorDict["propagandaTitle"],

        topCompetitorRounds = topCompetitorDict["involvedRounds"],
        bottomCompetitorRounds = bottomCompetitorDict["involvedRounds"],

        topCompetitorByedRounds = topCompetitorDict["byedRounds"],
        bottomCompetitorByedRounds = bottomCompetitorDict["byedRounds"],

        topCompetitorAltText = topCompetitorDict["altText"],
        bottomCompetitorAltText = bottomCompetitorDict["altText"],

        roundNumber=roundNumber,
        competitorQuantity = competitorQuantity,
        pollQuantity = int(currentRoundCompetitorQuantity/2),
        currentPoll = x+1,
        currentRoundCompetitorQuantity = currentRoundCompetitorQuantity
    )
    return formattedString

def makeIncrementingList(startValue, stopValue):
    countingList = []
    if startValue == stopValue:
        countingList.append(startValue)
    else:
        for value in range(startValue, stopValue):
            countingList.append(value)
    return countingList


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

def getValidInt(askedQuestion, minimumValue=None, maximumValue=None):
    while True:
        try:
            inputtedVariable = int(input(askedQuestion))
            if minimumValue is not None and maximumValue is not None:
                if inputtedVariable < minimumValue or inputtedVariable > maximumValue:
                    print(f"Please enter an integer in the inclusive range of {minimumValue} to {maximumValue}.")
                    continue
            elif minimumValue is not None:
                if inputtedVariable < minimumValue:
                    print(f"Please enter an integer greater than or equal to {minimumValue}.")
                    continue
            elif maximumValue is not None:
                if inputtedVariable > maximumValue:
                    print(f"Please enter an integer less than or equal to {maximumValue}.")
                    continue
            break
        except ValueError:
            print("Please type a valid integer!")
    return inputtedVariable

def editList(listToEdit, listName, maximumLength=None):
    print(f"Editing the list {listName}")
    while True:
        print("Here are the entries, arranged by their list index:")
        if len(listToEdit) == 0:
            print("(there are no entries)")
        else:
            prettyPrintList(listToEdit, 0)
        listEditMethod = getValidNumberSelection("\nWhat do you want to do?", ["Go Back", "Delete Entry", "Edit Entry", "Add Entry"])
        match listEditMethod:
            case 1:
                break
            case 2:
                relevantIndex = getValidInt("Enter the index of the entry you wish to delete.\n(type a negative index to clear the list)\n", len(listToEdit)-1)
                if relevantIndex < 0:
                    if ynQuestion("Are you sure you want to clear this list? (y/n)\n") == True:
                        print("OK! Clearing the list...")
                        listToEdit = []
                    else:
                        print("OK! NOT clearing the list...")
                else:
                    listToEdit.pop(relevantIndex)
            case 3:
                relevantIndex = getValidInt("Enter the index of the entry you wish to edit.\n", 0, len(listToEdit)-1)
                listToEdit[relevantIndex] = input(f"What would you like the entry at {relevantIndex} to say?")
            case 4:
                if maximumLength is None:
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

def editString(stringToEdit, stringName, minimumLength=None, maximumLength=None):
    while True:
        print(f"Current value of {stringName}:")
        if len(stringToEdit) > 0:
            print(f"\"{stringToEdit}\"")
        else:
            print("\"\" (nothing)")
        inputtedVariable = input("What should its new value be?\n")
        if minimumLength is not None and maximumLength is not None:
            if len(inputtedVariable) < minimumLength or len(inputtedVariable) > maximumLength:
                print(f"Please enter a string with a character count in the inclusive range of {minimumLength} to {maximumLength}.")
                continue
        elif minimumLength is not None:
            if len(inputtedVariable) < minimumLength:
                print(f"Please enter a string with a character count greater than or equal to {minimumLength}.")
                continue
        elif maximumLength is not None:
            if len(inputtedVariable) > maximumLength:
                print(f"Please enter a string with a character count less than or equal to {maximumLength}.")
                continue
        break
    return stringToEdit

def flipBool(boolToFlip):
    if boolToFlip == True:
        boolToFlip = False
    else:
        boolToFlip = True
    return boolToFlip

def getValidNumberSelection(askedQuestion, optionList, zeroOffset=1):
    validAnswers = []
    for options in range(len(optionList)):
        validAnswers.append(options+zeroOffset)
    while True:
        try:
            print(askedQuestion)
            for x in range(len(optionList)):
                print(f"{x+zeroOffset}. {optionList[x]}")
            inputtedVariable = int(input(""))
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
            client = pytumblr2.TumblrRestClient(
                consumerKey,
                consumerSecret,
                oauthToken,
                oauthSecret
            )
            client.info()
        else:
            clientInfo = {"hasCredentials": False}
        # dunno how I feel about storing this stuff in plaintext... but it's not like there's anything else I can really do
        with open("credentials.json", "w") as f:
            json.dump(clientInfo, f, indent=2)
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
    response = False
    try:
        competitorList = json.load(r)
    except json.decoder.JSONDecodeError:
        print("The tournament data file can't be read!")
        response = ynQuestion("Do you want to delete it? (y/n)\n(If not, the program will probably crash very soon!)\n")
    r.close()
    if response == True:
        os.remove(dataFileName)
        dataFileExists = False
except FileNotFoundError:
    dataFileExists = False

# automatically starting a new competition if there is no file
if dataFileExists == False:
    roundNumber = -1
# coming to terms with the file existing
else:
    while True:
        response = getValidNumberSelection("Would you like to continue the current competition or create a new one?", ["Continue the current competition", "Start a new competition"])
        match response:
            case 1:
                # getting the list of valid rounds
                allowedRounds = []
                allowedRoundsExclusive = []
                minimumExclusiveRound = 0
                for x in range(len(competitorList)-1):
                    dictSection = competitorList[f"competitor{x+1}"]
                    for y in dictSection["involvedRounds"]:
                        if y not in allowedRounds:
                            allowedRounds.append(y)
                        if y != min(dictSection["involvedRounds"]):
                            if y not in allowedRoundsExclusive:
                                allowedRoundsExclusive.append(y)
                
                if len(allowedRoundsExclusive)>0:
                    orderedValidRounds = makeIncrementingList(min(allowedRounds), max(allowedRoundsExclusive)+1)
                else:
                    orderedValidRounds = [min(allowedRounds)]

                # back to getting a list of rounds
                prettyValidRounds = []
                for x in orderedValidRounds:
                    prettyValidRounds.append(f"Round {x}")
                roundNumber = getValidNumberSelection("What round is it?", prettyValidRounds, orderedValidRounds[0])
                break
            case 2:
                if ynQuestion("Are you sure? The current tournament will be deleted! (y/n)\n") == True:
                    print("OK! Deleting the file...")
                    os.remove(dataFileName)
                    roundNumber = -1
                    break

# starting a new tournament
if roundNumber < 0:
    startedNewTournament = True
    print("Starting a new tournament!")
    # setting a bunch of random default data
    tournamentType = "Single Elimination"
    pollQuestion = "Which competitor deserves to win this competition the most?"
    pollTags = ["tumblr tournament", "poll", "polls", "round {roundNumber}", "{topCompetitorName}", "{bottomCompetitorName}"]
    propagandaPlaceholder = "(no propaganda submitted)"
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
    if competitorQuantity == 2:
        finalRound = 1
    else:
        finalRound = -1
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
        print("OK! Put images in the /assets directory of wherever you have this python file!")
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
            print("OK! Put the image you want to use in the /assets directory of wherever you have this python file!")
            headerStyle = "image"
            headerText = False
            needsImageDirectory = True

    # creating dummy post content
    postFormat = []
    # dealing with headings...
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
            postFormat.append({
                "type":"image",
                "known_file_type": False,
                "media": [{
                    "type": "images/png",
                    "identifier": "heading"
                }],
                "alt_text": "Header"
            })
    
    print(f"Blocks before poll: {blocksBeforePoll}")
    # dealing with competitor images...
    if useCompetitorImages == True:
        imageBlocks = [blocksBeforePoll, blocksBeforePoll+1]
        blocksBeforePoll = blocksBeforePoll+2
        postFormat.append({
                "type":"image",
                "media": [{
                    "type": "images/png",
                    "identifier": "topCompetitor"
                }],
                "alt_text": "{topCompetitorAltText}"
        })
        postFormat.append({
                "type":"image",
                "media": [{
                    "type": "images/png",
                    "identifier": "bottomCompetitor"
                }],
                "alt_text": "{bottomCompetitorAltText}"
        })
    else:
        imageBlocks = []

    # setting up poll
    postFormat.append({
        "type": "poll",
        "question": pollQuestion,
        "client_id": "Tumblr asks you to give a poll UUID, but then ignores it and creates its own. Isn't that odd?",
        "answers": [{"answer_text": "{topCompetitorName}"}, {"answer_text": "{bottomCompetitorName}"}],
        "settings":{
            "closed_status": "closed-after",
            "expire_after": 0
        }
    })
  
    # propaganda and relevant titles
    postFormat.append({
        "type": "text",
        "text": "{topCompetitorPropagandaTitle}",
        "subtype": "heading2"
    })

    postFormat.append({
        "type": "propaganda",
        "propaganda": "top"
    })

    postFormat.append({
        "type": "text",
        "text": "{bottomCompetitorPropagandaTitle}",
        "subtype": "heading2"
    })
    postFormat.append({
        "type": "propaganda",
        "propaganda": "bottom"
    })

    totalBlocks = len(postFormat)

    # setting up dummy layout
    display = []
    block = 0
    while block < totalBlocks:
        if block in imageBlocks:
            display.append({
                "blocks": [block, block+1]
            })
            block = block + 2
        else:
            display.append({
                "blocks": [block]
            })
            block = block+1
    postLayout = [
        {
            "type": "rows",
            "display": display,
            "truncate_after": blocksBeforePoll
        }
    ]

    # setting up dummy media sources
    postMediaSources = {}
    if headerStyle == "image":
        postMediaSources["heading"] = "assets/header"
    if useCompetitorImages == True:
        postMediaSources["topCompetitor"] = "assets/{topCompetitorPosition}"
        postMediaSources["bottomCompetitor"] = "assets/{bottomCompetitorPosition}"

    #all this "dummy" stuff... it's purely for the purpose of setting up a, well, "dummy" pseudo-npf post that the program understands...
    #all the logic for converting this into an actual tumblr post is lower down

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
                "placeholderImageAltText": "Unknown",
                "defaultPropaganda": propagandaPlaceholder,
                "postData": {
                    "content": postFormat,
                    "layout": postLayout,
                    "mediaSources": postMediaSources,
                    "postTags": pollTags
                }
            }
        }
    }
    finalOrder = []
    for x in range(len(finalSeedList)):
        altText = f"{competitorNames[int(finalSeedList[x]-1)]}"
        if finalSeedList[x] in seedsToBye:
            startRound = 1
            gotBye = [0]
        else:
            startRound = 0
            gotBye = []
        dictSection = {
        "position": x+1,
        "seed": finalSeedList[x],
        "involvedRounds": [startRound],
        "byedRounds": gotBye,
        "name": competitorNames[int(finalSeedList[x]-1)],
        "propagandaTitle": propagandaTitles[int(finalSeedList[x]-1)],
        "propaganda":[],
        "altText": altText
        }
        competitorList["competitor"+str(x+1)] = dictSection
        finalOrder.append(competitorNames[int(finalSeedList[x]-1)])
    competitorDict = json.dumps(competitorList, indent=2)
    w = open(dataFileName, "w")
    w.write(competitorDict)
    w.close()
    roundNumber = lowestRound


# dealing with a competition in progress
if roundNumber >= 0:
    # loading competition data
    f = open(dataFileName)
    competitorList = json.load(f)
    f.close()
    # this sucks. it is so bad. unfortuanately i am recovering from being chokeslammed so i can't write something better
    f = open(dataFileName)
    competitorListCloneForSafekeeping = json.load(f)
    f.close()
    tournamentInfo = competitorList["Tournament Info"]
    tournamentOptions = tournamentInfo["Parameters"]
    tournamentConstants = tournamentInfo["Constants"]
    competitorQuantity = len(competitorList)-1

    totalRounds = tournamentConstants["totalRounds"]
    competitionType = tournamentConstants["type"]
    placehoderImageAltText = tournamentOptions["placeholderImageAltText"]
    propagandaPlaceholder = tournamentOptions["defaultPropaganda"]
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
        originalSeedList.append(dictSection["seed"])
        originalNameList.append(dictSection["name"])
        if 0 in dictSection["byedRounds"]:
            print(f"competitor {x} is byed from round 0!")
            byes = byes+1
            notByed.append(False)
            notByed.append(False)
        else:
            print(f"competitor {x} exists and doesn't have a bye this round!")
            notByed.append(dictSection["name"])
        if max(dictSection["involvedRounds"]) >= roundNumber:
            if roundNumber not in dictSection["byedRounds"]:
                competitorCounter = competitorCounter + 1
                finalOrder.append(dictSection["name"])
                finalOrderPos.append(dictSection["position"])
                finalSeedList.append(dictSection["seed"])
    currentRoundCompetitorQuantity = len(finalOrder)
    print(f"Here are all the competitors that are in round {roundNumber}:")
    prettyPrintList(finalOrder, 1)

    if len(finalOrder) == 1:
        finalRoundSelected = True
    else:
        finalRoundSelected = False

    
    while True:
        if finalRoundSelected == True:
            selection = getValidNumberSelection("\nThis is the final round! What do you want to do?", ["Render chart for this round", "Edit tournament and competitor data"])
            response = selection+2
        else:
            response = getValidNumberSelection("\nWhat do you want to do?", ["Post polls for these competitors", "Record results of this round", "Render chart for this round", "Edit tournament and competitor data"])
        match response:
            case 1:
                # posting polls for existing matchup
                selection = getValidNumberSelection("How long do you want the poll to run for?", ["1 Day", "3 Days", "7 Days (1 Week)"])
                secondsPerDay = 86400
                # Unfortunately Tumblr caps you at having a poll for exactly 7 days, 3 days, or 1 day :(
                # this implementation is mostly since I don't wanna have to go through all the work of pulling up a calculator and putting numbers in... alas
                match selection:
                    case 1:
                        pollTimeLength = secondsPerDay
                    case 2:
                        pollTimeLength = 3 * secondsPerDay
                    case 3:
                        pollTimeLength = 7 * secondsPerDay
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
                selection = getValidNumberSelection("What should happen to these polls?", ["Immediately publish them", "Save them as drafts", "Put them in the queue"])
                match selection:
                    case 1:
                        postMethod = "published"
                    case 2:
                        postMethod = "draft"
                    case 3:
                        postMethod = "queue"
                for x in range(firstMatchup-1, lastMatchup):
                    matchupPos = 2*x
                    topCompetitor = finalOrder[matchupPos]
                    topCompetitorSeed=finalSeedList[matchupPos]
                    bottomCompetitor = finalOrder[matchupPos+1]
                    bottomCompetitorSeed = finalSeedList[matchupPos+1]

                    topCompetitorDict={}
                    bottomCompetitorDict={}

                    topCompetitorPosition = originalSeedList.index(topCompetitorSeed)
                    topCompetitorDict = competitorList[f"competitor{topCompetitorPosition+1}"]
                    bottomCompetitorPosition = originalSeedList.index(bottomCompetitorSeed)
                    bottomCompetitorDict = competitorList[f"competitor{bottomCompetitorPosition+1}"]

                    print(f"Match {x+1}:\n{topCompetitor} vs. {bottomCompetitor}\n")
                    
                    # convert dummy post format to actual tumblr NPF
                    dummyPostData = tournamentOptions["postData"]

                    # converting tags
                    actualPostTags = []
                    for y in dummyPostData["postTags"]:
                        actualPostTags.append(formatStringFromJson(y))

                    # converting post content
                    expandedRanges = {}
                    loopNumber = 0
                    actualPostContent = []
                    # WHY IS IT OVERWRITING THE DUMMY VALUES???? I am going to chokeslam whoever designed this system.
                    for y in range(len(competitorList["Tournament Info"]["Parameters"]["postData"]["content"])):
                        
                        competitorList = competitorListCloneForSafekeeping
                        dummyBlock = dummyPostData["content"][y]

                        match dummyBlock["type"]:
                            case "text":
                                dummyBlock["text"] = formatStringFromJson(competitorList["Tournament Info"]["Parameters"]["postData"]["content"][y]["text"])
                            case "image":
                                dummyBlock["alt_text"] = formatStringFromJson(competitorList["Tournament Info"]["Parameters"]["postData"]["content"][y]["alt_text"])
                                if findFile(formatStringFromJson(dummyPostData["mediaSources"][dummyBlock['media'][0]["identifier"]]), validTumblrImageFileFormats) == False:
                                    dummyBlock["alt_text"] = formatStringFromJson(competitorList["Tournament Info"]["Parameters"]["placeholderImageAltText"])
                            case "poll":
                                dummyAnswers = []
                                for z in range(len(dummyBlock["answers"])):
                                    answerSection = dummyBlock["answers"][z]
                                    answerSection["answer_text"]=formatStringFromJson(competitorList["Tournament Info"]["Parameters"]["postData"]["content"][y]["answers"][z]["answer_text"])
                                    dummyAnswers.append(answerSection)
                                dummyBlock["answers"] = dummyAnswers
                                dummyBlock["question"] = formatStringFromJson(competitorList["Tournament Info"]["Parameters"]["postData"]["content"][y]["question"])
                                dummyBlock["settings"]["expire_after"] = pollTimeLength
                            case "propaganda":
                                initialBlock = loopNumber
                                expandedRanges[loopNumber] = {
                                    "createNewRows": True,
                                    "initialPosition": initialBlock
                                }
                                additionalBlocks = 0
                                match dummyBlock["propaganda"]:
                                    case "top":
                                        if len(topCompetitorDict["propaganda"]) == 0:
                                            dummyBlock = {"type": "text", "text": tournamentOptions["defaultPropaganda"]}
                                        else:
                                            additionalBlocks = len(topCompetitorDict["propaganda"])-1
                                            for z in range(len(topCompetitorDict["propaganda"])):
                                                propagandaSection = topCompetitorDict["propaganda"][z]
                                                actualPostContent.append({"type": "text", "text": f"“{propagandaSection}”"})
                                        expandedRanges[loopNumber]["finalPosition"]=initialBlock+additionalBlocks
                                        expandedRanges[loopNumber]["additionalBlocks"]=additionalBlocks
                                    case "bottom":
                                        if len(bottomCompetitorDict["propaganda"]) == 0:
                                            dummyBlock = {"type": "text", "text": tournamentOptions["defaultPropaganda"]}
                                        else:
                                            additionalBlocks = len(bottomCompetitorDict["propaganda"])-1
                                            for z in range(len(bottomCompetitorDict["propaganda"])):
                                                propagandaSection = bottomCompetitorDict["propaganda"][z]
                                                actualPostContent.append({"type": "text", "text": f"“{propagandaSection}”"})
                                        expandedRanges[loopNumber]["finalPosition"]=initialBlock+additionalBlocks
                                        expandedRanges[loopNumber]["additionalBlocks"]=additionalBlocks
                            case _:
                                pass
                        if dummyBlock["type"] != "propaganda":
                            actualPostContent.append(dummyBlock)
                        loopNumber = loopNumber+1

                    # fixing layout...
                    if len(expandedRanges) == 0:
                        actualPostLayout = dummyPostData["layout"]
                    else:
                        actualPostLayout = []
                        expansionPositions = []
                        lastBlock=-1
                        for y in expandedRanges:
                            expansionPositions.append(y)
                        for y in dummyPostData["layout"]:
                            # this is a list for whatever reason...
                            layoutSection = y
                            sectionDisplay = []
                            try:
                                initialTruncateAfterBlock = layoutSection["truncate_after"]
                            except KeyError:
                                initialTruncateAfterBlock = False
                            for z in y["display"]:
                                blocksThisRow = 0
                                currentRow = []
                                for block in z["blocks"]:
                                    blocksThisRow = blocksThisRow+1
                                    if block in expansionPositions:
                                        if expandedRanges[block]["createNewRows"] == False:
                                            standardRowAdding = True
                                            blocksThisRow = blocksThisRow+expandedRanges[block]["additionalBlocks"]
                                        else:
                                            standardRowAdding = False
                                            for newBlocks in range(expandedRanges[block]["additionalBlocks"]+1):
                                                lastBlock = lastBlock+1
                                                sectionDisplay.append({"blocks": [lastBlock]})
                                    else:
                                        standardRowAdding = True
                                if standardRowAdding == True:
                                    for block in range(blocksThisRow):
                                        lastBlock = lastBlock+1
                                        currentRow.append(lastBlock)
                                    sectionDisplay.append({"blocks": currentRow})
                            layoutSection["display"]=sectionDisplay
                            if initialTruncateAfterBlock is not False:
                                truncateOffset = 0
                                for z in expansionPositions:
                                    if z <= initialTruncateAfterBlock:
                                        truncateOffset=truncateOffset+expandedRanges[z]["additionalBlocks"]
                                layoutSection["truncate_after"] = layoutSection["truncate_after"] + truncateOffset
                            actualPostLayout.append(layoutSection)

                    # setting up media sources...
                    actualMediaSources = {}
                    for y in dummyPostData["mediaSources"]:
                        foundFile = findFile(formatStringFromJson(dummyPostData["mediaSources"][y]), validTumblrImageFileFormats)
                        if foundFile == False:
                            foundFile = findFile("assets/placeholder", validTumblrImageFileFormats)
                        actualMediaSources[y] = foundFile

                    # creating post
                    if actuallyPost == True:
                        if len(actualPostTags) > 0:
                            client.create_post(
                                blogname=postedBlog,
                                tags= actualPostTags,
                                state= postMethod,
                                content = actualPostContent,
                                layout = actualPostLayout,
                                media_sources = actualMediaSources
                            )
                        else:
                            client.create_post(
                                blogname=postedBlog,
                                state= postMethod,
                                content = actualPostContent,
                                layout = actualPostLayout,
                                media_sources = actualMediaSources
                            )
                    else:
                        print("Tags:")
                        prettyPrintList(actualPostTags, 1)
                        print("Post content:")
                        prettyPrintList(actualPostContent, 1)
                        print("Layout:")
                        prettyPrintList(actualPostLayout, 1)
                        print("Media sources:")
                        for y in actualMediaSources:
                            print(f"{y}: {actualMediaSources[y]}")                            
                break
            case 2:
                # updating matchup
                print("OK! just type the number next to the WINNING competitor!")
                for x in range(int(currentRoundCompetitorQuantity/2)):
                    stayingList = [makeIncrementingList(competitorList[f"competitor{finalOrderPos[x*2]}"]["involvedRounds"][0], roundNumber+1), makeIncrementingList(competitorList[f"competitor{finalOrderPos[1+(x*2)]}"]["involvedRounds"][0], roundNumber+1)]
                    progressingList = [makeIncrementingList(competitorList[f"competitor{finalOrderPos[x*2]}"]["involvedRounds"][0], roundNumber+2), makeIncrementingList(competitorList[f"competitor{finalOrderPos[1+(x*2)]}"]["involvedRounds"][0], roundNumber+2)]
                    selection = getValidNumberSelection(f"Matchup {x + 1} of {int(currentRoundCompetitorQuantity/2)}:", [finalOrder[2*x], finalOrder[1+(2*x)]])
                    match selection:
                        case 1:
                            competitorList[f"competitor{finalOrderPos[x*2]}"]["involvedRounds"] = progressingList[0]
                            competitorList[f"competitor{finalOrderPos[1+(x*2)]}"]["involvedRounds"] = stayingList[1]
                        case 2:
                            competitorList[f"competitor{finalOrderPos[x*2]}"]["involvedRounds"] = stayingList[0]
                            competitorList[f"competitor{finalOrderPos[1+(x*2)]}"]["involvedRounds"] = progressingList[1]
                competitorDict = json.dumps(competitorList, indent=2)
                f = open(dataFileName, "w")
                f.write(competitorDict)
                roundNumber = roundNumber + 1
                finalOrder = []
                finalOrderPos = []
                finalSeedList = []
                for x in range(competitorQuantity):
                        dictSection = competitorList[f"competitor{x+1}"]
                        if max(dictSection["involvedRounds"]) >= roundNumber:
                            finalOrder.append(dictSection["name"])
                            finalOrderPos.append(dictSection["position"])
                            finalSeedList.append(dictSection["seed"])
                currentRoundCompetitorQuantity = len(finalOrder)
                print(f"\nAnd here is the updated competitor list, for round {roundNumber}:")
                for x in range(len(finalOrder)):
                    print(f"{x+1}. {finalOrder[x]}")
                if len(finalOrder) == 1:
                    finalRound = roundNumber
                    finalRoundSelected = True
                    print(f"Round {roundNumber} is the final round!")
            case 3:
                # finding the longest name
                firstRoundCompetitors = []
                maxNameLength = 5
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
                horizontalCompetitorSpacing = (lengthPerCharacterSize+2)*maxNameLength
                # setting up a grid where every possible matchup is on...
                alternatingFactor = 1
                for x in range(1,(4*(int(totalRounds)+1))-2):
                    if x == 2*(int(totalRounds)+1)-1:
                        alternatingFactor = 0
                    if x % 2 == alternatingFactor:
                        possibleXPositions.append(lastXPos+horizontalCompetitorSpacing)
                    else:
                        possibleXPositions.append(lastXPos+5*(lengthPerCharacterSize+2))
                    lastXPos = possibleXPositions[-1]
                for x in range(1,int((powerOf2UpperBound))+1):
                    possibleYPositions.append(deadspaceWidth+(x*verticalCompetitorSpacing))
                imageHeight = deadspaceWidth+ possibleYPositions[-1]
                imageLength = possibleXPositions[-2] + deadspaceWidth
                svgMarkup =f'<svg width="{imageLength}" height="{imageHeight}" xmlns="http://www.w3.org/2000/svg">\n<rect width="{imageLength}" height="{imageHeight}" x="0" y ="0" fill="white" />\n'
                rounds = {}
                if byes == competitorQuantity:
                    pretendRoundNumber = roundNumber - 1
                    rounds[0] = originalNameList
                else:
                    pretendRoundNumber = roundNumber
                    rounds[0]= notByed
                for x in range(1, totalRounds+2):
                    roundList = []
                    if x <= pretendRoundNumber:
                        for z in range(competitorQuantity):
                            dictSection=competitorList[f"competitor{z+1}"]
                            if pretendRoundNumber == roundNumber:
                                if max(dictSection["involvedRounds"]) >= x:
                                    roundList.append(dictSection["name"])
                            else:
                                if max(dictSection["involvedRounds"]) > x:
                                    roundList.append(dictSection["name"])
                    else:
                        for y in range(competitorQuantity):
                            roundList.append("")
                    rounds[x] = roundList
                #defining relevant nodes
                possiblyRelevantNodes = {}
                leftSide = True
                universalNodeID = 0
                posInLayer = []
                nodeIDList = []
                maxLevel = int(len(possibleXPositions)/4)
                for x in range(maxLevel+1):
                    posInLayer.append(0)
                for x in range(int(len(possibleXPositions)/2)):
                    layer = int(len(possibleXPositions)/4)-abs(x-int(len(possibleXPositions)/4))
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
                                    "posInLayer": posInLayer[layer],
                                    "side": "middle",
                                    "layer": maxLevel
                                }
                            else:
                                possiblyRelevantNodes[universalNodeID] = {
                                    "xPos": 2*x,
                                    "yPos": y,
                                    "posInLayer": posInLayer[layer],
                                    "side": side,
                                    "layer": layer
                                }
                            nodeIDList.append(universalNodeID)
                            universalNodeID = universalNodeID+1
                            posInLayer[layer] = posInLayer[layer] + 1
                        else:
                            nodesToSkip = nodesToSkip - 1
                relevantNodes = {}
                for x in possiblyRelevantNodes:
                    node = possiblyRelevantNodes[x]
                    if node["layer"] == 0:
                        if rounds[0][node["posInLayer"]] == False:
                            pass
                        else:
                            node["competitor"] = rounds[0][node["posInLayer"]]
                            relevantNodes[x] = node
                    else:
                        try:
                            node["competitor"] = rounds[node["layer"]][node["posInLayer"]]
                            relevantNodes[x] = node
                        except IndexError:
                            pass
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
                # adding names, drawing lines, then putting dots on top
                svgMarkup += f'<line x1="{possibleXPositions[int(len(possibleXPositions)/2)-1]}" y1="{possibleYPositions[int(len(possibleYPositions)/2)+centerNodeOffset]}" x2="{possibleXPositions[int(len(possibleXPositions)/2)-1]}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                svgMarkup += f'<line x1="{possibleXPositions[int((len(possibleXPositions))/2)-1]-horizontalCompetitorSpacing}" y1="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" x2="{possibleXPositions[int((len(possibleXPositions))/2)-1]+horizontalCompetitorSpacing}" y2="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset]}" style="stroke:black;stroke-width:{lineWidth}"/>\n'
                for x in range(len(nodesByLayer)-1):
                    currentLayer = nodesByLayer[x]
                    nextLayer = nodesByLayer[x+1]
                    for y in range(len(currentLayer)):
                        currentNodeID = currentLayer[y]
                        try:
                            currentNode = relevantNodes[currentNodeID]
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
                            svgMarkup += f'<text x="{int((possibleXPositions[currentNode["xPos"]]+ possibleXPositions[int((currentNode["xPos"]+nextNode["xPos"])/2)])/2)}" y="{possibleYPositions[currentNode["yPos"]-1]+int(fontSize/2)}" fill="black" text-anchor="middle" stroke="black" font-size="{fontSize}">{textToRender}</text>\n'
                            if len(finalOrder) == 1:
                                competitionVictor = finalOrder[0]
                                svgMarkup += f'<text x="{int(imageLength/2)}" y="{possibleYPositions[int(len(possibleYPositions)/2)-centerNodeOffset-1]+lineWidth}" fill="black" stroke="black" text-anchor="middle" font-size="{2*fontSize}">{str(competitionVictor)}</text>\n'
                        else:
                            pass
                for x in relevantNodes:
                    node = possiblyRelevantNodes[x]
                    svgMarkup += f'<circle cx="{possibleXPositions[node["xPos"]]}" cy="{possibleYPositions[node["yPos"]]}" r="{pointRadius}" fill="black" />\n'
                svgMarkup += '</svg>'
                try:
                    f = open(bracketImageName, "x")
                except FileExistsError:
                    os.remove(bracketImageName)
                    f = open(bracketImageName, "x")
                w = open(bracketImageName, "w")
                w.write(str(svgMarkup))
                w.close()
                print(f'Saved bracket image to "{bracketImageName}"')
                break
            case 4:
                # updating tournament data
                print("Sorry! This feature is currently disabled.\nYou can always edit values via the JSON file itself until this functionality is restored.")