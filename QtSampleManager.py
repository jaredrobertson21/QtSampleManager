import sys
import sqlite3
import database
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit, QListWidget,
                             QPushButton, QTextEdit, QWidget)

DATABASE_NAME = 'sample_database.db'

# GUI design and functionality for the "Add New Sample" dialog
class AddSampleDialog(QWidget):

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        # instantiate all GUI objects
        self.SAMPLE_NAME = QLineEdit()
        self.CHEMICAL_NAME = QLineEdit()
        self.SAMPLE_NOTES = QTextEdit()
        self.LABEL_SAMPLE_NAME = QLabel('Sample Name')
        self.LABEL_CHEMICAL_NAME = QLabel('Chemical Name')
        self.LABEL_SAMPLE_NOTES = QLabel('Sample Notes')
        self.OK_BUTTON = QPushButton('Ok')
        self.CANCEL_BUTTON = QPushButton('Cancel')

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.LABEL_SAMPLE_NAME, 1, 1)
        grid.addWidget(self.SAMPLE_NAME, 1, 2, 1, 2)
        grid.addWidget(self.LABEL_CHEMICAL_NAME, 2, 1)
        grid.addWidget(self.CHEMICAL_NAME, 2, 2, 1, 2)
        grid.addWidget(self.LABEL_SAMPLE_NOTES, 3, 1)
        grid.addWidget(self.SAMPLE_NOTES, 3, 2, 2, 2)
        grid.addWidget(self.OK_BUTTON, 5, 2)
        grid.addWidget(self.CANCEL_BUTTON, 5, 3)

        self.setLayout(grid)

        self.OK_BUTTON.clicked.connect(self.createSample)
        self.CANCEL_BUTTON.clicked.connect(self.close)

        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Add New Sample')
        self.show()

    # appends the new sample information to the sample library and database
    # TODO: don't allow multiple samples with the same name to be added
    def createSample(self):
        if self.SAMPLE_NAME.text():
            SAMPLES.addSample(self.SAMPLE_NAME.text(), self.CHEMICAL_NAME.text(), self.SAMPLE_NOTES.toPlainText())
            database.addSampleToDatabase(sample_db, cursor, self.SAMPLE_NAME.text(), self.CHEMICAL_NAME.text(),
                                         self.SAMPLE_NOTES.toPlainText())
            self.sendSampleToMainWindow(self.SAMPLE_NAME.text())
            self.close()

    # sends the new sample to be added to the main window list widget
    def sendSampleToMainWindow(self, sample):
        main_window.addSample(sample)


# defines the object that contains all sample information
class SampleLibrary(dict):

    def __init__(self):
        super().__init__()
        self.sample_library = {}

    # adds a sample and its properties to a JSON-style object
    def addSample(self, name, chemical, notes):
        self.sample_library[name] = {
            'chemical': chemical,
            'notes': notes
        }

        return self.sample_library

    def deleteSample(self, name):
        self.sample_library.pop(name)


