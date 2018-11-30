'''Models and their methods'''

class DB():
	'''In memory database'''
	def __init__(self):
		'''create an empty database'''
		self.incidents = []
	def drop(self):
		self.__init__()
db = DB()
class Base():
	'''class to be inherited by all other models'''
	def save(self):
		'''Add object to DB'''
		try:
			self.id = getattr(db, self.tablename)[-1]['id']+1
		except IndexError:
			self.id = 1
		current = self.current()
		getattr(db, self.tablename).append(current)
		return self.current()
	# def view(self):
	# 	'''view object as a dictionary'''
	# 	return self.current

class Incident(Base):
	'''incident models'''
	def __init__(self,title,nature,comment):
		self.id = 0
		self.title = title
		self.nature = nature
		self.comment = comment
		self.tablename = 'incidents'
	def current(self):
		'''current incidents'''
		current = {
		'title' : self.title,
		'nature' : self.nature,
		'comment' : self.comment,
		'id' : self.id
		}
		return current
	# def view(self):
	# 	'''view incidents info'''
	# 	return {
	# 	'title' : self.title,
	# 	'nature' : self.nature,
	# 	'comment' : self.comment,
	# 	'id' : self.id
	# 	}
