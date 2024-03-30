import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QRect
import threading
# import force_test

class UpdateSignal(QObject):
    update = pyqtSignal(int, int, int, int)

class PressureDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.left_f = 0
        self.left_b = 0
        self.right_f = 0
        self.right_b = 0

        # 초기 투명도 값 설정
        self.left_f_alpha = 0
        self.left_b_alpha = 0
        self.right_f_alpha = 0
        self.right_b_alpha = 0
        
        self.initUI()
        
        self.update_signal = UpdateSignal()
        self.update_signal.update.connect(self.update_values)

    def initUI(self):
        self.setGeometry(300, 300, 720, 640)  # 창 크기 2배로 조정
        self.setWindowTitle('force UI')

        # 배경색을 흰색으로 설정
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)
        self.show()

    def update_values(self, left_f, left_b, right_f, right_b):
        self.left_f = left_f
        self.left_b = left_b
        self.right_f = right_f
        self.right_b = right_b
        # 알파 값으로 투명도 업데이트
        self.left_f_alpha = left_f
        self.left_b_alpha = left_b
        self.right_f_alpha = right_f
        self.right_b_alpha = right_b
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 10, Qt.SolidLine))
        
        # 각 원의 색상 설정
        self.circle_color_left_f = QColor(255, 0, 0, self.left_f_alpha)
        self.circle_color_left_b = QColor(255, 0, 0, self.left_b_alpha)
        self.circle_color_right_f = QColor(255, 0, 0, self.right_f_alpha)
        self.circle_color_right_b = QColor(255, 0, 0, self.right_b_alpha)

        # 원의 크기와 위치 조정
        painter.setBrush(QBrush(self.circle_color_left_f))
        painter.drawEllipse(60, 60, 200, 200)  # 왼쪽 앞 원
        
        painter.setBrush(QBrush(self.circle_color_left_b))
        painter.drawEllipse(60, 320, 200, 200)  # 왼쪽 뒤 원
        
        painter.setBrush(QBrush(self.circle_color_right_f))
        painter.drawEllipse(460, 60, 200, 200)  # 오른쪽 앞 원
        
        painter.setBrush(QBrush(self.circle_color_right_b))
        painter.drawEllipse(460, 320, 200, 200)  # 오른쪽 뒤 원

        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setFont(QFont('Comic Sans MS', 20))  # 폰트 크기 조정
        
        # 텍스트 그리기 위치 조정
        painter.drawText(QRect(60, 60, 200, 200), Qt.AlignCenter, f'{self.left_f}N')
        painter.drawText(QRect(60, 320, 200, 200), Qt.AlignCenter, f'{self.left_b}N')
        painter.drawText(QRect(460, 60, 200, 200), Qt.AlignCenter, f'{self.right_f}N')
        painter.drawText(QRect(460, 320, 200, 200), Qt.AlignCenter, f'{self.right_b}N')
        painter.drawText(QRect(60, 540, 200, 60), Qt.AlignCenter, 'LEFT')
        painter.drawText(QRect(460, 540, 200, 60), Qt.AlignCenter, 'RIGHT')
        painter.drawText(QRect(280, 120, 160, 60), Qt.AlignCenter, 'FRONT')
        painter.drawText(QRect(280, 400, 160, 60), Qt.AlignCenter, 'BACK')

def read_input(update_signal):
    while True:
        try:
            print("투명도 값을 입력하세요 (왼쪽 앞, 왼쪽 뒤, 오른쪽 앞, 오른쪽 뒤): ")
            values = input()
            left_f, left_b, right_f, right_b = map(int, values.split())
            update_signal.update.emit(left_f, left_b, right_f, right_b)
        except ValueError:
            print("올바른 값을 입력하세요!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PressureDisplay()
    input_thread = threading.Thread(target=read_input, args=(ex.update_signal,), daemon=True)
    input_thread.start()
    sys.exit(app.exec_())
