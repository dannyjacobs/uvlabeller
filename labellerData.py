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
    	""" Initialize the session's data object."""
        super(Data, self).__init__()
        self.UV = UVData()
        self.labels = {}
        self.recentRectangle = None
        self.notes = None
        self.keys = {}

    def setFile(self, filename, idx=0):
    	""" Update data object based on the file attributes. """
        self.filename = filename
        self.idx = idx
        self.UV.read(self.filename)
        self.pairs = self.UV.get_antpairs()
        self.ants = self.UV.get_ants()
        self.currAnts = list(self.pairs[0])
        self.pols = self.UV.get_pols()
        self.pol = self.pols[0]
        self.getLabels(None)
        # eventually will have someway to get saved labels

    def setFiles(self, filenames):
    	""" Retain list of files to be opened."""
        self.files = filenames
        self.setFile(self.files[0])

    def nextFile(self):
    	""" Open the next file. """
        if self.files:
            idx = (self.idx + 1) % len(self.files)
            self.setFile(self.files[self.idx], idx)

    def setAnts(self, a=None, b=None):
    	""" Set the baseline. """
        if tuple(self.currAnts) in self.pairs or (
                self.currAnts[1], self.currAnts[0] in self.pairs):
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
    	""" Set the polarization. """
        self.pol = pol

    def saveRect(self, coords=None, width=None, height=None, **kwargs):
    	""" Retain recent annotation attributes. """
        if coords is not None:
            self.recentRectangle = [coords, width, height]
        else:
            self.recentRectangle = None

    def saveLabel(self, keywords=None, notes=None):
    	""" Save the annotation and its label information. """
        # how protect when not labeling?
        # if self.recentRectangle is not none?
        keywords = list(set(keywords.split(','))) if keywords is not \
            None and keywords != '' else ['no group']
        keywords = [k.strip() for k in keywords]
        newEntry = {'id': 0, 'keywords': keywords, 'notes': notes,
                    'rect': self.recentRectangle}
        dictID = (str(self.currAnts), self.pol)
        if self.filename not in self.labels:
            # Notes for later:
            # ask about when flipped if unique or join
            # use tuple(self.currAnts) instead? dictionaries are weird...
            self.labels[self.filename] = {str(dictID): [newEntry]}
            self.updateTree(keywords, 0)
        elif str(dictID) not in self.labels[self.filename]:
            self.labels[self.filename][str(dictID)] = [newEntry]
            self.updateTree(keywords, 0)
        else:
            nextId = self.getNextAvailableId()
            self.labels[self.filename][str(dictID)].append({
                                'id': nextId, 'keywords': keywords,
                                'notes': notes, 'rect': self.recentRectangle})
            self.updateTree(keywords, nextId)

        print(self.labels)

    def getNextAvailableId(self):
    	""" Get the next available label ID"""
        dictID = (str(self.currAnts), self.pol)
        labels = self.labels[self.filename][str(dictID)]
        ids = [l['id'] for l in labels]
        diff = set(ids).difference(set(range(0, max(ids)+1)))
        if diff == set():
            diff = {max(ids) + 1}
        return min(diff)

    def updateLabel(self):
        pass

    def delLabel(self, filename, currAntsPol=None, idLabel=None):
    	""" Remove the label and its annotation. """
        keys = self.keys
        if idLabel is not None:
            for i in range(keys[filename][currAntsPol], 0, -1):
                if keys[filename][currAntsPol][i]['id'] == idLabel:
                    del self.keys[filename][currAntsPol][i]
        elif currAntsPol is not None:
            del self.keys[filename][currAntsPol]
        elif idLabel is None and currAntsPol is None:
            del self.keys[filenames]

    # if file has labels
    def getLabels(self, oldLabels=None):
    	""" Update the data object with existing labels in a file. """
        if oldLabels is None and self.keys == {}:
            self.keys = {'no group': []}
            self.addLabel.emit('no group', '', 0)
        else:
            keys = {}
            files = oldLabels[self.filename]
            for t in files:  # tuples
                for l in files[t]:  # label
                    for k in files[t][l]['keywords']:
                        tupleVal = str(files[t])
                        labelVal = str(files[t][l]['keywords']['id'])
                        if k not in keys:
                            keys[k] = [tupleVal + labelVal]
                        else:
                            keys[k].append([tupleVal + labelVal])
            self.keys = keys

    # adding new labels
    def updateTree(self, keys, newID):
    	""" Update the tree widget with new annotations. """
        dictID = (str(self.currAnts), self.pol)
        name = str(dictID) + str(newID)
        for k in keys:
            if k not in self.keys:
                self.keys[k] = [name]
                self.addLabel.emit(k, name, 0)
            else:
                self.keys[k].append(name)
                self.addLabel.emit(k, name, 1)

    @QtCore.pyqtSlot(list, str, int)
    def selectLabels(self, items, single, lType):
    	""" Filter labels based on selection. """
        print(items, single, lType)
        if lType == -1:
            pass
        elif lType == 0:
            pass
        elif lType == 1:
            pass
        elif lType == 2:
            pass
        else:
            print("Problem")

    def exportLabels(self, exportName):
    	""" Write the data object to a file. """
        # write dictionary to json for now
        # also no order bc dictionary, again, for now
        # also need to ensure it does full path
        with open(exportName, 'w') as fp:
            json.dumps(self.labels, fp, indent=4)
