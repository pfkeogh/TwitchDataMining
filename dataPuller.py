###
#David Shagam
#DataScraper for Data Mining
#Currently configured for twitch API
###

import requests
import math
import time

###
#THIS IS WHERE FUNCTIONS ARE DEFINED
##

def getJSONData(userName):
	if getUserOrChannel == "channel":
		getString = CHANNEL % userName
	elif getUserOrChannel == "user":
		getString = USER % userName

	#calculate the wait time.
	if CallsPerSecond == -1:
		#some arbitrary default
		waitTime = 1/10
	else:
		waitTime = 1/CallsPerSecond

	#first call
	response = requests.get(getString)
	while response.status_code != requests.codes.ok:
		time.sleep(waitTime)
		response = requests.get(getString)
	responseJSON = response.json()

	#num calls made and default wait time.
	numCalls = 1
	waitTime = 1

	#calculate needed calls
	totalNeededCalls = math.ceil( responseJSON["_total"]/100)
	if totalNeededCalls > limit and limit != -1:
		totalNeededCalls = limit

	print("Number of calls needed is for user", NUMPEOPLE, "is", totalNeededCalls)

	#Works for one user not for a file
	#print(TID, end="")
	if getUserOrChannel == "channel":
		outputFile.write(userName+",")
	while numCalls <= totalNeededCalls:
		for x in responseJSON["follows"]:
			if getUserOrChannel == "user":
				for y in x["channel"]:
					if y == "name":
						if x["channel"][y] != TID:
							#print("," + x["channel"][y] ,end="")
							outputFile.write(x["channel"][y]+",")
			elif getUserOrChannel == "channel":
				for y in x["user"]:
					if y == "name":
						if x["user"][y] != userName:
							#print("," + x["user"][y], end="")
							outputFile.write(x["user"][y]+",")
		time.sleep(waitTime)
		##gets json info for loop
		response = requests.get(responseJSON["_links"]["next"])
		while response.status_code != requests.codes.ok:
			time.sleep(waitTime)
			response = requests.get(responseJSON["_links"]["next"])
		responseJSON = response.json()
		numCalls = numCalls + 1
	#print()
	outputFile.write("\n")

##
#General Logic
##

#The number of API calls to be made -1 for until complete. Any ohter number is the upper limit.
limit = -1
CallsPerSecond = -1
#User = Standard user follows list. A follows B
#Channel = a channels follower list. Aka Channel A has User B following it.
getUserOrChannel = "NONE"
#channels followinglist
CHANNEL="https://api.twitch.tv/kraken/channels/%s/follows?limit=100&direction=asc"
#Users followers
USER = "https://api.twitch.tv/kraken/users/%s/follows/channels?limit=100"
readFromFile = 0
usernameOrFilePath = ""
TID = ""
outputFile = ""
outputFileName = ""
NUMPEOPLE = 1

#if we read from a file the format of the file must be TID, ITEM1, ITEM2, ..., ITEMN\n
#for example BobRoss, Sue, Joe, Billy\n
userResponse = input("Are we using a File? yes or no\n")
if userResponse.lower() == 'yes':
	readFromFile = 1
	usernameOrFilePath = input("Please type the file path\n")
	inputFile = open(usernameOrFilePath, 'r')
	#all lines of the file.
	fileLines = inputFile.read().splitlines()
else:
	#not a file grabbing by username
	usernameOrFilePath = input("Please type the username\n")
	TID = usernameOrFilePath

#deal with API caps to use with smaller subsets
userReponse = input("Is there a API cap? yes or no\n")
if userReponse.lower() == 'yes':
	limit = int(input("Please Enter the API Cap\n"))

#deal with API rate caps
CallsPerSecond = int(input("Please Enter how many calls per second may be made\n"))

#User following vs Channel's followers
userReponse = input("Are we getting a channel's followers or a user's following list? user channel\n")
if userReponse.lower() == "user":
	getUserOrChannel = "user"
else:
	getUserOrChannel = "channel"

outputFileName = input("Please insert the name of an output file\n")
print(limit, CallsPerSecond, getUserOrChannel, readFromFile, usernameOrFilePath)

#get requests once for testing
outputFile = open(outputFileName, 'w')

if readFromFile == 1:
	#loop logic here
	for x in range(0, len(fileLines)):
		lineData = fileLines[x].strip().split(",")
		TID = lineData[0];
		for y in range (1, len(lineData)-1):
			getJSONData(lineData[y])
			NUMPEOPLE = NUMPEOPLE +1
elif readFromFile == 0:
	getJSONData(TID)