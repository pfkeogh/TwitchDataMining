import requests
import math
import time
#The number of API calls to be made -1 for until complete. Any ohter number is the upper limit.
limit = -1
CallsPerSecond = -1
#User = Standard user follows list. A follows B
#Channel = a channels follower list. Aka Channel A has User B following it.
getUserOrChannel = "NONE"
#channels followinglist
CHANNEL="https://api.twitch.tv/kraken/channels/%s/follows?limit=100"
#Users followers
USER = "https://api.twitch.tv/kraken/users/%s/follows/channels?limit=100"
readFromFile = 0
usernameOrFilePath = ""
TID = ""
outputFileName = ""

#if we read from a file the format of the file must be TID, ITEM1, ITEM2, ..., ITEMN\n
#for example BobRoss, Sue, Joe, Billy\n
userResponse = input("Are we using a File? yes or no\n")
if userResponse.lower() == 'yes':
	readFromFile = 1
	usernameOrFilePath = input("Please type the file path\n")
	inputFile = open(usernameOrFilePath, 'r')
	#all lines of the file.
	fileLines = inputFile.read().splitlines()
	lineData = fileLines[0].strip().split(", ")
	TID = lineData[0]
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
print(limit, CallsPerSecond, getUserOrChannel, readFromFile, usernameOrFilePath)

#get requests once for testing
if getUserOrChannel == "channel":
	getString = CHANNEL % TID
	outputFileName = "%s'sFollowers" % TID
elif getUserOrChannel == "user":
	getString = USER % TID
	outputFileName = "%s'Follows" % TID

#first call
response = requests.get(getString)
responseJSON = response.json()

#num calls made and default wait time.
numCalls = 1
waitTime = 1

#calculate needed calls
totalNeededCalls = math.ceil( responseJSON["_total"]/100)
if totalNeededCalls > limit and limit != -1:
	totalNeededCalls = limit
#calculate the wait time.
if CallsPerSecond == -1:
	#some arbitrary default
	waitTime = 1/10
else:
	waitTime = 1/CallsPerSecond

print("Number of calls needed is ", totalNeededCalls)

#Works for one user not for a file
print(TID, end="")
while numCalls <= totalNeededCalls:
	for x in responseJSON["follows"]:
		for y in x["channel"]:
			if y == "name":
				print(", " + x["channel"][y] ,end="")
	time.sleep(waitTime)
	response = requests.get(responseJSON["_links"]["next"])
	responseJSON = response.json()
	numCalls = numCalls + 1
print()