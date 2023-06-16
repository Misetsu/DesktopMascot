# ライブラリ
import os
from PyQt5.QtWidgets import *
from datetime import datetime

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
        try:
            cwd = os.getcwd()
            cwd = cwd + "/memo"
            l = [f for f in os.listdir(cwd) if f.endswith("memo.txt")]
            p = cwd + "/" + l[0]
            # Read & write
            with open(p, "r+", encoding="utf-8") as file:
                data = file.read()
            self.memopad.setPlainText(data)
        except:
            self.memopad.setPlainText("メモがないよ\nAddボタンでメモを追加してね")

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
        # ファイルの場所を取得
        summary = []
        cwd = os.getcwd()
        cwd = cwd + "/memo"
        l = [f for f in os.listdir(cwd) if f.endswith("memo.txt")]
        for i in l:
            p = cwd + "/" + i
            # Read only
            with open(p, "r", encoding="utf-8") as file:
                first_line = file.readline().strip('\n') # 1行目
            summary.append(first_line)
        # 更新
        self.memolist.clear()
        self.memolist.addItems(summary)
        self.memolist.setCurrentRow(memo_index)

    # 表示するメモをかえる
    def changeMemo(self):
        global memo_index
        self.saveMemo()
        try:
            # ファイルの場所を取得
            i = int(self.memolist.currentRow())
            memo_index = i
            cwd = os.getcwd()
            cwd = cwd + "/memo"
            l = [f for f in os.listdir(cwd) if f.endswith("memo.txt")]
            p = cwd + "/" + l[i]
            # Read & write
            with open(p, "r+", encoding="utf-8") as file:
                data = file.read()
            self.memopad.setPlainText(data)
            self.getSummary()
        except:
            pass

    # メモを追加
    def addMemo(self):
        global memo_index
        self.saveMemo()
        # ファイルの場所を取得
        t = datetime.now()
        ct = t.strftime("%Y%m%d%H%M%S")
        name = ct + "memo.txt"
        cwd = os.getcwd()
        cwd = cwd + "/memo"
        p = cwd + "/" + name
        try:
            open(p, "x", encoding="utf-8")
            l = [f for f in os.listdir(cwd) if f.endswith("memo.txt")]
            for i in range(len(l)):
                if l[i].endswith(name):
                    break
            self.memolist.setCurrentRow(i)
            memo_index = i
            self.memopad.setPlainText("")
            self.changeMemo()
        except:
            pass

    # メモを保存　自動保存
    def saveMemo(self):
        global memo_index
        try:
            # ファイルの場所を取得
            i = int(self.memolist.currentRow())
            cwd = os.getcwd()
            cwd = cwd + "/memo"
            l = [f for f in os.listdir(cwd) if f.endswith("memo.txt")]
            p = cwd + "/" + l[memo_index]
            # Overwrite
            with open(p, "w", encoding="utf-8") as file:
                file.write(self.memopad.toPlainText())
        except:
            pass

    # メモを削除
    def deleteMemo(self):
        global memo_index
        # ファイルの場所を取得
        i = int(self.memolist.currentRow())
        cwd = os.getcwd()
        cwd = cwd + "/memo"
        l = [f for f in os.listdir(cwd) if f.endswith("memo.txt")]
        p = cwd + "/" + l[i]
        # ファイルがあるかチェック
        if os.path.exists(p):
            os.remove(p)
        # 更新
        try:
            memo_index = 0
            cwd = os.getcwd()
            cwd = cwd + "/memo"
            l = [f for f in os.listdir(cwd) if f.endswith("memo.txt")]
            p = cwd + "/" + l[0]
            # Read & write
            with open(p, "r+", encoding="utf-8") as file:
                data = file.read()
            self.memopad.setPlainText(data)
            self.getSummary()
        except:
            self.getSummary()
            self.memopad.setPlainText("メモがないよ\nAddボタンでメモを追加してね")
