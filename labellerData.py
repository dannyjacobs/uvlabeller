# UV Labeller Data

from pyuvdata import UVData
import numpy as np

import random

# UVData management
class Data():
	def __init__(self):
		self.UV = UVData()
		self.labels = {}

	def setFile(self,filename, idx=0):
		self.filename = filename
		self.idx = idx
		self.UV.read(self.filename[idx])
		self.pairs = self.UV.get_antpairs()
		self.ants = self.UV.get_ants()
		self.currAnts = list(self.pairs[0])
		self.pols = self.UV.get_pols()
		self.pol = self.pols[0]

	def setFiles(self,filenames):
		self.files = filenames
		self.setFile(self.files[0])

	def nextFile(self):
		if self.files:
			idx = (self.idx + 1)%len(self.files)
			self.setFile(self.files[self.idx], idx)

	def setAnts(self,a=None,b=None):
		if a != self.currAnts[0] and a is not None:
			if (a, self.currAnts[1]) in self.pairs:
				self.currAnts = [a, self.currAnts[1]]
			elif (self.currAnts[1], a) in self.pairs:
				self.currAnts = [self.currAnts[1], a]
		if b != self.currAnts[1] and b is not None:
			if (self.currAnts[0], b) in self.pairs:
				self.currAnts = [self.currAnts[0], b]
			elif (b, self.currAnts[0]) in self.pairs:
				self.currAnts = [b, self.currAnts[0]]
		# else tooltip error

	def setPol(self, pol):
		self.pol = pol

	def saveLabel(self, keywords, notes, rectAttrib):
		if self.filename not in self.labels:
			# Notes for later:
			# ask about when flipped if unique or join
			# use tuple(self.currAnts) instead? dictionaries are weird...
			self.labels[self.filename] = {(self.currAnts[0], self.currAnts[1], self.pol):
											[{'id': 0, 'keywords':keywords, 'notes':notes, 'rect': rectAttrib}]}
		elif (self.currAnts[0], self.currAnts[1], self.pol) not in self.labels[self.filename]:
			self.labels[self.filename][(self.currAnts[0], self.currAnts[1], self.pol)] = [{'id': 0, 
											'keywords':keywords, 'notes':notes, 'rect': rectAttrib}]
		else:
			nextId = self.getNextAvailableId()
			self.labels[self.filename][(self.currAnts[0], self.currAnts[1], self.pol)].append({
											'id': nextId, 'keywords':keywords, 'notes':notes, 'rect': rectAttrib})

	def getNextAvailableId(self):
		labels = self.labels[self.filename][(self.currAnts[0], self.currAnts[1], self.pol)]
		ids = [l['id'] for l in labels]
		diff = set(a).symmetric_difference(set(range(0, max(ids))))
		if diff == {}:
			diff = {max(ids) + 1}
		return min(diff)

	def updateLabel(self):
		pass

	def delLabel(self, filename, currAnts, pol, id):
		pass