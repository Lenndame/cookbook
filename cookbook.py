import sqlite3
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView
from pathlib import Path


#connection to sqlite database methods to add new entities to database and to read from database
class Database():

    def __init__(self) -> None:
        self.connection = sqlite3.connect("Cookbook.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE if not EXISTS "Rezepte" ( "idrezept" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "Name" TEXT, "Buchseite" INTEGER, "PDF" TEXT, "Jahreszeit" TEXT, "Gekocht" TEXT,
                            "Bewertung" TEXT, "Kommentar" TEXT)''')
        self.cursor.execute('''CREATE TABLE if not EXISTS "Zutaten" ( "idzutat" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "idrezept" INTEGER, FOREIGN KEY("idrezept") REFERENCES Rezepte("idrezept"))''')

    def write_recepies(self, data):
        id_list = []
        for row_data in data:
            newentity = (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6], row_data[7], row_data[8])
            recepielist = self.cursor.execute('SELECT Name, Buchseite, PDF, Jahreszeit, Gekocht, Bewertung, Kommentar FROM Rezepte').fetchall()
            if newentity in recepielist:
                pass
            else:
                self.cursor.execute('''INSERT INTO "Rezepte" (Name, Buchseite, PDF, Jahreszeit, 
                                    Gekocht, Bewertung, Kommentar) VALUES (?, ?, ?, ?, ?, ?, ?)''', newentity)
                self.connection.commit()
            id = self.cursor.execute('''SELECT idPerson FROM persons WHERE Name = ? AND Buchseite = ? AND PDF = ? 
                                     AND Jahreszeit = ? AND Bewertung = ? AND Kommentar = ? ''', newentity).fetchone()
            id_list.append(id[0])
        return id_list

    def write_ingredient(self, data, idrezept):
        for i in range(len(data)):
            newentity = (data[i][9])
            newentity.append(idrezept[i])
            ingredientlist = self.cursor.execute('''SELECT Zutat FROM Zutaten''').fetchall()
            if newentity in ingredientlist:
                pass
            else:
                self.cursor.execute('''INSERT INTO Zutaten (Zutat) VALUES (?)''', newentity)
                self.connection.commit()


class MainWindow(QtWidgets.QMainWindow, Database):

    def __init__(self) -> None:
        QtWidgets.QMainWindow.__init__(self)
        Database.__init__(self)
        self.ui = uic.load_ui.loadUi(Path(__file__).parent / "cookbook.ui", self)


class Main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


Main()
