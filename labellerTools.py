# UV Labeller Toolbar

import matplotlib.pyplot as plt
import matplotlib
plt.rcParams['toolbar'] = 'toolmanager'
from matplotlib.backend_tools import ToolBase, ToolToggleBase

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class Annotate(object):
	def __init__(self, axes, data):
		self.labeling = False
		self.data = data
		self.axes = axes
		self.rect = matplotlib.patches.Rectangle((0,0), 1, 1, color='white', alpha=0.5)
		self.x0 = None
		self.y0 = None
		self.x1 = None
		self.y1 = None
		self.pressed = False
		self.axes.add_patch(self.rect)
		self.axes.figure.canvas.mpl_connect('button_press_event', self.on_press)
		self.axes.figure.canvas.mpl_connect('button_release_event', self.on_release)
		self.axes.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

	def toggle(self):
		self.labeling = not self.labeling
		if not self.labeling:
			print('toolbar')
			self.data.saveRect()

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
			# get rectangle attributes vertices, coordinates
			self.data.saveRect(self.rect.get_xy(), self.rect.get_width(), self.rect.get_height())
			self.axes.figure.canvas.draw()

	def on_motion(self, event):
		if self.pressed and self.labeling:
			self.x1 = event.xdata
			self.y1 = event.ydata
			self.rect.set_width(self.x1 - self.x0)
			self.rect.set_height(self.y1 - self.y0)
			self.rect.set_xy((self.x0, self.y0))
			self.rect.set_linestyle('dashed')
			self.axes.figure.canvas.draw()


class MyToolbar(NavigationToolbar):
	def __init__(self, data, canvas, parent=None):
		NavigationToolbar.__init__(self, canvas, parent)
		self.data = data
		self.canvas = canvas
		self.ann = Annotate(canvas.axes, data)
		#self.iconDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
		#	"..", "images", "icons", "")

		#self.a = self.addAction(QIcon(iconDir + "BYE2.ico"),
		self.addSeparator()
		a = self.addAction("Annotate", self.ann.toggle)
