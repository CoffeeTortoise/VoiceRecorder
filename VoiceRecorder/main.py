from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QSlider, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from pyaudio import PyAudio
import sys
from config import WND_WIDTH, WND_HEIGHT, SIZE, FNT_SIZE, BORDER_W, FONT, ICON, TITLE
from recorder import SoundRecorder
from settings import OUT_FORMATS


class TurtleApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.layout: QGridLayout = QGridLayout()
        self.recorder: SoundRecorder = SoundRecorder()
        
        # Style
        self.font: QFont = QFont(FONT, FNT_SIZE)
        self.border: str = f'border: {BORDER_W}px solid black;'
        self.height: int = SIZE * 2
        
        # Gui
        self.wnd: QWidget = QWidget(self)
        self.lbl_duration: QLabel = QLabel(self.wnd)
        self.sld_duration: QSlider = QSlider(self.wnd)
        self.lbl_time: QLabel = QLabel(self.wnd)
        self.lbl_file: QLabel = QLabel(self.wnd)
        self.inp_line: QLineEdit = QLineEdit(self.wnd)
        self.frmt_box: QComboBox = QComboBox(self.wnd)
        self.btn_confirm: QPushButton = QPushButton(self.wnd)
        self.btn_start: QPushButton = QPushButton(self.wnd)
        self.btn_quit: QPushButton = QPushButton(self.wnd)
        
        self.init_gui()
     
    def start_record(self) -> None:
        record: PyAudio = self.recorder.record()
        self.recorder.save(record)
    
    def confirm(self) -> None:
        forbidden_simbs: str = ' \n,.-!@#$%^&*()+=-*/<>?|\\~`   '
        self.recorder.time_lim = self.sld_duration.value()
        self.recorder.out = self.frmt_box.currentIndex()
        txt: str = self.inp_line.text()
        if txt.startswith('_'):
            correct: str = txt.replace('_', 'T')
            txt = correct
        for symb in forbidden_simbs:
            new_txt: str = txt.replace(symb, '')
            txt = new_txt
        filename: str = txt if txt else self.recorder.filename
        self.recorder.filename = filename
    
    def quit(self) -> None:
        self.wnd.destroy()
        self.destroy()
        QApplication.quit()
    
    def init_gui(self) -> None:
        self.init_main_wnd()
        self.init_wnd()
        self.init_lbl_duration()
        self.init_sld_duration()
        self.init_lbl_time()
        self.init_lbl_file()
        self.init_inp_line()
        self.init_frmt_box()
        self.init_btn_confirm()
        self.init_btn_start()
        self.init_btn_quit()
    
    
    def init_main_wnd(self) -> None:
        icon: QIcon = QIcon(ICON)
        self.setFixedSize(WND_WIDTH, WND_HEIGHT)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(icon)
    
    def init_wnd(self) -> None:
        self.wnd.setFixedSize(WND_WIDTH, WND_HEIGHT)
        self.wnd.move(0, 0)
        self.wnd.setLayout(self.layout)
    
    def init_lbl_duration(self) -> None:
        lbl_txt: str = 'Duration'
        lbl_size: tuple[int, int] = SIZE * 4, self.height
        self.lbl_duration.setText(lbl_txt)
        self.lbl_duration.setFont(self.font)
        self.lbl_duration.setFixedSize(lbl_size[0], lbl_size[1])
        self.lbl_duration.setStyleSheet(self.border)
        self.layout.addWidget(self.lbl_duration, 0, 0)
    
    def init_sld_duration(self) -> None:
        orient: int = 1
        rang: tuple[int, int] = 1, 360
        size: tuple[int, int] = SIZE * 16, self.height
        self.sld_duration.setMinimum(rang[0])
        self.sld_duration.setMaximum(rang[1])
        self.sld_duration.setOrientation(orient)
        self.sld_duration.setFixedSize(size[0], size[1])
        self.sld_duration.valueChanged.connect(self.change_time_value)
        self.layout.addWidget(self.sld_duration, 0, 1)
    
    def init_lbl_time(self) -> None:
        txt: str = str(self.recorder.time_lim)
        size: tuple[int, int] = SIZE * 3, self.height
        self.lbl_time.setText(txt)
        self.lbl_time.setFont(self.font)
        self.lbl_time.setStyleSheet(self.border)
        self.lbl_time.setFixedSize(size[0], size[1])
        self.layout.addWidget(self.lbl_time, 0, 3)
    
    def change_time_value(self) -> None:
        value: int = self.sld_duration.value()
        self.lbl_time.setText(str(value))
    
    def init_lbl_file(self) -> None:
        lbl_text: str = 'Filename'
        lbl_size: tuple[int, int] = SIZE * 4, self.height
        self.lbl_file.setText(lbl_text)
        self.lbl_file.setFont(self.font)
        self.lbl_file.setStyleSheet(self.border)
        self.lbl_file.setFixedSize(lbl_size[0], lbl_size[1])
        self.layout.addWidget(self.lbl_file, 1, 0)
    
    def init_inp_line(self) -> None:
        inp_size: tuple[int, int] = SIZE * 12, self.height
        self.inp_line.setText(self.recorder.filename)
        self.inp_line.setFont(self.font)
        self.inp_line.setFixedSize(inp_size[0], inp_size[1])
        self.layout.addWidget(self.inp_line, 1, 1)
    
    def init_frmt_box(self) -> None:
        size: tuple[int, int] = SIZE * 3, self.height
        self.frmt_box.addItems(OUT_FORMATS)
        self.frmt_box.setFont(self.font)
        self.frmt_box.setFixedSize(size[0], size[1])
        self.layout.addWidget(self.frmt_box, 1, 2)
    
    def init_btn_confirm(self) -> None:
        btn_txt: str = 'Confirm'
        btn_size: tuple[int, int] = SIZE * 4, self.height
        self.btn_confirm.setText(btn_txt)
        self.btn_confirm.setFont(self.font)
        self.btn_confirm.clicked.connect(self.confirm)
        self.btn_confirm.setFixedSize(btn_size[0], btn_size[1])
        self.layout.addWidget(self.btn_confirm, 1, 3)
    
    def init_btn_start(self) -> None:
        btn_txt: str = 'Start'
        btn_size: tuple[int, int] = SIZE * 4, self.height
        self.btn_start.setText(btn_txt)
        self.btn_start.setFont(self.font)
        self.btn_start.clicked.connect(self.start_record)
        self.btn_start.setFixedSize(btn_size[0], btn_size[1])
        self.layout.addWidget(self.btn_start, 2, 0)
    
    def init_btn_quit(self) -> None:
        btn_txt: str = 'Quit'
        btn_size: tuple[int, int] = SIZE * 3, self.height
        self.btn_quit.setText(btn_txt)
        self.btn_quit.setFont(self.font)
        self.btn_quit.clicked.connect(self.quit)
        self.btn_quit.setFixedSize(btn_size[0], btn_size[1])
        self.layout.addWidget(self.btn_quit, 2, 3)


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    turtle: TurtleApp = TurtleApp()
    turtle.show()
    sys.exit(app.exec_())
