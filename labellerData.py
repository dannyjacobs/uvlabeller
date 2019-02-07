# UV Labeller Data

from pyuvdata import UVData
import numpy as np

import json

# Signals
from PyQt5 import QtCore

import random

# UVData management
class Data(QtCore.QObject):
	addLabel = QtCore.pyqtSignal(str, str, int)

	def __init__(self):
		super(Data, self).__init__()
		self.UV = UVData()
		self.labels = {}
		self.recentRectangle = None
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

	def saveRect(self, coords=None, width=None, height=None, **kwargs):
		#if self.recentRectangle is not None:
		#	self.saveLabel()
		#	self.clear.emit(True)
		if coords is not None:
			self.recentRectangle = [coords, width, height]
		else:
			self.recentRectangle = None

	def saveLabel(self, keywords=None, notes=None):
		keywords = list(set(keywords.split(','))) if keywords is not None and keywords != '' else ['no group']
		newEntry = {'id': 0, 'keywords':keywords, 'notes': notes, 'rect': self.recentRectangle}
		dictID = (str(self.currAnts[0]), str(self.currAnts[0]), self.pol)
		if self.filename not in self.labels:
			# Notes for later:
			# ask about when flipped if unique or join
			# use tuple(self.currAnts) instead? dictionaries are weird...
			self.labels[self.filename] = {str(dictID):[newEntry]}
			self.updateTree(keywords, 0)
		elif str(dictID) not in self.labels[self.filename]:
			self.labels[self.filename][str(dictID)] = [newEntry]
			self.updateTree(keywords, 0)
		else:
			nextId = self.getNextAvailableId()
			self.labels[self.filename][str(dictID)].append({
								'id': nextId, 'keywords':keywords, 'notes':notes, 'rect': self.recentRectangle})
			self.updateTree(keywords, nextId)

		print(self.labels)

	def getNextAvailableId(self):
		dictID = (str(self.currAnts[0]), str(self.currAnts[0]), self.pol)
		labels = self.labels[self.filename][str(dictID)]
		ids = [l['id'] for l in labels]
		diff = set(ids).difference(set(range(0, max(ids)+1)))
		if diff == set():
			diff = {max(ids) + 1}
		return min(diff)

	def updateLabel(self):
		pass

	def delLabel(self, filename, currAnts, pol, id):
		pass

	# if file has labels
	def getLabels(self,oldLabels=None):
		if oldLabels == None and self.keys == {}:
			self.keys = {'no group': []}
			self.addLabel.emit('no group', '', 0)
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
		dictID = (str(self.currAnts[0]), str(self.currAnts[0]), self.pol)
		name = str(dictID) + str(newID)
		for k in keys:
			if k not in self.keys:
				self.keys[k] = [name]
				self.addLabel.emit(k, name, 0)
			else:
				self.keys[k].append(name)
				self.addLabel.emit(k, name, 1)

	def exportLabels(self, exportName):
		# write dictionary to json for now
		# also no order bc dictionary, again, for now
		# also need to ensure it does full path
		with open(exportName, 'w') as fp:
			json.dumps(self.labels, fp, indent=4)
