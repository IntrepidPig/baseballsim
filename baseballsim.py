import random
from os import listdir

print("Welcome to the ball game.")

# List of all players
players = []

# List of the two teams playing
team1 = []
team2 = []

# The player class
class Player:
	def __init__(self, name, team, batskill, catchskill, throwskill, speed):
		"""
		Parameters:
		--------------
		name : string
			name of the player
		team : string
			team the player is on
		batskill : int
			batting skill of the player from 1 - 100
		catchskill : int
			catching skill of the player from 1 - 100
		throwskill : int
			throwing skill of the player from 1 - 100
		speed : int
			speed of the player from 1 - 100
		"""
		self.name = name
		self.team = team
		self.batskill = int(batskill)
		self.catchskill = int(catchskill)
		self.throwskill = int(throwskill)
		self.speed = int(speed)
	
	"""
	Get the stats of the player as a pretty string
	"""
	def tostring(self):
		return "Name:            " + self.name + \
		       "\nTeam:            " + self.team + \
		       "\nBatting Skill:   " + str(self.batskill) + \
		       "\nCatching Skill:  " + str(self.catchskill) + \
		       "\nThrowing Skill:  " + str(self.throwskill) + \
		       "\nSpeed:           " + str(self.speed)

# The class with info for the current inning (of 9)
class Inning:
	battingteam = None
	pitcher = None
	
	def __init__(self, outfieldteamlineup, battinglineup):
		"""
		Parameters
		------------
		outfieldteamlineup : Player list
			list of the outfield team players
		battinglineup : Player list
			lineup for batters
		"""
		self.outfieldteamlineup = outfieldteamlineup;
		self.battingteam = battinglineup;
		self.pitcher = random.choice(outfieldteamlineup)
		self.batter = battinglineup[0]

# Loads the player data from files
def loadplayers():
	for filename in listdir('players'):
		playerdata = [line.rstrip('\n') for line in open('players/' + filename)]
		name = playerdata[0].split(':')[1]
		team = playerdata[1].split(':')[1]
		batskill = playerdata[2].split(':')[1]
		catchskill = playerdata[3].split(':')[1]
		throwskill = playerdata[4].split(':')[1]
		speed = playerdata[5].split(':')[1]
		players.append(Player(name, team, batskill, catchskill, throwskill, speed))

# Loads the players into teams
def loadteams():
	for player in players:
		if player.team == "Bouncing Beans":
			team1.append(player)
		else:
			team2.append(player)
	print("It's the game of the season! The " + team1[0].team + " versus " + team2[0].team + "!")

def getscore(skill):
	return skill + ((random.random() * skill / 3) - skill / 6)

battingteam = None
outfieldteam = None

# See how many bases a player runs
def run(player, batresult):
	avgcatchskill = 0
	avgthrowskill = 0
	avgspeed = 0
	for player in outfieldteam:
		avgcatchskill += player.catchskill
		avgthrowskill += player.throwskill
		avgspeed += player.speed
	avgcatchskill = avgcatchskill / len(outfieldteam)
	avgthrowskill = avgthrowskill / len(outfieldteam)
	avgspeed = avgspeed / len(outfieldteam)

	avgoutfieldskill = (avgcatchskill + avgthrowskill + avgspeed) / 3
	decidedoutfieldskill = getscore(avgoutfieldskill)

	outcomescore = ((getscore(player.speed) + batresult) / 2) - decidedoutfieldskill

	if outcomescore < 0:
		return 0
	elif outcomescore < 6:
		return 1
	elif outcomescore < 11:
		return 2
	elif outcomescore < 17:
		return 3
	else:
		return 4

# See how many bases the batter will run and run all the players currently on bases
# incomplete
def runbases(batresult):
	for player in bases:
		if player != None:
			currentbase = bases.index(player)
			distance = run(player, batresult)

# Pitch and find result
def pitch(pitcher, batter, strikes):
	pitchscore = getscore(pitcher.throwskill)
	batresult = getscore(batter.batskill)

	if pitchscore - batresult < 0:
		print("It's a hit!\n")
		#runbases(batresult)
	else:
		strikes += 1
		print("Strike " + str(strikes) + "!")
		if strikes == 3:
			print("He's out!\n")
			return
		pitch(pitcher, batter, strikes)

# Runs through an inning
def inning():
	# Pick team for outfield and batting
	outfieldteam = random.choice([team1, team2])
	if outfieldteam == team1:
		battingteam = team2;
	else:
		battingteam = team1;
	
	inning = Inning(outfieldteam, battingteam)
	
	print(battingteam[0].team + " is batting and " + outfieldteam[0].team + " is in the outfield")
	
	for batter in inning.battingteam:
		print(inning.pitcher.name + " is pitching for " + batter.name)
		pitch(inning.pitcher, batter, 0)
		
	# Switch sides
	outfieldteam, battingteam = battingteam, outfieldteam
	
	inning = Inning(outfieldteam, battingteam)
	
	print(battingteam[0].team + " is batting and " + outfieldteam[0].team + " is in the outfield")
	
	for batter in inning.battingteam:
		print(inning.pitcher.name + " is pitching for " + batter.name)
		pitch(inning.pitcher, batter, 0)
	

# Main loop controller
running = True

# Main process
loadplayers()
loadteams()
for i in range(0, 8):
	print("\n######################\nIt's inning number " + str(i + 1) + "\n######################\n")
	inning()
	typed = input()
	if typed == "quit":
		running = False
