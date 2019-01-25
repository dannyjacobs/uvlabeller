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
import matplotlib

plt.rcParams['toolbar'] = 'toolmanager'
from matplotlib.backend_tools import ToolBase, ToolToggleBase

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
		self.UV.read(self.filename) 	# Functional. But testing means I want faster load times
		#self.UV.read(self.filename, read_data=False, read_metadata=True)
		self.pairs = self.UV.get_antpairs()
		print(self.pairs)
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

		print('ants', self.currAnts)

	def setPol(self, pol):
		self.pol = pol
	def flagger():
		pass

# Matplotlib management
class WidgetPlot(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		QtWidgets.QWidget.__init__(self, *args, **kwargs)
		self.setLayout(QtWidgets.QVBoxLayout())
		self.canvas = PlotCanvas(self, width=10, height=10)
		self.toolbar = MyToolbar(self.canvas, self)
		#self.toolbar.toolmanager.add_tool('Labelling', LabelTool, Annotate)

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
		self.annotate = Annotate(self.axes)
		
	def compute_initial_figure(self):
		pass

class PlotCanvas(GraphWindow):
	"""A canvas that updates itself every second with a new plot."""

	def __init__(self, *args, **kwargs):
		GraphWindow.__init__(self, *args, **kwargs)

	def update_figure(self, data):
		#data.UV.read(data.filename, bls=[(data.currAnts[0],data.currAnts[1])])
		calc = data.UV.get_data((data.currAnts[0],data.currAnts[1],data.pol))
		im = self.axes.imshow(np.abs(calc), aspect='auto', extent=[0,1000,60,0], vmin=0, vmax=2.0*np.median(np.abs(calc)))
		self.fig.colorbar(im, cax=self.cbar)
		self.draw()

class MyToolbar(NavigationToolbar):
  def __init__(self, canvas, parent=None):
    NavigationToolbar.__init__(self, canvas, parent)
    self.canvas = canvas
    #self.annotate = annotate
    #self.iconDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #    "..", "images", "icons", "")

    #self.a = self.addAction(QIcon(iconDir + "BYE2.ico"),
    self.a = self.addAction("Annotate", self.canvas.annotate.toggle)

class Annotate(object):
	def __init__(self, canvas):
		self.labeling = True
		self.ax = canvas
		self.rect = matplotlib.patches.Rectangle((0,0), 1, 1, color='white')
		self.x0 = None
		self.y0 = None
		self.x1 = None
		self.y1 = None
		self.pressed = False
		self.ax.add_patch(self.rect)
		self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
		self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
		self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

	def toggle(self):
		self.labeling = not self.labeling
		print(self.labeling, 'hello')

	def on_press(self, event):
		if self.labeling:
			self.pressed = True
			self.x0 = event.xdata
			self.y0 = event.ydata

	def on_release(self, event):
		if self.labeling:
			self.pressed = False
			self.x1 = event.xdata
			self.y1 = event.ydata
			self.rect.set_width(self.x1 - self.x0)
			self.rect.set_height(self.y1 - self.y0)
			self.rect.set_xy((self.x0, self.y0))
			self.ax.figure.canvas.draw()

	def on_motion(self, event):
		if self.pressed and self.labeling:
			self.x1 = event.xdata
			self.y1 = event.ydata
			self.rect.set_width(self.x1 - self.x0)
			self.rect.set_height(self.y1 - self.y0)
			self.rect.set_xy((self.x0, self.y0))
			self.rect.set_linestyle('dashed')
			self.ax.figure.canvas.draw()

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
		self.pData = self.data.pols
		self.aCBox.clear()	   # delete all items from comboBox
		self.bCBox.clear()
		self.pCBox.clear()
		self.aCBox.addItems(self.aData) # add the actual content of self.comboData
		self.bCBox.addItems(self.bData)
		self.pCBox.addItems(self.pData)
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
		pol = QtWidgets.QLabel('Polarization')
		notes = QtWidgets.QLabel('Notes')

		self.aCBox = QtWidgets.QComboBox()
		self.aCBox.currentIndexChanged.connect(self.selection)
		self.bCBox = QtWidgets.QComboBox()
		self.bCBox.currentIndexChanged.connect(self.selection2)
		self.pCBox = QtWidgets.QComboBox()
		self.pCBox.currentIndexChanged.connect(self.selection3)

		notesEdit = QtWidgets.QTextEdit()
		vlay = QtWidgets.QVBoxLayout()
		vlay.addWidget(self.plot)
		hlay = QtWidgets.QHBoxLayout()
		vlay.addLayout(hlay)
		hlay.addWidget(ant1)
		hlay.addWidget(self.aCBox)
		hlay.addWidget(ant2)
		hlay.addWidget(self.bCBox)
		hlay.addWidget(pol)
		hlay.addWidget(self.pCBox)
		vlay.addWidget(notes)
		vlay.addWidget(notesEdit)
		self.activeWindow.setLayout(vlay)

	def selection(self, idx):
		self.data.setAnts(int(self.aData[idx]))
		self.plot.update(self.data)

	def selection2(self, idx):
		self.data.setAnts(None, int(self.bData[idx]))
		self.plot.update(self.data)
	def selection3(self, idx):
		self.data.setPol(self.pData[idx])
		self.plot.update(self.data)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	ex = Main()
	ex.setWindowTitle("UV Labeler")
	ex.show()
	sys.exit(app.exec_())