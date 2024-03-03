from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction,QIcon
import os


#styleSheetColor index
#https://www.w3.org/TR/SVG11/types.html#ColorKeywords



"""
Whenever we import a file, a temp file appears so we can change the file without saving
"""


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        #this array will contain all of our current spreadsheet
        self.temp_array = []
        self.file_name = ""

        self.app = app
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Excel Clone")
        self.setStyleSheet("""
            background-color: #1E1E1E;
            color: #FFFFFF;
        """)


        #######  TOP TAB BAR ########
        menu_bar = self.menuBar()

        #file 
        file_menu = menu_bar.addMenu("File")
        save_action = file_menu.addAction("Save")
        import_action = file_menu.addAction("Import")
        saveas_action = file_menu.addAction("Save as")

        save_action.triggered.connect(lambda: self.save(self.file_name))
        import_action.triggered.connect(self.importCSV)
        saveas_action.triggered.connect(self.saveAs)


        #edit
        edit_menu = menu_bar.addMenu("Edit")
        copy_action = edit_menu.addAction("copy")
        paste_action = edit_menu.addAction("paste")

        #insert
        insert_menu = menu_bar.addMenu("Insert")
        image_action = insert_menu.addAction("image..")

        #find
        find_menu = menu_bar.addMenu("Find")
        findInstance_action = find_menu.addAction("find instances")
        #####################################


        ######## SPREAD SHEET ##########
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(50) # Set the number of rows
        self.table_widget.setColumnCount(35) # Set the number of columns

        #style shee for spreadSheet
        self.table_widget.setStyleSheet("""/* Scrollbar Styling */
        QScrollBar:vertical {
            border: 2px solid grey;
            background: #141414;
            width: 15px;
            margin: 22px 0 22px 0;
        }
        QScrollBar::handle:vertical {
            background: white;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical {
            border: 2px solid grey;
            background: #141414;
            height: 20px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            border: 2px solid grey;
            background: #141414;
            height: 20px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QScrollBar:horizontal {
            border: 2px solid grey;
            background: #141414;
            height: 15px;
            margin: 0px 20px 0 20px;
        }
        QScrollBar::handle:horizontal {
            background: white;
            min-width: 20px;
        }
        QScrollBar::add-line:horizontal {
            border: 2px solid grey;
            background: #141414;
            width: 20px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:horizontal {
            border: 2px solid grey;
            background: #141414;
            width: 20px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
        
        QTableWidget::item {
            padding: 5px; /* Padding around cell content */
        }

        """)

        #Populate the QTableWidget with empty data
        for row in range(50):
            for col in range(35):
                self.table_widget.setItem(row, col, QTableWidgetItem(""))

        #Checking if an entry has been changed
        self.table_widget.itemChanged.connect(self.handleItemChanged)

        #Wrap the QTableWidget in a QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.table_widget)
        self.scroll_area.setWidgetResizable(True)

        #Checking if we need to add more table values
        self.scroll_area.widget().verticalScrollBar().sliderMoved.connect(self.scrollPositionChangedVertical)
        self.scroll_area.widget().horizontalScrollBar().sliderMoved.connect(self.scrollPositionChangedHorizontal)
        self.row_limit = (self.table_widget.rowCount()) // 2
        self.col_limit = (self.table_widget.columnCount() * 3) // 4
        print(self.row_limit, self.col_limit)

        #Create a layout and add the scroll area
        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        
        #Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        ##################################


    ########### INIT METHOD END #############





    #Import a csv file function
    def importCSV(self):
        
        #find file
        fileName = self.openFileDialog()
        if not fileName:
            return
            
        self.file_name = fileName
        
        #populate tempFile
        with open(fileName, 'r') as file:

            row = 0
            for line in file.readlines():
                line = line.strip()
                lineArray = line.split(',')
                self.temp_array.append(lineArray)
                #print(lineArray)
                
                #we also have to populate the graph
                for col in range(len(lineArray)):
                        self.table_widget.setItem(row, col, QTableWidgetItem(lineArray[col]))
                row += 1

        print("File Imported")



        
    #Save work
    def save(self, fileName):

        if not fileName:
            self.warning("No file name specified, use Save As")
            return

        #saves temp file to the filename given
        with open(fileName, 'w') as file:
            
            delimeter = ','
            for line in self.temp_array:
                file.write(delimeter.join(line) + os.linesep)

        print("File Saved To", fileName)

        

        
    #Save as if the you want to save it as a new file
    def saveAs(self):
        #just call save function with file name
        fileName = self.saveAsDialog()
        if not fileName:
            return
        self.FileName = fileName
        self.save(fileName)




    #being able to copy and paste entire chunks??
    def copy(self):
        pass

    def paste(self):
        pass

    def insert(self):
        pass

    def find(self):
        pass



    def handleItemChanged(self, item):
        #if a row we click on isnt in temp array then we will build our way there 
        row = item.row()
        col = item.column()

        length = row + 1 - len(self.temp_array)
        if length > 0:
            for _ in range(length):
                self.temp_array.append([""])

        length = col + 1 - len(self.temp_array[row])
        if length > 0:
            for _ in range(length):
                self.temp_array[row].append("")
            
        self.temp_array[row][col] = item.text()




    #If scroll gets 2/3 the way to the end then add more
    def scrollPositionChangedHorizontal(self, value):
        
        if value > self.col_limit:
            #add another 30 columns
            self.col_limit = (self.table_widget.columnCount() * 3) // 4

            lastRows = self.table_widget.rowCount()
            lastCols = self.table_widget.columnCount()
            self.table_widget.setColumnCount(lastCols + 30)
            for col in range(lastCols, lastCols+30):
                for row in range(lastRows):
                    self.table_widget.setItem(row, col, QTableWidgetItem(""))





    def scrollPositionChangedVertical(self, value):
        
        if value > self.row_limit:
            #add another 50 rows
            self.row_limit = (self.table_widget.rowCount() * 3) // 4

            lastRows = self.table_widget.rowCount()
            lastCols = self.table_widget.columnCount()
            self.table_widget.setRowCount(lastRows + 50)
            for row in range(lastRows, lastRows+50):
                for col in range(lastCols):
                    self.table_widget.setItem(row, col, QTableWidgetItem(""))


        



    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;CSV Files (*.csv)", options=options)

        while not fileName.endswith(".csv"):

            if self.tryAgain("Invalid File Name,\nMust be a .CSV\nTry Again?"):
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;CSV Files (*.csv)", options=options)
            else:
                return
        return fileName



    def saveAsDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*);;CSV Files (*.csv)", options=options)

        while not fileName.endswith(".csv"):

            if self.tryAgain("Invalid File Name,\nMust be a .CSV\nTry Again?"):
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*);;CSV Files (*.csv)", options=options)
            else:
                return
        return fileName
    


    #Delete ranges of stuff
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selectedRanges = self.table_widget.selectedRanges()
            
            for selectedRange in selectedRanges:
                rowCount = selectedRange.rowCount()
                colCount = selectedRange.columnCount()
                leftCol = selectedRange.leftColumn()
                topRow = selectedRange.topRow()
                
                for row in range(topRow, topRow + rowCount):
                    for col in range(leftCol, leftCol + colCount):
                        self.table_widget.setItem(row, col, QTableWidgetItem(""))



    ############## ERROR MESSAGES ###############    
    def tryAgain(self, text):
        ret = QMessageBox.critical(self, "Critical Message!", text, QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok : 
            print("User chose OK")
            return True
        else : 
            print ("User chose Cancel")
            return False
        

    def warning(self, text):
        ret = QMessageBox.critical(self, "Critical Message!", text, QMessageBox.Ok)
        return

    



    






