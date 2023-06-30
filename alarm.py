#ライブラリ
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QLocale, QDate, Qt, QTimer, QTime
from PyQt5.QtGui import QFont

date_index = QDate.currentDate()
date_index = date_index.toString("yyyyMMdd")
on_time = []

class AlarmWindow(QWidget):
    # ウィンド初期化
    def __init__(self):
        super(AlarmWindow, self).__init__()

        self.setFixedSize(1000, 500)
        self.setWindowTitle("アラーム")

        self.button = QPushButton("")
        self.button.clicked.connect(self.changeLayout)

        self.stack1 = QWidget()  #画面1：日記/タスク
        self.stack2 = QWidget()  #画面2：アラーム

        self.stack1UI()
        self.stack2UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        layout = QGridLayout(self)
        layout.addWidget(self.Stack, 0, 0, 1, 5)
        layout.addWidget(self.button, 3, 4)
        self.setLayout(layout)

    # 画面切り替え動作
    def changeLayout(self):
        i = self.Stack.currentIndex()
        if i == 1:
            self.Stack.setCurrentIndex(0)
            self.button.setText("カレンダー画面")
        else:
            self.saveDiary()
            self.saveTask()
            self.Stack.setCurrentIndex(1)
            self.button.setText("アラーム画面")

    # ウィンドを閉じる時の動作
    # 自動保存
    def closeEvent(self, e):
        self.saveDiary()
        self.saveTask()
        # self.saveAlarm()
        self.close()

    # 画面1UI
    def stack1UI(self):
        self.cal = QCalendarWidget(self)
        self.cal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.cal.setLocale(QLocale(QLocale.Japanese))
        self.cal.setGridVisible(True)
        self.cal.selectionChanged.connect(self.dateChange)
        self.cal.setSelectedDate(QDate.currentDate())

        self.date = QLabel("")

        self.diary = QTextEdit()

        self.input = QLineEdit()
        self.add = QPushButton("追加")
        self.add.clicked.connect(self.addTask)
        self.task = QListWidget()

        layout = QGridLayout()
        layout.addWidget(self.cal, 0, 0, 8, 4)
        layout.addWidget(self.date, 0, 4)
        layout.addWidget(self.diary, 1, 4, 3, 4)
        layout.addWidget(self.input, 4, 4, 1, 3)
        layout.addWidget(self.add, 4, 7)
        layout.addWidget(self.task, 5, 4, 3, 4)

        # 初期画面の読み込み
        self.getDiary()
        self.getTask()
        self.dateChange()
        self.stack1.setLayout(layout)

    # 日付切り替え動作
    def dateChange(self):
        global date_index
        self.saveDiary()
        self.saveTask()
        d = self.cal.selectedDate()
        date_index = d.toString("yyyyMMdd")
        w = d.toString("yyyy年M月d日")
        self.date.setText(w)
        self.getDiary()
        self.getTask()

    # 日記を取得
    def getDiary(self):
        global date_index
        d = date_index
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT content FROM diary WHERE diaryDate = ?;"
        results = cursor.execute(query, (d,)).fetchone()
        if results is None:
            query = "INSERT INTO diary (diaryDate, content) VALUES (?,?);"
            row = (d, "", )
            cursor.execute(query, row)
            conn.commit()
            self.diary.setPlainText("")
        else:
            for result in results:
                self.diary.setPlainText(result)

    # 日記保存
    def saveDiary(self):
        global date_index
        # ファイルの場所を取得
        d = date_index
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "UPDATE diary SET content = ? WHERE diaryDate = ?;"
        row = (self.diary.toPlainText(), d,)
        cursor.execute(query, row)
        conn.commit()

    # タスクを取得
    def getTask(self):
        global date_index
        self.task.clear()
        d = date_index
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT taskName, switch FROM task WHERE taskDate = ?;"
        results = cursor.execute(query, (d,)).fetchall()
        if results is None:
            pass
        else:
            for result in results:
                item = QListWidgetItem(result[0])
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if result[1] == 1:
                    item.setCheckState(Qt.Checked)
                elif result[1] == 0:
                    item.setCheckState(Qt.Unchecked)
                self.task.addItem(item)

    # タスクを追加
    def addTask(self):
        global date_index
        d = date_index
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "INSERT INTO task (taskDate, taskName, switch) VALUES (?,?,?);"
        row = (d, self.input.text(), 0,)
        cursor.execute(query, row)
        conn.commit()
        self.input.setText("")
        self.getTask()

    # タスクを保存
    def saveTask(self):
        global date_index
        d = date_index
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        for i in range(self.task.count()):
            item = self.task.item(i)
            if item.checkState() == Qt.Checked:
                row = (1, d, item.text(),)
            elif item.checkState() == Qt.Unchecked:
                row = (0, d, item.text(),)
            query = "UPDATE task SET switch = ? WHERE taskDate = ? AND taskName = ?;"
            cursor.execute(query, row)
        conn.commit()
        self.getTask()

    # 画面2UI
    def stack2UI(self):
        self.time = QLabel()
        self.time.setFont(QFont('Arial', 30))
        self.time.setAlignment(Qt.AlignCenter)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setDisplayFormat("hh:mm")

        self.add_alarm = QPushButton("追加")
        self.add_alarm.clicked.connect(self.addAlarm)

        self.Frame = QGroupBox()
        self.FrameHorizontalLayout = QHBoxLayout(self.Frame)
        self.ListWidget = QListWidget(self.Frame)
        self.ListWidget.setSpacing(11)
        self.ListWidget.setStyleSheet(
            "QListWidget { background: palette(window); border: none;}"
            "QListWidget::item {"
            "border-style: solid;"
            "border-width:1px;"
            "border-color:  black;"
            "margin-right: 30px;"
            "}"
            "QListWidget::item:hover {"
            "border-color: blue;"
            "}")
        self.FrameHorizontalLayout.addWidget(self.ListWidget)

        self.layout2 = QGridLayout(self)
        self.layout2.addWidget(self.time, 0, 0, 8, 4)
        self.layout2.addWidget(self.time_edit, 0, 4, 1, 3)
        self.layout2.addWidget(self.add_alarm, 0, 7, 1, 1)
        self.layout2.addWidget(self.Frame, 1, 4, 7, 4)
        self.getAlarmList()
        self.stack2.setLayout(self.layout2)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    # 時計を表示
    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString("hh:mm:ss")
        self.time.setText(label_time)

    # アラームを表示
    def getAlarmList(self):
        self.ListWidget.clear()
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT * FROM alarm;"
        results = cursor.execute(query).fetchall()
        if results is None:
            pass
        else:
            # ループでlist itemを作る
            for result in results:
                self.item = QListWidgetItem()
                self.item_widget = QWidget()
                self.line_text = QLabel(result[1])
                self.line_push_button = QPushButton()
                self.line_push_button.setObjectName("switch " + str(result[0]))
                self.line_push_button.setCheckable(True)
                if result[3] == 1:
                    self.line_push_button.setChecked(True)
                    self.line_push_button.setText("オン")
                elif result[3] == 0:
                    self.line_push_button.setText("オフ")
                self.line_push_button.clicked.connect(self.clicked)
                self.delete_button = QPushButton("削除")
                self.delete_button.setObjectName("del " + str(result[0]))
                self.delete_button.clicked.connect(self.delAlarm)
                self.item_layout = QHBoxLayout()
                self.item_layout.addWidget(self.line_text)
                self.item_layout.addWidget(self.line_push_button)
                self.item_layout.addWidget(self.delete_button)
                self.item_widget.setLayout(self.item_layout)
                self.item.setSizeHint(self.item_widget.sizeHint())
                self.ListWidget.addItem(self.item)
                self.ListWidget.setItemWidget(self.item, self.item_widget)

    # アラームをオンオフ
    def clicked(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        t, i = push_button.objectName().split(" ")
        i = int(i)
        if push_button.isChecked():
            push_button.setText("オン")
            self.alarmOn(i)
        else:
            push_button.setText("オフ")
            self.alarmOff(i)

    # アラームをオンにする
    def alarmOn(self, i):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "UPDATE alarm SET switch = 1 WHERE alarmId = ?;"
        cursor.execute(query, (i, ))
        conn.commit()
        self.getOnAlarm()

    # アラームをオフにする
    def alarmOff(self, i):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "UPDATE alarm SET switch = 0 WHERE alarmId = ?;"
        cursor.execute(query, (i,))
        conn.commit()
        self.getOnAlarm()

    # アラームを追加
    def addAlarm(self):
        t = self.time_edit.time().toString()
        row = (t[:-3], t[:-3] + ":00", 0,)
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "INSERT INTO alarm (alarmName, time, switch) VALUES (?,?,?);"
        cursor.execute(query, row)
        conn.commit()
        self.getAlarmList()

    # アラームを削除
    def delAlarm(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        t, i = push_button.objectName().split(" ")
        i = int(i)
        self.alarmOff(i)
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "DELETE FROM alarm WHERE alarmId = ?;"
        cursor.execute(query, (i, ))
        conn.commit()
        self.getAlarmList()

    # オンにしたアラームを取得
    def getOnAlarm(self):
        global on_time
        on_time.clear()
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        query = "SELECT time FROM alarm WHERE switch = 1;"
        results = cursor.execute(query).fetchall()
        for result in results:
            on_time.append(result[0])
