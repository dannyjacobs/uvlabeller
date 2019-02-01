# UV Labeller Data

from pyuvdata import UVData
import numpy as np

import random

# UVData management
class Data():
	def __init__(self):
		self.UV = UVData()

	def setFile(self,filename):
		self.filename = filename
		self.UV.read(self.filename)
		self.pairs = self.UV.get_antpairs()
		self.ants = self.UV.get_ants()
		self.currAnts = list(self.pairs[0])
		self.pols = self.UV.get_pols()
		self.pol = self.pols[0]

	def setFiles(self,filenames):
		self.files = filenames

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
	def flagger(self):
		pass

	def saveLabels(self):
		pass