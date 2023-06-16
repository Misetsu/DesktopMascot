#ライブラリ
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QLocale, QDate, Qt, QTimer, QTime
from PyQt5.QtGui import QFont

date_index = QDate.currentDate()
date_index = date_index.toString("yyyyMMdd")
alarm_list = []
on_alarm = []
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
        self.saveAlarm()
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
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/diary" + d + ".txt"
        # ファイルを新しく作る、エラーは無視、最後にファイルを読み込む
        try:
            open(p, "x", encoding="utf-8")
        except:
            pass
        finally:
            # Read & write
            with open(p, "r+", encoding="utf-8") as file:
                data = file.read()
            self.diary.setPlainText(data)

    # 日記保存
    def saveDiary(self):
        global date_index
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/diary" + d + ".txt"
        # Overwrite
        with open(p, "w", encoding="utf-8") as file:
            file.write(self.diary.toPlainText())

    # タスクを取得
    def getTask(self):
        global date_index
        self.task.clear()
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/task" + d + ".txt"
        # ファイルを新しく作る、エラーは無視、最後にファイルを読み込む
        try:
            open(p, "x", encoding="utf-8")
        except:
            pass
        finally:
            with open(p, "r+", encoding="utf-8") as file:
                lines = [line.rstrip() for line in file]
            for line in lines:
                flg, name = line.split("&_sep_&")
                item = QListWidgetItem(name)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if flg == "1":
                    item.setCheckState(Qt.Checked)
                elif flg == "0":
                    item.setCheckState(Qt.Unchecked)
                self.task.addItem(item)

    # タスクを追加
    def addTask(self):
        global date_index
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/task" + d + ".txt"
        text = self.input.text()
        # 最後に追加
        with open(p, "a", encoding="utf-8") as file:
            file.write("0&_sep_&" + text + "\n")
        self.input.setText("")
        self.getTask()

    # タスクを保存
    def saveTask(self):
        global date_index
        all_task = ""
        # アイテムごとにチェック
        for i in range(self.task.count()):
            item = self.task.item(i)
            if item.checkState() == Qt.Checked:
                all_task = all_task + "1&_sep_&" + item.text() + "\n"
            elif item.checkState() == Qt.Unchecked:
                all_task = all_task + "0&_sep_&" + item.text() + "\n"
        # ファイルの場所を取得
        d = date_index
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/task" + d + ".txt"
        # Overwrite
        with open(p, "w", encoding="utf-8") as file:
            file.write(all_task)
        self.getTask()

    # 画面2UI
    def stack2UI(self):
        global alarm_list, on_alarm, on_time
        alarm_list = []
        on_alarm = []
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/alarm.txt"
        # 保存しているアラームを取得
        try:
            with open(p, "r+", encoding="utf-8") as file:
                lines = [line.rstrip() for line in file]
            alarm_list = lines[0].split(" ")
            on_alarm = lines[1].split(" ")
            on_time = lines[2].split(" ")
        finally:
            pass

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
        global alarm_list, on_alarm
        # ループでlist itemを作る
        for i in range(len(alarm_list)):
            self.item = QListWidgetItem()
            self.item_widget = QWidget()
            self.line_text = QLabel(alarm_list[i])
            self.line_push_button = QPushButton("オフ")
            self.line_push_button.setObjectName("switch " + str(i))
            self.line_push_button.setCheckable(True)
            if alarm_list[i] in on_alarm:
                self.line_push_button.setChecked(True)
                self.line_push_button.setText("On")
            self.line_push_button.clicked.connect(self.clicked)
            self.delete_button = QPushButton("削除")
            self.delete_button.setObjectName("del " + str(i))
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
        global alarm_list, on_alarm, on_time
        time_str = str(alarm_list[i])
        on_alarm.append(time_str)
        time_str = time_str + ":00"
        on_time.append(time_str)

    # アラームをオフにする
    def alarmOff(self, i):
        global alarm_list,on_alarm, on_time
        time_str = alarm_list[i]
        try:
            on_alarm.remove(time_str)
        except:
            pass
        time_str = str(time_str) + ":00"
        try:
            on_time.remove(time_str)
        except:
            pass

    # アラームを追加
    def addAlarm(self):
        global alarm_list
        t = self.time_edit.time().toString()
        t = t[:-3]
        alarm_list.append(t)
        self.ListWidget.clear()
        self.getAlarmList()

    # アラームを削除
    def delAlarm(self):
        global alarm_list
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        t, i = push_button.objectName().split(" ")
        i = int(i)
        self.alarmOff(i)
        alarm_list.pop(i)
        self.ListWidget.clear()
        self.getAlarmList()

    # アラームを保存
    def saveAlarm(self):
        global alarm_list, on_alarm, on_time
        data = ""
        for i in alarm_list:
            data = data + i + " "
        data = data + "\n"
        for i in on_alarm:
            data = data + i + " "
        data = data + "\n"
        for i in on_time:
            data = data + i + " "
        data = data + "\n"
        cwd = os.getcwd()
        cwd = cwd + "/calendar"
        p = cwd + "/alarm.txt"
        try:
            with open(p, "w", encoding="utf-8") as file:
                file.write(data)
        finally:
            pass