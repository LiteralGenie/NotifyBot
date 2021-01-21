import logging

class TagFilter:
	def __init__(self, blacklist=None):
		self.blacklist= blacklist if blacklist else []
		self.blacklist= [[x.lower() for x in y] for y in blacklist if y]

	def filter(self, record):
		l= logging.getLogger(record.name)
		tags= [x.lower() for x in l._tags]

		if not tags:
			return True
		if any(all(x in tags for x in y) for y in self.blacklist):
			return False

		return True

# shows message + tags
class TagDebugger:
	def __init__(self, width=100):
		self.width= width

	def filter(self, record):
		l= logging.getLogger(record.name)
		tags= [x.lower() for x in l._tags]
		tags= f'[{", ".join(tags)}]'

		tmp= record.msg.split("\n")[-1]
		tmp= max(self.width-len(tmp)-len(tags), 0) + 5
		tmp= " ".join([""]*tmp)

		record.msg+= tmp + tags
		return True