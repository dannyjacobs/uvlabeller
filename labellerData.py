# UV Labeller Data

from pyuvdata import UVData
import numpy as np

# Signals
from PyQt5 import QtCore

import random

# UVData management
class Data(QtCore.QObject):
	clear = QtCore.pyqtSignal(bool)
	addLabel = QtCore.pyqtSignal(str, str, int)

	def __init__(self):
		super(Data, self).__init__()
		self.UV = UVData()
		self.labels = {}
		self.recentRectangle = None
		self.keywords = None
		self.notes = None
		self.keys = {}

	def setFile(self,filename, idx=0):
		self.filename = filename
		self.idx = idx
		self.UV.read(self.filename)
		self.pairs = self.UV.get_antpairs()
		self.ants = self.UV.get_ants()
		self.currAnts = list(self.pairs[0])
		self.pols = self.UV.get_pols()
		self.pol = self.pols[0]
		self.getLabels(None) # eventually will have someway to get saved labels

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
		if self.recentRectangle is not None:
			self.saveLabel()
			self.clear.emit(True)
		if coords is not None:
			self.recentRectangle = [coords, width, height]
		else:
			self.recentRectangle = None

	def saveLabel(self):
		keywords = list(set(self.keywords.split(','))) if self.keywords is not None else ['no group']
		newEntry = {'id': 0, 'keywords':keywords, 'notes':self.notes, 'rect': self.recentRectangle}
		if self.filename not in self.labels:
			# Notes for later:
			# ask about when flipped if unique or join
			# use tuple(self.currAnts) instead? dictionaries are weird...
			self.labels[self.filename] = {(self.currAnts[0], self.currAnts[1], self.pol):[newEntry]}
			self.updateTree(keywords, 0)
		elif (self.currAnts[0], self.currAnts[1], self.pol) not in self.labels[self.filename]:
			self.labels[self.filename][(self.currAnts[0], self.currAnts[1], self.pol)] = [newEntry]
			self.updateTree(keywords, 0)
		else:
			nextId = self.getNextAvailableId()
			self.labels[self.filename][(self.currAnts[0], self.currAnts[1], self.pol)].append({
								'id': nextId, 'keywords':keywords, 'notes':self.notes, 'rect': self.recentRectangle})
			self.updateTree(keywords, nextId)

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

	# if file has labels
	def getLabels(self,oldLabels=None):
		if oldLabels == None and self.keys == {}:
			self.keys = {'no group': ''}
		else:
			keys = {}
			for t in oldLabels[self.filename]: #tuples
				for l in oldLabels[self.filename][t]: #label
					for k in oldLabels[self.filename][t][l]['keywords']:
						if k not in keys:
							keys[k] = [str(oldLabels[self.filename][t]) + str(oldLabels[self.filename][t][l]['keywords']['id'])]
						else:
							keys[k].append(str(oldLabels[self.filename][t]) + str(oldLabels[self.filename][t][l]['keywords']['id']))
			self.keys = keys

	# adding new labels
	def updateTree(self, keys, newID):
		label = str(self.currAnts[0], self.currAnts[1], self.pol) + str(newID)
		for k in keys:
			if k not in self.keys:
				self.keys[k] = [label]
				self.addLabel.emit(k, label, 0)
			else:
				self.keys[k].append(label)
				self.addLabel.emit(k, label, 1)

