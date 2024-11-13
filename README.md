# poll-blogger
A python program that sets up and runs single elimination tournaments on Tumblr with (hopefully) minimal human tedium

I don't know if there is a good way to ship a python virtual environment with a program so you're going to have to set up your own. I do have a nice reqirement.txt file that you should be able to use to install everything you need with pip. If you don't set up a virtual environment and/or install pytumblr2, you will be able to do everything except automatically post polls to Tumblr.

# Features
Currently, this program can do the following things:
## Setting up a competition
When you run the program, you will first be prompted to enter the round number. If you enter that the round is is negative, then you will be guided through the process of entering competitors and influencing their seeding. There can be any integer amount of competitors; byes will be automatically calculated and applied to any competitor count that is not a power of 2. Competitors that are not granted a bye will compete in round 0.

Currently, the following seeding options are available:
### 1. No Seeding
This returns the competitors in the order that they were entered in.
### 2. Random Seeding
This returns the competitors in a completely random order.
### 3. Standard Seeding
This returns the competitors, seeded in the standard way. The "standard way" is determined via a recursive pattern, where the highest seed in a round is consistently pitted against the lowest seed, and the second highest seed is consistently pitted against the second lowest seed, and so on.
### 4. Cohort Randomized Seeding
This returns the competitors in an order that follows the methodology of cohort randomized seeding, as proposed by Allen J. Schwenk [here](https://www.researchgate.net/publication/248422647_What_is_the_Correct_Way_to_Seed_a_Knockout_Tournament). Essentially, competititors are assigned to cohorts. Cohort 1 contains the first 2 competitors, cohort 2 contains the next 2 competitors, then cohorts 3 and higher are twice the size of the previous cohort (cohort 3 contains 4 competitors, cohort 4 contains 8 competitors, cohort 5 contains 16 competitors, etc.). Then, a similar recursive pattern to standard seeding is used to ensure that each competitor is consistently pitted against a random member of the largest size cohort that remains.
### 5. Equal Gap Seeding
This is Equal gap seeding, as proposed by Alexander Karpov [here](https://www.sciencedirect.com/science/article/pii/S0167637716300876). Again, this follows a recursive pattern. However, instead of consistently attempting to place the strongest competitors against the weakest competitors for as long as possible, it instead seeks to spread out pairs of competitors (1 and 2, 3 and 4, and so on) evenly throughout the list.
## Running a competition
Upon inputting a positive round or 0, the script will load all the competitors that made it to that round and list them out. From there, there are four options:
### 1. Post polls for these competitors
This option posts polls for each of the matchups. These polls can either be published, put in drafts, or put in the queue. Furthermore, it is possible to only post a certain range of polls.
#### What You Need in Order to Post Polls
In order to use the tumblr functionality of this script, you will need two things:
1. the pytumblr2 python package
2. valid tumblr API credentials

If you do not have either of those, you will not be able to automatically post polls to tumblr.
### 2. Record results of this round
This option will give you each matchup, and you will enter "1" or "2" in order to input which competitor won each matchup.

Additionally, this will automatically take you to the next round.
### 3. Render chart for this round
Renders a chart of the competition, up to the current round, and saves it as an SVG file in the directory that the python file is in.
### 4. Edit tournament and competitor data
Allows you to edit certain information about the tournament in general and for specific competitors, without editing the JSON file yourself. This includes all data that would not break the tournament if changed, such as competitor propaganda and some data about the style of the Tumblr posts tis program makes.
