# UV Labeller UI

# PyQt5 Imports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# Matplotlib Imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib

# Custom Library Imports
import labellerData as dataLib
import labellerTools as toolsLib

# Other Libraries
import numpy as np


# Matplotlib management
# Widget calls PlotCanvas which is a child of GraphWindow
class WidgetPlot(QtWidgets.QWidget):
	def __init__(self, data, *args, **kwargs):
		QtWidgets.QWidget.__init__(self, *args, **kwargs)
		self.setLayout(QtWidgets.QVBoxLayout())
		self.canvas = PlotCanvas(self, width=10, height=10)
		self.toolbar = toolsLib.MyToolbar(data, self.canvas, self)
		self.layout().addWidget(self.toolbar)
		self.layout().addWidget(self.canvas)

	def update(self, data):
		self.canvas.update_figure(data)

	def setTitle(self, filename):
		self.canvas.updateTitle(filename)

	def addRect(self):
		self.toolbar.addRect()

class GraphWindow(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		self.axes.set_title(' ')
		self.axes.set_xlabel(' ')
		self.axes.set_ylabel(' ')
		self.cbar = self.fig.add_axes([0.925, 0.1, 0.035, 0.8])
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

class PlotCanvas(GraphWindow):
	def __init__(self, *args, **kwargs):
		GraphWindow.__init__(self, *args, **kwargs)

	def update_figure(self, data):
		# Introduces slowness, bug?
		#[p.remove() for p in reversed(self.axes.patches)]
		#print('patches', self.axes.patches)
		calc = data.UV.get_data((data.currAnts[0],data.currAnts[1],data.pol))
		tmax = (data.UV.time_array.max() - data.UV.time_array.min()) * 24. * 60 * 60
		extent = [data.UV.freq_array.min() * 1e-6, data.UV.freq_array.max() * 1e-6, tmax, 0]
		im = self.axes.imshow(np.abs(calc), aspect='auto', extent=extent, vmin=0, vmax=2.0*np.median(np.abs(calc)))
		self.fig.colorbar(im, cax=self.cbar)
		self.draw()

	def updateTitle(self, filename):
		name = filename.split('/')[-1] if '/' in filename else filename.split('\\')[-1]
		self.axes.set_title(name)
		self.axes.set_xlabel('Freq (MHz)')
		self.axes.set_ylabel('Time (s)')


# Label Management
class TreeWidget(QtWidgets.QWidget):
	show = QtCore.pyqtSignal(list, str, int)
	def __init__(self, data, *args, **kwargs):
		QtWidgets.QWidget.__init__(self, *args, **kwargs)
		self.data = data
		self.setLayout(QtWidgets.QVBoxLayout())
		self.tw = QtWidgets.QTreeWidget(self)
		self.tw.resize(200, 500)
		self.tw.updateGeometry()
		self.tw.setColumnCount(1)
		self.tw.setColumnWidth(1, 80)
		self.tw.setHeaderLabels(["Keywords"])
		self.tw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.tw.itemSelectionChanged.connect(self.selection)
		self.data.addLabel.connect(self.updateTree)
		self.show.connect(self.data.selectLabels)
		for l in self.data.keys:
			group = QtWidgets.QTreeWidgetItem([l])
			for labelID in self.data[l]:
				item = QtWidgets.QTreeWidgetItem([labelID])
				group.addChild(item)
			self.tw.addTopLevelItem(group)
		self.layout().addWidget(self.tw)
		self.resize(self.sizeHint().width(), self.minimumHeight())

	@QtCore.pyqtSlot(str, str, int)
	def updateTree(self, label, item, insertType):
		if insertType == 0:
			newLabel = QtWidgets.QTreeWidgetItem([label])
			if item != '':
				treeItem = QtWidgets.QTreeWidgetItem([item])
				newLabel.addChild(treeItem)
			self.tw.addTopLevelItem(newLabel)
		elif insertType == 1:
			root = self.tw.invisibleRootItem()
			child_count = root.childCount()
			for i in range(child_count):
				if root.child(i).text(0) == label:
					treeItem = QtWidgets.QTreeWidgetItem([item])
					root.child(i).addChild(treeItem)
					break
		else:
			print("Problem")

	def selection(self):
		selected = self.tw.selectedItems()
		root = self.tw.invisibleRootItem()
		top = []
		children = []
		for i in range(root.childCount()):
			top.append(root.child(i))
			for j in range(root.child(i).childCount()):
				children.append(root.child(i).child(j))
		viewT = []
		viewC = []
		if selected:
			for i in selected:
				if i in top:
					viewT.append(i)
				elif i in children:
					viewC.append(i)
				else:
					print("Problem")
			if len(viewT) > 0 and len(viewC) > 0:
				out = []
				for v in viewT:
					out.append(v.text(0))
				self.show.emit(out, viewC[0].text(0), 0)
			elif len(viewT) > 0 and len(viewC) == 0:
				out = []
				for v in viewT:
					out.append(v.text(0))
				self.show.emit(out, '', 1)
			else:
				out = []
				for v in viewC:
					out.append(v.text(0))
				self.show.emit(out, '', 2)
		else:
			self.show.emit([],'', -1)

# GUI management
# This handles the entire window
class Main(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.resize(1000,600)
		self.center()
		self.statusBar()

		# Main Window 
		mainMenu = self.initMenuBar()
		self.activeWindow = QtWidgets.QWidget()
		self.setCentralWidget(self.activeWindow)
		# Init data class
		self.data = dataLib.Data()
		# Plot
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
		file = QtWidgets.QFileDialog.getExistingDirectory(self,"Select UV file", "", options=options)
		self.data.setFile(file)
		self.aData = [str(x) for x in self.data.ants]
		self.pData = self.data.pols
		self.aCBox.clear()	   # delete all items from comboBox
		self.bCBox.clear()
		self.pCBox.clear()
		self.aCBox.addItems(self.aData) # add the actual content of self.comboData
		self.bCBox.addItems(self.aData)
		self.pCBox.addItems(self.pData)
		self.plot.update(self.data)
		self.plot.setTitle(file)

	def saveFile(self):
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save UV file","","All Files (*);;UV Files (*.uv)", options=options)
		if fileName:
			print(fileName)

	def exportFile(self):
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Export Labels","","All Files (*);;JSON Files (*.json)", options=options)
		if fileName:
			#handler for nonjson
			self.data.exportLabels(fileName)

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
		exportAct.setStatusTip('Export Labels')
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

		menubar.setNativeMenuBar(True) # debatable
		return menubar

	def initGraphWin(self):
		# Graph
		self.plot = WidgetPlot(self.data, self)
		self.tree = TreeWidget(self.data, self)

		#Info window
		ant1 = QtWidgets.QLabel('Antenna')
		ant2 = QtWidgets.QLabel('Antenna')
		pol = QtWidgets.QLabel('Polarization')
		keywords = QtWidgets.QLabel('Keywords (comma separated)')
		notes = QtWidgets.QLabel('Notes')
		self.aCBox = QtWidgets.QComboBox()
		self.aCBox.currentIndexChanged.connect(lambda idx: self.selectCombo(idx, 0))
		self.bCBox = QtWidgets.QComboBox()
		self.bCBox.currentIndexChanged.connect(lambda idx: self.selectCombo(idx, 1))
		self.pCBox = QtWidgets.QComboBox()
		self.pCBox.currentIndexChanged.connect(lambda idx: self.selectCombo(idx, 2))

		self.keysEdit = QtWidgets.QLineEdit()
		self.notesEdit = QtWidgets.QTextEdit()

		self.saveBtn = QtWidgets.QPushButton("Save label")
		self.saveBtn.setEnabled(True) # connect to labelling to be disabled otherwise
		self.saveBtn.clicked.connect(self.saveLabel)

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
		hlay2 = QtWidgets.QHBoxLayout() # space between this and keysEdit odd
		hlay2.addWidget(keywords)
		hlay2.addWidget(self.saveBtn)
		vlay.addLayout(hlay2)
		vlay.addWidget(self.keysEdit)
		vlay.addWidget(notes)
		vlay.addWidget(self.notesEdit)

		hlayMain = QtWidgets.QHBoxLayout()
		hlayMain.addLayout(vlay)
		hlayMain.addWidget(self.tree)
		self.activeWindow.setLayout(hlayMain)

	def selectCombo(self, idx, cBoxType):
		if cBoxType == 0:
			self.data.setAnts(int(self.aData[idx]))
		elif cBoxType == 1:
			self.data.setAnts(None, int(self.aData[idx]))
		elif cBoxType == 2:
			self.data.setPol(self.pData[idx])
		else: 
			print('Problem') #error handle later
		self.plot.update(self.data)

	def saveLabel(self):
		self.data.saveLabel(self.keysEdit.text(), self.notesEdit.toPlainText())
		self.plot.addRect()
		self.keysEdit.clear()
		self.notesEdit.clear()

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	ex = Main()
	ex.setWindowTitle("UV Labeller")
	ex.show()
	sys.exit(app.exec_())