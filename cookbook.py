import sqlite3
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication
from pathlib import Path


class Database():

    def __init__(self) -> None:
        self.connection = sqlite3.connect("Cookbook.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE if not EXISTS "Rezepte" ( "idrezept" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "Name" TEXT, "Buchseite" INTEGER, "PDF" TEXT, "Jahreszeit" TEXT, "Gekocht" BOOL,
                            "Bewertung" TEXT, "Kommentar" TEXT)''')
        self.cursor.execute('''CREATE TABLE if not EXISTS "Zutaten" ( "idzutat" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "Zutat" TEXT, "idrezept" INTEGER, FOREIGN KEY("idrezept") REFERENCES Rezepte("idrezept"))''')

    def db_write_recepies(self, data):
        for row_data in data:
            newentity = (
                data[0], data[1], data[2], ", ".join(data[3]),
                data[4], data[5], data[6])
            recepielist = self.cursor.execute('SELECT Name, Buchseite, PDF, Jahreszeit, Gekocht, Bewertung, Kommentar FROM Rezepte').fetchall()
            if newentity in recepielist:
                pass
            else:
                self.cursor.execute('''INSERT INTO "Rezepte" (Name, Buchseite, PDF, Jahreszeit, 
                                    Gekocht, Bewertung, Kommentar) VALUES (?, ?, ?, ?, ?, ?, ?)''', newentity)
                self.connection.commit()

    def db_write_ingredients(self, ingredient_snippets):
        for snippet in ingredient_snippets:
            existing_ingredients = self.cursor.execute('''SELECT Zutat FROM Zutaten''').fetchall()
            if (snippet,) in existing_ingredients:
                pass
            else:
                self.cursor.execute('''INSERT INTO Zutaten (Zutat) VALUES (?)''', (snippet,))
                self.connection.commit()


class MainWindow(QtWidgets.QMainWindow, Database):

    def __init__(self) -> None:
        QtWidgets.QMainWindow.__init__(self)
        Database.__init__(self)
        self.ui = uic.load_ui.loadUi(Path(__file__).parent / "cookbook.ui", self)
        self.ui.pb_write_w.clicked.connect(self.write_recepies)
        self.ui.pb_write_w.clicked.connect(self.write_ingredients)

    def write_recepies(self):
        data = [
            self.le_name_w.text(),
            self.le_seite_w.text(),
            self.le_pdf_w.text(),
            [
                "Herbst" if self.cb_autumn_w.isChecked() else "",
                "Sommer" if self.cb_summer_w.isChecked() else "",
                "Winter" if self.cb_winter_w.isChecked() else "",
                "Frühling" if self.cb_spring_w.isChecked() else ""
            ],
            self.cb_cook_w.isChecked(),
            self.le_bewertung_w.text(),
            self.txte_kommentar_w.toPlainText()
        ]
        self.db_write_recepies(data)

    def write_ingredients(self):
        ingredients_text = self.txte_zutaten_w.toPlainText()
        ingredient_snippets = [snippet.strip() for snippet in ingredients_text.split(',') if snippet.strip()]
        if ingredient_snippets:
            self.db_write_ingredients(ingredient_snippets)


class Main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


Main()
