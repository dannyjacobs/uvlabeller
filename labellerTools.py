# UV Labeller Toolbar

import matplotlib.pyplot as plt
import matplotlib
plt.rcParams['toolbar'] = 'toolmanager'
from matplotlib.backend_tools import ToolBase, ToolToggleBase

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class Annotate(object):
	def __init__(self, canvas, data):
		self.labeling = False
		self.data = data
		self.canvas = canvas
		self.axes = self.canvas.axes
		#self.rects = [] # to be used with ids for selection later
		self.rect = matplotlib.patches.Rectangle((0,0), 1, 1, color='white', alpha=0.5)
		self.x0 = None
		self.y0 = None
		self.x1 = None
		self.y1 = None
		self.pressed = False
		self.shift = False
		self.axes.add_patch(self.rect) # needed to see rectangle drawn on screen
		self.axes.figure.canvas.mpl_connect('button_press_event', self.on_press)
		self.axes.figure.canvas.mpl_connect('button_release_event', self.on_release)
		self.axes.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
		self.axes.figure.canvas.mpl_connect('key_press_event', self.on_key_press)
		self.axes.figure.canvas.mpl_connect('key_release_event', self.on_key_release)
		self.background = self.canvas.copy_from_bbox(self.axes.bbox)

	def toggle(self):
		#self.axes.figure.canvas.draw()
		self.labeling = not self.labeling
		if not self.labeling:
			print('toolbar')
			self.data.saveRect()

	def on_press(self, event):
		#self.background = self.canvas.copy_from_bbox(self.axes.bbox)
		if self.labeling and not self.shift:
			self.pressed = True
			self.x0 = event.xdata
			self.y0 = event.ydata
		elif self.pressed and self.labeling and self.shift:
			# select rect under mouse
			# move label
			pass

	def on_release(self, event):
		if self.labeling and not self.shift:
			self.pressed = False
			self.x1 = event.xdata
			self.y1 = event.ydata
			self.rect.set_width(self.x1 - self.x0)
			self.rect.set_height(self.y1 - self.y0)
			# get rectangle attributes vertices, coordinates
			self.data.saveRect(self.rect.get_xy(), self.rect.get_width(), self.rect.get_height())
			#self.axes.figure.canvas.draw()
			self.axes.draw_artist(self.rect)
			self.canvas.blit(self.axes.bbox)
		if self.labeling and self.shift:
			# save selected rect and update pos. 
			# find and update rect in data
			pass

	def on_motion(self, event):
		#self.rect.remove()
		self.canvas.restore_region(self.background)
		self.canvas.blit(self.axes.bbox)
		if self.pressed and self.labeling and not self.shift:
			self.x1 = event.xdata
			self.y1 = event.ydata
			self.rect.set_width(self.x1 - self.x0)
			self.rect.set_height(self.y1 - self.y0)
			self.rect.set_xy((self.x0, self.y0))
			self.rect.set_linestyle('dashed')
			#self.axes.figure.canvas.draw()
			self.axes.draw_artist(self.rect)
			self.canvas.blit(self.axes.bbox)
		elif self.pressed and self.labeling and self.shift:
			# move selected rect
			pass

	def on_key_press(self, event):
		if event.key == 'shift':
			self.shift = True

	def on_key_release(self, event):
		if event.key == 'shift':
			self.shift = False

	def addRect(self):
		rect = matplotlib.patches.Rectangle(self.rect.get_xy(), self.rect.get_width(), self.rect.get_height(), color='white', alpha=0.3)
		self.axes.add_patch(rect) # can I just patch self.rect?

	#how det. visibility through tree?
	def showRects(self, labels):
		pass

class MyToolbar(NavigationToolbar):
	def __init__(self, data, canvas, parent=None):
		NavigationToolbar.__init__(self, canvas, parent)
		self.data = data
		self.canvas = canvas
		self.ann = Annotate(canvas, data)
		#self.iconDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
		#	"..", "images", "icons", "")

		#self.a = self.addAction(QIcon(iconDir + "BYE2.ico"),
		self.addSeparator()
		a = self.addAction("Annotate", self.ann.toggle)
	def addRect(self):
		self.ann.addRect()