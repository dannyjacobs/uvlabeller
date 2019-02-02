# UV Labeller Data

from pyuvdata import UVData
import numpy as np

# Signals
from PyQt5 import QtCore

import random

# UVData management
class Data(QtCore.QObject):
	clear = QtCore.pyqtSignal(bool)

	def __init__(self):
		super(Data, self).__init__()
		self.UV = UVData()
		self.labels = {}
		self.recentRectangle = None
		self.keywords = None
		self.notes = None

	def setFile(self,filename, idx=0):
		self.filename = filename
		self.idx = idx
		self.UV.read(self.filename)
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
		if tuple(self.currAnts) in self.pairs or (self.currAnts[1], self.currAnts[0] in self.pairs):
			self.saveRect()

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

	def updateText(self, txt, txtType):
		print(txt)
		if txtType == 0:
			self.keywords = txt
		elif txtType == 1:
			self.notes = txt

	def saveRect(self, coords=None, width=None, height=None, **kwargs):
		print('data', coords, width, height)
		if self.recentRectangle is not None:
			print(self.recentRectangle)
			self.saveLabel()
			self.clear.emit(True)
		if coords is not None:
			self.recentRectangle = [coords, width, height]
			print('data', coords, width, height)
			print(self.recentRectangle, 'saved')
		else:
			self.recentRectangle = None

	def saveLabel(self):
		keywords = self.keywords.split(',') if self.keywords is not None else None
		if self.filename not in self.labels:
			# Notes for later:
			# ask about when flipped if unique or join
			# use tuple(self.currAnts) instead? dictionaries are weird...
			self.labels[self.filename] = {(self.currAnts[0], self.currAnts[1], self.pol):
											[{'id': 0, 'keywords':keywords, 'notes':self.notes, 'rect': self.recentRectangle}]}
		elif (self.currAnts[0], self.currAnts[1], self.pol) not in self.labels[self.filename]:
			self.labels[self.filename][(self.currAnts[0], self.currAnts[1], self.pol)] = [{'id': 0, 
											'keywords':keywords, 'notes':self.notes, 'rect': self.recentRectangle}]
		else:
			nextId = self.getNextAvailableId()
			self.labels[self.filename][(self.currAnts[0], self.currAnts[1], self.pol)].append({
											'id': nextId, 'keywords':keywords, 'notes':self.notes, 'rect': self.recentRectangle})
		print(self.labels)

	def getNextAvailableId(self):
		labels = self.labels[self.filename][(self.currAnts[0], self.currAnts[1], self.pol)]
		ids = [l['id'] for l in labels]
		diff = set(ids).symmetric_difference(set(range(0, max(ids))))
		if diff == {}:
			diff = {max(ids) + 1}
		return min(diff)

	def updateLabel(self):
		pass

	def delLabel(self, filename, currAnts, pol, id):
		pass