import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)

        self.filename = ""

        self.initUI()
        
        
    def cursorPosition(self):
        cursor = self.text.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        
        self.statusbar.showMessage("Line:{} | Column:{} ".format(line,col))
            
            
    def new(self):

        spawn = Main(self)
        spawn.show()

    def open(self):

        # Get filename and show only .writer files
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.txt)")

        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())

    def save(self):
    
        # Only open dialog if there is no filename yet
        if not self.filename:
            self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

        # Append extension if not there yet
        if not self.filename.endswith('.txt'):
            self.filename += ".txt"

        # We just store the contents of the text file along with the
        # format in html, which Qt does in a very nice way for us
        with open(self.filename,"wt") as file:
            file.write(self.text.toHtml())
    def preview(self):

        # Open preview dialog
        preview = QtGui.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))

        preview.exec_()

    def printf(self):
    
        # Open printing dialog
        dialog = QtGui.QPrintDialog()

        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())
    def initToolbar(self):

        self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New",self)
        self.newAction.setStatusTip("Create a new document from scratch.")
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        
        self.cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

       
        self.toolbar.addSeparator()

        # Makes the next toolbar appear underneath this one
        self.addToolBarBreak()
        
        self.printfAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
        self.printfAction.setStatusTip("Print document")
        self.printfAction.setShortcut("Ctrl+P")
        self.printfAction.triggered.connect(self.printf)

        self.previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"),"Page view",self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)
        
        self.toolbar.addAction(self.printfAction)
        self.toolbar.addAction(self.previewAction)

        self.toolbar.addSeparator()
    def initFormatbar(self):
        
        fontBox = QtGui.QFontComboBox(self)
        fontBox.currentFontChanged.connect(self.fontFamily)
        
        fontSize = QtGui.QComboBox(self)
        fontSize.setEditable(True)
        fontSize.setMinimumContentsLength(3)
        
        fontSize.activated.connect(self.fontSize)
        
        #Typical font sizes
        fontSizes = ['6','7','8','9','10','11','12','13','14','15','16','17','18','20','22','24','26','28','32','36','40','44','48','54','60','66','72','80','88','96']
        for i in fontSizes:
            fontSize.addItem(i)
        fontColor =  QtGui.QAction(QtGui.QIcon("icons/font-color.png"),"font color",self)
        fontColor.triggered.connect(self.fontColor)
        
        backColor = QtGui.QAction(QtGui.QIcon("icons/highlight.png"),"Background Color",self)
        backColor.triggered.connect(self.highlight)
        
        self.formatbar = self.addToolBar("Format")
        
        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)
        
        self.formatbar.addSeparator()
        
        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)
        
        self.formatbar.addSeparator()
        
        boldAction = QtGui.QAction(QtGui.QIcon("icons/bold.png"),"Bold",self)
        boldAction.triggered.connect(self.bold)
        
        italicAction =  QtGui.QAction(QtGui.QIcon("icons/italic.png"),"Italic",self)
        italicAction.triggered.connect(self.italic)
        
        underlAction = QtGui.QAction(QtGui.QIcon("icons/underline.png"),"Underline",self)
        underlAction.triggered.connect(self.underline)
        
        strikeAction = QtGui.QAction(QtGui.QIcon("icons/strike.png"),"Strike",self)
        strikeAction.triggered.connect(self.strike)
        
        #superAction = QtGui.Action(QtGui.QIcon("icons/superscript"),"Superscript",self)
        #superAction.triggered.connect(self.superScript)
        
        #subAction = QtGui.QAction(QtGui.QIcon("icons/subscript.png"),"Subsript",self)
        #ssubAction.triggered.connect(self.subScript)
        
        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        #self.formatbar.addAction(superAction)
        #self.formatbar.addAction(subAction)
        
        self.formatbar.addSeparator()
        
    def initMenubar(self):

        menubar = self.menuBar()
    
        file = menubar.addMenu("File")
        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")
        file.addAction(self.printfAction)
        file.addAction(self.previewAction)
        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)

    def initUI(self):

        self.text = QtGui.QTextEdit(self)
        self.setCentralWidget(self.text)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1030,800)

        self.setWindowTitle("WriteMe")
        #self.setWindowIcon(web.jpg)
        
    def fontFamily(self,font):
        self.text.setCurrentFont(font)
    def fontSize(self,fontSize):
        self.text.setFontPointSize(int(fontSize))
        
    def fontColor(self):
        
        color = QtGui.QColorDialog.getColor()
        self.text.setTextColor(color)
    def highlight(self):
         
        color = QtGui.QColorDialog.getColor()
        
        self.text.setTextBackgroundColor(color)
        
    def bold(self):
        
        if self.text.fontWeight() == QtGui.QFont.Bold:
            self.text.setFontWeight(QtGui.QFont.Normal)
        else:  
            
            self.text.setFontWeight(QtGui.QFont.Bold)
    def italic(self):
        
        state = self.text.fontItalic()
        
        self.text.setFontItalic(not state)
    def underline(self):
        
        state = self.text.fontUnderline()
        
        self.text.setFontUnderline(not state)
    def strike(self):
        fmt = self.text.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.text.setCurrentCharFormat(fmt)
    #def 
def main():

    app = QtGui.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
