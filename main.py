from PyQt5.QtCore import Qt  
from notes import Ui_MainWindow 
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox 
from data import write_json, read_json 
 
 
class MainWindow(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self) 
        self.name_file = "notes.json" 
        self.notes = read_json(self.name_file) 
        name_note = list(self.notes.keys()) 
        self.ui.note_list.addItems(name_note) 
        name_note = name_note[0] 
        self.set_note(name_note) 
        self.connects() 
 
    def set_note(self, name_note): 
        note = self.notes[name_note] 
        self.ui.text_edit.clear() 
        self.ui.text_edit.setText(note["text"]) 
        self.ui.teg_list.clear()  
        self.ui.teg_list.addItems(note["teg"]) 
        item = self.ui.note_list.findItems(name_note, Qt.MatchExactly) 
        n = self.ui.note_list.row(item[0]) 
        self.ui.note_list.setCurrentRow(n) 
 
    def add_note(self): 
        name_note, do = QInputDialog.getText(self, 
                                            "notes_edit", 
                                            "Введіть назву нової замітки") 
        self.notes[name_note] = {"text": "", "teg": []} 
        write_json(self.notes, self.name_file) 
        self.ui.note_list.addItem(name_note) 
        self.set_note(name_note) 
    
    def add_teg(self):
        name_teg, do = QInputDialog.getText(self, 
                                            "notes_edit", 
                                            "Введіть назву нового тегу") 
        name_note = self.ui.note_list.currentItem().text()
        self.notes[name_note]["teg"].append(name_teg)
        write_json(self.notes, self.name_file)
        self.ui.teg_list.addItem(name_teg)

    def find_teg(self):
        teg = self.ui.text_edit.text()
        teg_notes = dict()
        for name_note in self.notes:
            if teg in self.notes[name_note]["teg"]:
                teg_notes[name_note] = self.notes[name_note]
        self.ui.note_list.clear()
        names = list(teg_notes.keys())
        self.ui.note_list.addItems(names)
        self.set_note(names[0])

    def del_teg(self):
        item = self.ui.teg_list.currentItem() 
        name_teg = item.text()
        num = self.ui.note_list.row(item)
        item = self.ui.note_list.currentItem()
        name_note = item.text()
        self.notes[name_note].remove(name_teg)
        write_json(self.notes,self.name_file) 
        self.ui.teg_list.takeItem(num)
    

    def delete_note(self): 
        item = self.ui.note_list.currentItem() 
        name_note = item.text() 
        num = self.ui.note_list.row(item) 
        del self.notes[name_note] 
        write_json(self.notes,self.name_file) 
        self.ui.note_list.takeItem(num) 
     
    def save_note(self): 
        item = self.ui.note_list.currentItem() 
        name_note = item.text() 
        text = self.ui.text_edit.toPlainText() 
        self.notes[name_note]["text"] = text 
        write_json(self.notes,self.name_file) 
        mes = QMessageBox(self.ui.main_win) 
        mes.setText("Замітку збережено") 
        mes.show() 
        mes.exec() 
 
    def connects(self): 
        self.ui.btn_del_note.clicked.connect(self.delete_note) 
        self.ui.btn_add_note.clicked.connect(self.add_note) 
        self.ui.btn_find_teg.clicked.connect(self.find_teg) 
        self.ui.btn_save_note.clicked.connect(self.save_note) 
        self.ui.note_list.itemClicked.connect(self.click_note) 
        #self.ui.note_list.currentRowChanged.connect(self.click_note) 
         
    def click_note(self):     
        item = self.ui.note_list.currentItem() 
        name_note = item.text() 
        self.set_note(self.click_note) 
 
app = QApplication([]) 
win = MainWindow() 
win.show() 
app.exec()