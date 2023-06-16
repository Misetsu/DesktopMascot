# ライブラリ
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QTime, QDateTime
from PyQt5.QtGui import *
from alarm import AlarmWindow


class Clock(QDialog):
    # ウィンドウ初期化
    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setGeometry(1450, 680, 400, 100)
        self.setStyleSheet(Stylesheet)
        self.widget = QWidget(self)
        self.initUi()
        # 他ウィンドを定義
        self.alarm_window = AlarmWindow()

    # UI初期化
    def initUi(self):
        # 丸い角のウィンドを作る
        self.widget.setObjectName('Custom_Widget')
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)

        # 要素を追加
        layout = QGridLayout(self.widget)
        layout.addItem(QSpacerItem(40, 20), 0, 0)
        # 閉じるボタン
        close = QPushButton("r", self)
        close.clicked.connect(self.accept)
        close.setObjectName("closeButton")
        # アラーム画面を開くボタン
        alarm = QPushButton("a", self)
        alarm.setObjectName("actionButton")
        alarm.clicked.connect(self.showAlarm)
        # カレンダー画面を開くボタン
        calendar = QPushButton("c", self)
        calendar.setObjectName("actionButton")
        calendar.clicked.connect(self.showCalendar)
        # 時間ラベル
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 30))
        # 日付ラベル
        label1 = QLabel()
        label1.setAlignment(Qt.AlignLeft)
        label1.setFont(QFont('Arial', 12))
        label1.setText(QDateTime.currentDateTime().toString("yyyy年MM月dd日"))
        # レイアウト
        layout.addWidget(label1, 0, 0, 1, 1)
        layout.addWidget(self.label, 1, 0, 2, 1)
        layout.addWidget(close, 0, 1)
        layout.addWidget(calendar, 1, 1)
        layout.addWidget(alarm, 2, 1)
        self.setLayout(layout)
        # 時間ループ
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    # 時計を表示
    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString("hh:mm:ss")
        self.label.setText(label_time)

    # アラーム画面に切り替え
    def showAlarm(self):
        self.alarm_window.Stack.setCurrentIndex(1)
        self.alarm_window.button.setText("カレンダー画面")
        self.alarm_window.show()
        self.close()

    # カレンダー画面に切り替え
    def showCalendar(self):
        self.alarm_window.Stack.setCurrentIndex(0)
        self.alarm_window.button.setText("アラーム画面")
        self.alarm_window.show()
        self.close()

# CSS
Stylesheet = """
#Custom_Widget {
    background: #CCC;
    border-radius: 20px;
    opacity: 100;
    border: 3px solid #1c3561;                   
}
#closeButton {
    min-width: 30px;
    min-height: 30px;
    max-width: 30px;
    max-height: 30px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: #ccc;
    background: red;
}
#actionButton {
    min-width: 30px;
    min-height: 30px;
    max-width: 30px;
    max-height: 30px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#actionButton:hover {
    color: #ccc;
    background: #1c3561;
}
"""