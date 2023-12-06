class Player:

	"""Player object has three states (loggedin, available, and busy)
	loggedin indicates that the user has logged in isnt searching for a game yet
	available indicates that the user is searching for a game
	busy indicates that the user is in game"""

	def __init__(self, username, conn):
		"""Constructor"""
		self.username  = username
		self.conn = conn
		self.state = "l"

	def send(self, msg):
		"""Sends msg through players conn"""
		self.conn.send(msg.encode("utf-8"))

	def setAvailable(self):
		"""Makes player state available"""
		self.state = "a"

	def setBusy(self):
		"""Make player state busy"""
		self.state = "b"

	def setLoggedIn(self):
		"""Makes player state loggedin"""
		self.state = "l"
