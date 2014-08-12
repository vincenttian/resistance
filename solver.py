from argparse import ArgumentParser
from constraint import *
import colors

class Round:
	def __init__(self, fails, players):
		self.num_fails = int(fails)
		self.players = players

	def __repr__(self):
		return "%s %s" % (self.num_fails, self.players)

	def constraint(self, players):
		pass

	def is_relevant(self):
		pass


class Mission(Round):
	def constraint(self, players):
		return sum(players) <= len(players) - self.num_fails

	def is_relevant(self):
		return self.num_fails > 0

class LadyOfTheLake(Round):
	def constraint(self, players):
		if len(players) != 2:
			return True
		p1, p2 = players
		if self.num_fails == 1:
			return p1 != p2 and p1 != 1
		else:
			return p1 != 1 or p2 != 0

	def is_relevant(self):
		return True

class Parser:
	def __init__(self, inputfile):
		self.rounds = []
		self.players = []
		self.init_parser(inputfile)

	def init_parser(self, inputfile):
		lines = inputfile.readlines()
		lines = filter(lambda line: line.strip() != "", lines)
		lines = [line.strip() for line in lines]
		self.parse_nums(lines[:2])
		self.parse_players(lines[2])
		self.parse_rounds(lines[3:])

	def parse_nums(self, arr):
		for vals in arr:
			val = vals.split()
			if val[0].lower() == "spies":
				self.spy_count = int(vals[-1])
			elif val[0].lower() == "resistance":
				self.resistance_count = int(vals[-1])
			else:
				print "INPUT ERROR"

	def parse_players(self, players):
		self.players = [Player(p.strip()) for p in players.split(",")]

	def parse_rounds(self, rounds):
		for r in rounds:
			outcome, people = r.split(":")
			players = [Player(player.strip()) for player in people.split(",")]
			if len(outcome.split()) == 2:
				outcome = 0 if outcome.split()[1] == 'pass' else 1
				self.rounds.append(LadyOfTheLake(outcome, players))
			else:
				self.rounds.append(Mission(outcome, players))

	def get_args(self):
		return { "resistance" : self.resistance_count,
				 "spies" : self.spy_count,
				 "rounds" : self.rounds,
				 "players" : self.players }

class Player:
	def __init__(self, name):
		self.name = name

	def get_string_val(self, color):
		return color + str(self.name) + color

	def __repr__(self):
		return self.name

	def __eq__(self, other):
		return self.name == self.name

	def __hash__(self):
		return hash(self.name)

class Solver:
	def __init__(self, args):
		self.resistance_count = args["resistance"]
		self.spy_count = args["spies"]
		self.rounds = args["rounds"]
		self.players = args["players"]
		possibilities = self.solve()
		self.print_possiblities(possibilities)
		self.print_statistics(possibilities)

	def solve(self):
		problem = Problem()
		variables = []
		for player in self.players:
			problem.addVariable(player, [0, 1])
		problem.addConstraint(lambda *args: sum(args) == self.resistance_count)
		for round in self.rounds:
			if round.is_relevant():
				problem.addConstraint(lambda *players: round.constraint(players), round.players)
		return problem.getSolutions()

	def print_possiblities(self, possibilities):
		print "*** All Possible Combinations ***"
		for p in possibilities:
			string = ""
			for player in self.players:
				if p[player] == 1:
					string += player.get_string_val(colors.Color.BLUE)
				else:
					string += player.get_string_val(colors.Color.RED)
				string += " " + colors.Color.END
			print string

	def print_statistics(self, possibilities):
		print "*** Game Statistics ***"
		num_possiblities = len(possibilities)
		for player in self.players:
			print "There are %s out of %s combinations where %s is a resistance" % \
					(sum([p[player] for p in possibilities]), num_possiblities, player.name)

if __name__ == '__main__':
	parser = ArgumentParser(description="Finds probabilities in Resistance")
	parser.add_argument("-i", "--inputfile",
						type=file,
						required=True,
						help="input file")
	args = parser.parse_args()	
	solver = Solver(Parser(args.inputfile).get_args())

