# ライブラリ
import sqlite3
from PyQt5.QtWidgets import *

memo_index = 0

class MemoWindow(QWidget):
    # ウィンド初期化
    def __init__(self):
        super(MemoWindow, self).__init__()

        self.initUI()
        self.acceptDrops()
        self.setFixedSize(1000, 500)
        self.setWindowTitle("メモ")

    # UI初期化
    def initUI(self):
        self.memolist = QListWidget()
        self.getSummary()
        self.memolist.itemClicked.connect(self.changeMemo)
        self.memolist.setCurrentRow(0)

        self.memopad = QTextEdit()

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT content FROM memo;"
        results = cursor.execute(query).fetchone()
        if results is None:
            self.memopad.setPlainText("メモがないよ\n追加ボタンでメモを追加してね")
        else:
            for result in results:
                self.memopad.setPlainText(result)

        self.add = QPushButton("追加")
        self.add.clicked.connect(self.addMemo)
        self.delete = QPushButton("削除")
        self.delete.clicked.connect(self.deleteMemo)

        layout = QGridLayout()
        layout.addWidget(self.add, 0, 6)
        layout.addWidget(self.delete, 0, 7)
        layout.addWidget(self.memolist, 1, 0, 1, 3)
        layout.addWidget(self.memopad, 1, 3, 1, 5)
        self.setLayout(layout)

        self.changeMemo()


    # ウィンド閉じる時の動作
    def closeEvent(self, e):
        self.saveMemo()
        self.getSummary()
        self.close()

    # メモの目次を取得
    def getSummary(self):
        global memo_index
        summary = []

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT memoName FROM memo;"
        results = cursor.execute(query).fetchall()
        if results is None:
            self.memolist.clear()
        else:
            for result in results:
                summary.append(str(result[0]))
            self.memolist.clear()
            self.memolist.addItems(summary)
            self.memolist.setCurrentRow(memo_index)

    # 表示するメモをかえる
    def changeMemo(self):
        global memo_index
        self.saveMemo()
        i = int(self.memolist.currentRow())
        memo_index = i
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT memoId FROM memo LIMIT 1 OFFSET ?;"
        results = cursor.execute(query, (memo_index,)).fetchone()
        if results is None:
            pass
        else:
            for result in results:
                id = result
            query = "SELECT content FROM memo WHERE memoId = ?;"
            results = cursor.execute(query, (id,)).fetchall()
            if results is None:
                pass
            else:
                for result in results:
                    self.memopad.setPlainText(str(result[0]))
                    self.getSummary()

    # メモを追加
    def addMemo(self):
        global memo_index
        self.saveMemo()

        name = ""
        text = ""
        row = (name, text,)
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "INSERT INTO memo (memoName, content) VALUES (?,?);"
        cursor.execute(query, row)
        conn.commit()
        self.getSummary()
        query = "SELECT COUNT(*) FROM memo;"
        i = cursor.execute(query).fetchone()
        i = i[0] - 1
        self.memolist.setCurrentRow(i)
        memo_index = i
        self.memopad.setPlainText("")
        self.changeMemo()

    # メモを保存　自動保存
    def saveMemo(self):
        global memo_index
        try:
            text = self.memopad.toPlainText()
            name = self.memopad.toPlainText().split("\n")
            name = name[0]
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            query = "SELECT memoId FROM memo LIMIT 1 OFFSET ?;"
            results = cursor.execute(query, (memo_index,)).fetchone()
            if results is None:
                pass
            else:
                for result in results:
                    id = result
                row = (name, text, id,)
                query = "UPDATE memo SET memoName = ?, content = ? WHERE memoId = ?;"
                cursor.execute(query, row)
                conn.commit()
        except:
            pass

    # メモを削除
    def deleteMemo(self):
        global memo_index
        print(memo_index)
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT memoId FROM memo LIMIT 1 OFFSET ?;"
        results = cursor.execute(query, (memo_index,)).fetchone()
        if results is None:
            pass
        else:
            for result in results:
                id = result
            query = "DELETE FROM memo WHERE memoId = ?;"
            cursor.execute(query, (id,))
            conn.commit()

        self.memolist.setCurrentRow(0)
        memo_index = 0
        query = "SELECT memoId FROM memo LIMIT 1 OFFSET ?;"
        results = cursor.execute(query, (memo_index,)).fetchone()
        if results is None:
            self.getSummary()
            self.memopad.setPlainText("メモがないよ\n追加ボタンでメモを追加してね")
        else:
            for result in results:
                id = result
                query = "SELECT content FROM memo WHERE memoId = ?;"
                results = cursor.execute(query, (id,)).fetchall()
                if results is None:
                    pass
                else:
                    for result in results:
                        self.memopad.setPlainText(str(result[0]))
                        self.getSummary()
