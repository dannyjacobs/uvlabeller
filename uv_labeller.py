# Cecilia La Place
# Thesis Project

# PyQt5 Imports
import sys
from PyQt5 import QtCore, QtWidgets
#from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QWidget, QMessageBox, QAction, qApp, QGridLayout, QTextEdit, QLineEdit, QLabel, QComboBox, QSizePolicy
#from PyQt5.QtGui import QIcon

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
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
		print(self.pairs)
		self.ants = self.UV.get_ants()
		self.currAnts = list(self.pairs[0])

	def setFiles(self,filenames):
		self.files = filenames

	def setAnts(self,a=None,b=None):
		if a != self.currAnts[0] and a is not None:
			if (a, self.currAnts[1]) in self.pairs:
				self.currAnts = [a, self.currAnts[1]]
		if b != self.currAnts[1] and b is not None:
			if (self.currAnts[0], b) in self.pairs:
				self.currAnts = [self.currAnts[0], b]
		# else tooltip error

		print('ants', self.currAnts)

	def flagger():
		pass

# Matplotlib management
class WidgetPlot(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		QtWidgets.QWidget.__init__(self, *args, **kwargs)
		self.setLayout(QtWidgets.QVBoxLayout())
		self.canvas = PlotCanvas(self, width=10, height=10)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.layout().addWidget(self.toolbar)
		self.layout().addWidget(self.canvas)

	def update(self, data):
		self.canvas.update_figure(data)

class GraphWindow(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		self.cbar = self.fig.add_axes([0.925, 0.1, 0.035, 0.8])
		self.compute_initial_figure()
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def compute_initial_figure(self):
		pass

class PlotCanvas(GraphWindow):
	"""A canvas that updates itself every second with a new plot."""

	def __init__(self, *args, **kwargs):
		GraphWindow.__init__(self, *args, **kwargs)
		#Adjust to a change in drop down menus
		#timer = QtCore.QTimer(self)
		#timer.timeout.connect(self.update_figure)
		#timer.start(1000)

	#def compute_initial_figure(self):
		#self.count = 0
		#im = self.axes.imshow(np.abs(UV.get_data((1,2,'xx'))), aspect='auto', extent=[0,1000,60,0], vmin=0, vmax=2.0*np.median(np.abs(UV.get_data((1,2,'xx')))))
		#cbar = self.fig.add_axes([0.925, 0.1, 0.035, 0.8])
		#self.fig.colorbar(im, cax=cbar)
	#	pass
	  

	def update_figure(self, data):
		#self.count += 1
		#self.count %= len(pairs)
		#curr = pairs[self.count]
		calc = data.UV.get_data((data.currAnts[0],data.currAnts[1],'xx'))
		im = self.axes.imshow(np.abs(calc), aspect='auto', extent=[0,1000,60,0], vmin=0, vmax=2.0*np.median(np.abs(calc)))
		self.fig.colorbar(im, cax=self.cbar)
		self.draw()

# GUI management
class Main(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.resize(800,500)
		self.center()
		self.statusBar()

		# Main Window 
		mainMenu = self.initMenuBar()
		self.activeWindow = QtWidgets.QWidget()
		self.setCentralWidget(self.activeWindow)
		self.data = Data()

		self.initGraphWin()
		self.show()
		
	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	
	def openFiles(self):
		options = QtWidgets.QFileDialog.Options()
		#options |= QtWidgets.QFileDialog.DontUseNativeDialog
		options =  QtWidgets.QFileDialog.ShowDirsOnly
		files = QtWidgets.QFileDialog.getExistingDirectory(self,"Select UV file", "", options=options)
		self.data.setFile(files)
		self.aData = [str(x) for x in self.data.ants]
		self.bData = [str(x) for x in self.data.ants]
		self.aCBox.clear()       # delete all items from comboBox
		self.bCBox.clear()
		self.aCBox.addItems(self.aData) # add the actual content of self.comboData
		self.bCBox.addItems(self.bData)
		self.plot.update(self.data)
	def saveFile(self):
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save UV file","","All Files (*);;UV Files (*.uv)", options=options)
		if fileName:
			print(fileName)

	def exportFile(self):
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Export UV file","","All Files (*);;UV Files (*.uv)", options=options)
		if fileName:
			print(fileName)

	def initMenuBar(self):
		''' COME BACK TO LATER
		self.file_menu = QtWidgets.QMenu('&File', self)
		self.file_menu.addAction('&Quit', self.fileQuit,
								 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
		self.menuBar().addMenu(self.file_menu)

		self.help_menu = QtWidgets.QMenu('&Help', self)
		self.menuBar().addSeparator()
		self.menuBar().addMenu(self.help_menu)

		self.help_menu.addAction('&About', self.about)

		self.openFileNamesDialog()
		self.saveFileDialog()
		 
		self.show()

		'''

		# File
		openAct = QtWidgets.QAction('&Open', self)
		openAct.setShortcut('Ctrl+O')
		openAct.setStatusTip('Open file')
		openAct.triggered.connect(self.openFiles)

		saveAct = QtWidgets.QAction('&Save', self)
		saveAct.setShortcut('Ctrl+S')
		saveAct.setStatusTip('Save flagging')
		saveAct.triggered.connect(self.saveFile)

		exportAct = QtWidgets.QAction('&Export', self)
		exportAct.setShortcut('Ctrl+E')
		exportAct.setStatusTip('Export')
		exportAct.triggered.connect(self.exportFile)

		prefAct = QtWidgets.QAction('&Preferences', self)
		prefAct.setStatusTip('Preferences')
		#prefAct.triggered.connect()

		exitAct = QtWidgets.QAction('&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(QtWidgets.qApp.quit)

		# Edit
		undoAct = QtWidgets.QAction('&Undo', self)
		undoAct.setShortcut('Ctrl+Z')
		undoAct.setStatusTip('Undo most recent action')
		#undoAct.triggered.connect()

		redoAct = QtWidgets.QAction('&Redo', self)
		redoAct.setShortcut('Ctrl+Shift+Z')
		redoAct.setStatusTip('Repeat previous action or recently undone action')
		#redoAct.triggered.connect()

		dupAct = QtWidgets.QAction('&Duplicate', self)
		dupAct.setShortcut('Ctrl+D')
		dupAct.setStatusTip('Duplicate')
		#dupAct.triggered.connect()

		# View


		# Help
		helpAct = QtWidgets.QAction('&Tutorial', self)
		#helpAct.triggered.connect()
		aboutAct = QtWidgets.QAction('&About', self)
		#aboutAct.triggered.connect()

		# Menubar Management
		menubar = self.menuBar()

		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(openAct)
		fileMenu.addAction(saveAct)
		fileMenu.addAction(exportAct)
		fileMenu.addAction(prefAct)
		fileMenu.addAction(exitAct)

		editMenu = menubar.addMenu('&Edit')
		editMenu.addAction(undoAct)
		editMenu.addAction(redoAct)
		editMenu.addAction(dupAct)

		viewMenu = menubar.addMenu('&View')

		helpMenu = menubar.addMenu('&Help')
		helpMenu.addAction(helpAct)

		menubar.setNativeMenuBar(False) # for macs only?
		return menubar

	def initGraphWin(self):
		# Graph
		self.plot = WidgetPlot(self)

		#Info window
		ant1 = QtWidgets.QLabel('Antenna')
		ant2 = QtWidgets.QLabel('Antenna')
		notes = QtWidgets.QLabel('Notes')

		self.aCBox = QtWidgets.QComboBox()
		self.aCBox.currentIndexChanged.connect(self.selection)
		self.bCBox = QtWidgets.QComboBox()
		self.bCBox.currentIndexChanged.connect(self.selection2)

		notesEdit = QtWidgets.QTextEdit()
		vlay = QtWidgets.QVBoxLayout()
		vlay.addWidget(self.plot)
		hlay = QtWidgets.QHBoxLayout()
		vlay.addLayout(hlay)
		hlay.addWidget(ant1)
		hlay.addWidget(self.aCBox)
		hlay.addWidget(ant2)
		hlay.addWidget(self.bCBox)
		vlay.addWidget(notes)
		vlay.addWidget(notesEdit)
		self.activeWindow.setLayout(vlay)

	def selection(self, idx):
		self.data.setAnts(int(self.aData[idx]))
		self.plot.update(self.data)

	def selection2(self, idx):
		self.data.setAnts(None, int(self.bData[idx]))
		self.plot.update(self.data)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	ex = Main()
	ex.setWindowTitle("UV Labeler")
	ex.show()
	sys.exit(app.exec_())