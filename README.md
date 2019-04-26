# uvlabeller
An open source tool to interact with interferometric data.


# Dependencies
pyuvdata
numpy
pyqt 5.12+ 
python 3.6+


# Development

### UI
UI edits must be done through Qt Creator (open source, v5.12.x).
Open the \*.ui file being edited or create a new Qt Design Form (not class)
Regenerate the files via the following command
`pyuic5 -x editedFileNameHere.ui -o editedFileNameHere.py`
If you edited uvlabeller.py:
Edit uvlabeller by
Adding these imports
`from PyQt5.QtCore import QObject, pyqtSlot`
`import default_view as mainview`
Replace this line
`class Ui_MainWindow(object):` with this line `class Ui_MainWindow( QObject ):`

Following this line
`self.frame.setObjectName("frame")`
Add
```
self.curr_ui = mainview.Ui_Frame()
self.curr_ui.setupUi(self.frame)
```

UI functionality can be found in the controller classes. UI regeneration will wipe existing UI code.

### Data
This tool currently works with UVData and can label


## Future Work
Flagging
Opening other data types


# Bugs?
Submit an issue and give it the label "bug"

Please describe the actions done to reach the bug (ie click the "label" button) and what the bug does (ie program freezes, crashes, doesn't do action, etc)