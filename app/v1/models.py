'''Models and their methods'''

class DB():
	'''In memory database'''
	def __init__(self):
		'''create an empty database'''
		self.redflag = []
	def drop(self):
		'''Drop entire database'''
		self.__init__():
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
		return self.view
	def view(self):
		'''view object as a dictionary'''
		return self.current

class Redflag(Base):
	'''redflags models'''
	def __init__(self,id,title,type,comment):
		self.id = 0
		self.title = title
		self.type = type
		self.comment = comment
	def current(self):
		'''current redflags'''
		current = {
		'title' : self.title,
		'type' : self.type,
		'comment' : self.comment,
		'id' : self.id
		}
		return current
	def view(self):
		'''view redflags info'''
		return {
		'title' : self.title,
		'type' : self.type,
		'comment' : self.comment,
		'id' : self.id
		}
		