# GUI design and functionality for the main window
class MainWindow(QWidget):

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        # instantiate all GUI objects
        self.NEW_SAMPLE_BUTTON = QPushButton('New Sample')
        self.DELETE_SAMPLE_BUTTON = QPushButton('Delete Sample')
        self.SAMPLES_LIST = QListWidget()
        self.SAMPLE_NAME = QLineEdit()
        self.CHEMICAL_NAME = QLineEdit()
        self.SAMPLE_NOTES = QTextEdit()
        self.LABEL_SAMPLE_NAME = QLabel('Sample Name')
        self.LABEL_CHEMICAL_NAME = QLabel('Chemical Name')
        self.LABEL_SAMPLE_NOTES = QLabel('Sample Notes')
        grid = QGridLayout()

        grid.setSpacing(10)
        grid.addWidget(self.SAMPLES_LIST, 1, 1, 3, 1)
        grid.addWidget(self.LABEL_SAMPLE_NAME, 1, 2)
        grid.addWidget(self.SAMPLE_NAME, 1, 3)
        grid.addWidget(self.NEW_SAMPLE_BUTTON, 4, 1)
        grid.addWidget(self.DELETE_SAMPLE_BUTTON, 5, 1)
        grid.addWidget(self.LABEL_CHEMICAL_NAME, 2, 2)
        grid.addWidget(self.CHEMICAL_NAME, 2, 3)
        grid.addWidget(self.LABEL_SAMPLE_NOTES, 3, 2)
        grid.addWidget(self.SAMPLE_NOTES, 3, 3, 3, 1)

        self.setLayout(grid)

        self.NEW_SAMPLE_BUTTON.clicked.connect(self.showAddSampleDialog)
        self.DELETE_SAMPLE_BUTTON.clicked.connect(self.deleteSample)
        self.SAMPLES_LIST.itemClicked.connect(self.getSampleProperties)
        self.SAMPLE_NAME.textEdited.connect(self.editProperty)
        self.CHEMICAL_NAME.textEdited.connect(self.editProperty)
        self.SAMPLE_NOTES.textChanged.connect(self.editProperty)

        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle('Sample Manager')
        self.show()

    # adds the sample name to the main window list widget
    def addSample(self, sample):
        self.SAMPLES_LIST.addItem(sample)


    def deleteSample(self):
        selected_sample = self.SAMPLES_LIST.selectedItems()
        if len(selected_sample) == 1:
            # if a sample is highlighted, delete from the database and sample list
            SAMPLES.deleteSample(selected_sample[0].text())
            self.SAMPLES_LIST.takeItem(self.SAMPLES_LIST.currentRow())


    # TODO: update method to handle changes to the notes without having notes update
    # TODO: each time a new sample is clicked
    def editProperty(self):
        current_sample = self.SAMPLES_LIST.currentItem().text()

        # update the edited fields in the sample library
        if self.sender() == self.SAMPLE_NAME:
            # update the edited sample name in the sample library
            SAMPLES.sample_library[self.SAMPLE_NAME.text()] = SAMPLES.sample_library.pop(current_sample)
            self.SAMPLES_LIST.currentItem().setText(self.SAMPLE_NAME.text())

        elif self.sender() == self.CHEMICAL_NAME:
            SAMPLES.sample_library[current_sample]['chemical'] = self.CHEMICAL_NAME.text()

        else:
            SAMPLES.sample_library[current_sample]['notes'] = self.SAMPLE_NOTES.toPlainText()

    # populate the properties of the sample in the widgets when the sample name is clicked
    def getSampleProperties(self):
        if self.sender() == self.SAMPLES_LIST:
            sample_properties = SAMPLES.sample_library[self.SAMPLES_LIST.currentItem().text()]
            self.SAMPLE_NAME.setText(self.SAMPLES_LIST.currentItem().text())
            self.CHEMICAL_NAME.setText(sample_properties['chemical'])
            self.SAMPLE_NOTES.setText(sample_properties['notes'])

    # Create the 'Add sample' dialog - the window where samples can be added
    def showAddSampleDialog(self):
        self.AddSampleDialog = AddSampleDialog()

    # closes the 'Add sample' dialog when the main window is closed
    def closeEvent(self, QCloseEvent):
        if hasattr(self, 'AddSampleDialog'):
            self.AddSampleDialog.close()


if __name__ == '__main__':

    sample_db = sqlite3.connect(DATABASE_NAME)
    cursor = sample_db.cursor()
    database.createTable(cursor)
    data = database.getAllData(cursor)

    # instantiate all major objects; SAMPLES contains all stored samples
    SAMPLES = SampleLibrary()
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # load samples from database into SAMPLES object and main window
    for sample in data:
        SAMPLES.addSample(sample[0], sample[1], sample[2])
        main_window.addSample(sample[0])

    # TODO: figure out how to simultaneously close db connection
    sys.exit(app.exec_())


