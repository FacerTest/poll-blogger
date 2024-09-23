# poll-blogger
A python program that sets up and runs single elimination tournaments on Tumblr with (hopefully) minimal human tedium

I will immediately preface this by saying that this program is not functionally complete. **it is currently impossible to input competitor propaganda through the program**; you have to edit the competitor JSON file. But hey! You could always take fate into your own hands and do my work for me :)

Also, I don't know if there is a good way to ship a python virtual environment with a program so you're going to have to set up your own. I do have a nice reqirement.txt file that you should be able to use to install everything you need with pip.

# Features
Currently, this program can do the following things:
## Setting up a competition
When you run the program, you will first be prompted to enter the round number. If you enter that the round is 0, then you will be guided through the process of entering competitors and influencing their seeding. Currently, the following seeding options are available:
### 1. No Seeding
This returns the competitors in the order that they were entered in.
### 2. Random Seeding
This returns the competitors in a completely random order.
### 3. Standard Seeding
This returns the competitors, seeded in the standard way. The highest seed is pitted against the lowest seed, the second highest seed is pitted against the second highest seed, and so on.
### 4. Cohort Randomized Seeding
This returns the competitors in an order that follows the methodology of cohort randomized seeding, as proposed by Allen J. Schwenk [here](https://www.researchgate.net/publication/248422647_What_is_the_Correct_Way_to_Seed_a_Knockout_Tournament).
## Running a competition
Upon inputting a round other than 0, the script will load all the competitors that made it to that round and list them out. From there, there are three options:
### 1. Post polls for these competitors
This option posts polls for each of the matchups. These polls can either be published, put in drafts, or put in the queue. Furthermore, it is possible to only post a certain range of polls.
#### What You Need in Order to Post Polls
In order to use the tumblr functionality of this script, you will need two things:
1. the pytumblr2 python package
2. valid tumblr API credentials

If you do not have either of those, you will not be able to automatically post polls to tumblr.
### 2. Record results of this round
This option will give you each matchup, and you will enter "1" or "2" in order to input which competittor won each matchup.
### 3. Render chart for this round
Renders a chart of the competition, up to the current round and saves it as an SVG file.
