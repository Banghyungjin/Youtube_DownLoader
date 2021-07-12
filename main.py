"""
made by HyungJin Bang
"""

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtGui import QFontDatabase, QFont
import configparser
from qt_material import apply_stylesheet
import webbrowser
from pytube import YouTube


def open_directory():  # 저장 공간 열기
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini', encoding='utf-8')
    path = config_parser['directory']['directory']
    if not os.path.isdir(path):
        os.mkdir(path)
    os.startfile(config_parser['directory']['directory'])




class YoutubeDownloader(QWidget):

    def config_generator(self):
        # 설정파일 만들기
        config_parser = configparser.ConfigParser()
        self.datetime = QDateTime.currentDateTime()

        # 설정파일 오브젝트 만들기
        config_parser['system'] = {}
        config_parser['system']['title'] = 'YouTube_Downloader'
        config_parser['system']['author'] = 'HyungJin Bang'
        config_parser['system']['version'] = '0.0.1'
        config_parser['system']['update'] = self.datetime.toString('yyyy-MM-dd')
        config_parser['directory'] = {}
        config_parser['directory']['directory'] = 'Videos'

        # 설정파일 저장
        with open('config.ini', 'w', encoding='utf-8') as configfile:  # 동영상 저장 폴더가 없을 경우 만듬
            config_parser.write(configfile)
        configfile.close()
        path = config_parser['directory']['directory']
        if not os.path.isdir(path):
            os.mkdir(path)

    def reset_str(self):  # 저장 공간 리셋
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', 'Videos')
            config_parser.write(configfile)
        configfile.close()
        self.storage_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.storage_label.repaint()

    def select_directory(self):  # 저장 공간 설정
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', QFileDialog.getExistingDirectory(self, "select Directory"))
            config_parser.write(configfile)
        configfile.close()
        self.storage_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.storage_label.repaint()

    def open_browser(self):  # 웹 브라우저 열기
        url = 'https://www.youtube.com/'
        webbrowser.open(url)

    def __init__(self):
        super().__init__()

        self.datetime = QDateTime.currentDateTime()
        self.init_ui()

    def init_ui(self):
        if not os.path.isfile('config.ini'):
            self.config_generator()
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        storage_text = "현재 저장 장소 = " + config_parser['directory']['directory']
        # self.storage_label = QLabel(self.storage_text, self)

        # 버튼 생성
        reset_str_btn = QPushButton('저장 장소 초기화')
        reset_str_btn.setToolTip('저장 장소를 초기화 합니다.')
        reset_str_btn.clicked.connect(self.reset_str)  # 버튼이 클릭되면 해당 함수 실행

        save_btn = QPushButton('저장 장소 설정')
        save_btn.setToolTip('스크린샷이 저장될 위치를 선택합니다.')
        save_btn.clicked.connect(self.select_directory)  # 버튼이 클릭되면 해당 함수 실행

        open_btn = QPushButton('저장 장소 열기')
        open_btn.setToolTip('스크린샷이 저장된 위치를 엽니다.')
        open_btn.clicked.connect(open_directory)  # 버튼이 클릭되면 해당 함수 실행

        browser_btn = QPushButton('웹 브라우저 열기')
        browser_btn.setToolTip('웹 브라우저를 엽니다.')
        browser_btn.clicked.connect(self.open_browser)  # 버튼이 클릭되면 해당 함수 실행

        # 박스 레이아웃 생성
        box_1 = QHBoxLayout()
        box_1.addStretch(1)
        date_label = QLabel('오늘 날짜 : ' + self.datetime.toString('yyyy 년 MM 월 dd 일'))
        date_label.setFont(QFont("", 20))
        box_1.addWidget(date_label)
        box_1.addStretch(1)

        box_2 = QHBoxLayout()
        box_2.addStretch(1)
        directory_label = QLabel(storage_text, self)
        directory_label.setFont(QFont("", 20))
        box_2.addWidget(directory_label)
        box_2.addStretch(1)

        box_3 = QHBoxLayout()
        box_3.addWidget(QLabel("URL을 입력해 주세요."))
        input_url = QLineEdit()
        box_3.addWidget(input_url)

        box_4 = QHBoxLayout()

        box_4.addStretch(1)
        box_4.addStretch(1)

        box_5 = QHBoxLayout()
        box_5.addStretch(1)
        box_5.addWidget(QLabel("사용법 : 저장하고 싶은 YouTube 동영상의 URL을 입력하여 주세요"))
        box_5.addStretch(1)
        # 그리드 레이아웃 생성
        grid = QGridLayout()
        grid.addWidget(save_btn, 0, 0)
        grid.addWidget(open_btn, 0, 1)
        grid.addWidget(reset_str_btn, 0, 2)
        grid.addWidget(browser_btn, 0, 3)

        vbox = QVBoxLayout()
        vbox.addLayout(box_1)
        vbox.addLayout(box_2)
        vbox.addLayout(box_4)
        vbox.addLayout(box_3)
        vbox.addLayout(box_5)
        vbox.addLayout(grid)

        self.setLayout(vbox)
        self.setWindowTitle('YouTube Downloader')  # 프로그램 제목 설정
        self.setGeometry(300, 300, 720, 400)  # 창 위치, 크기 설정 (X위치, Y위치, X크기, Y크기)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_blue.xml')
    ex = YoutubeDownloader()
    sys.exit(app.exec_())
