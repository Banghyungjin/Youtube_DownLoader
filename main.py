"""
made by HyungJin Bang
"""
import sys
import os.path
from functools import partial
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
import configparser
from qt_material import apply_stylesheet
import webbrowser
import threading
from pytube import YouTube

def open_directory():  # 저장 공간 열기
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini', encoding='utf-8')
    path = config_parser['directory']['directory']
    if not os.path.isdir(path):
        os.mkdir(path)
    os.startfile(config_parser['directory']['directory'])


def open_browser():  # 웹 브라우저 열기
    url = 'https://www.youtube.com/'
    webbrowser.open(url)


class YoutubeDownloader(QWidget, threading.Thread):

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
        self.directory_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.directory_label.repaint()

    def select_directory(self):  # 저장 공간 설정
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', QFileDialog.getExistingDirectory(self, "select Directory"))
            config_parser.write(configfile)
        configfile.close()
        self.directory_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.directory_label.repaint()

    def save_video(self):  # 동영상 저장
        url = self.input_url.text()
        try:
            self.youtube = YouTube(url)
            youtube_streams = self.youtube.streams
            video_vertical = QVBoxLayout()
            video_vertical.addStretch(1)
            video_name = QLabel("비디오 이름")
            video_name.setFont(QFont("궁서", 15))
            video_name.setStyleSheet("Color: #6495ED")
            video_vertical.addWidget(video_name)
            video_vertical.addStretch(1)
            video_title = QLabel(f'- {self.youtube.title}')
            video_title.setFont(QFont("궁서", 15))
            video_title.setStyleSheet("Color: #6495ED")
            video_vertical.addWidget(video_title)
            video_vertical.addStretch(1)
            video_len = QLabel(f'비디오 길이\n - {self.youtube.length // 3600} 시간 {(self.youtube.length % 3600) // 60} 분 {self.youtube.length % 60} 초')
            video_len.setFont(QFont("궁서", 15))
            video_len.setStyleSheet("Color: #6495ED")
            video_vertical.addWidget(video_len)
            video_vertical.addStretch(1)

            for i, stream in enumerate(
                    youtube_streams.filter(progressive=True)):
                # print(i, stream, type(stream), stream.resolution)
                video_horizontal = QHBoxLayout()
                input_save_btn = QPushButton(f'해상도 = {stream.resolution}\tfps = {stream.fps}')
                input_save_btn.clicked.connect(partial(self.save_btn_clicked, youtube_streams, stream.itag))
                video_horizontal.addWidget(input_save_btn)
                video_vertical.addLayout(video_horizontal)
                video_vertical.addStretch(1)
            mp3_btn = QPushButton("mp3 다운로드")
            mp3_btn.clicked.connect(partial(self.mp3_download, youtube_streams))
            video_vertical.addWidget(mp3_btn)
            video_vertical.addStretch(1)
            exit_btn = QPushButton("뒤로가기")
            exit_btn.clicked.connect(self.exit_save)
            video_vertical.addWidget(exit_btn)
            video_vertical.addStretch(1)
            self.save_dialog.setWindowTitle("Available formats")
            self.save_dialog.setWindowModality(Qt.ApplicationModal)
            self.save_dialog.setLayout(video_vertical)
            self.save_dialog.show()
        except:
            print("error")

    def mp3_download(self, input_stream):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        sound_stream = input_stream.get_by_itag(140)
        sound_stream.download(output_path=config_parser['directory']['directory'], filename=f'{self.youtube.title}_sound')
        self.save_dialog.close()
        self.save_dialog.destroy()
        self.save_dialog = QDialog()

    def save_btn_clicked(self, input_stream, itag):
        stream = input_stream.get_by_itag(itag)
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        stream.download(output_path=config_parser['directory']['directory'])
        self.save_dialog.close()
        self.save_dialog.destroy()
        self.save_dialog = QDialog()

    def exit_save(self):
        self.save_dialog.close()
        self.save_dialog.destroy()
        self.save_dialog = QDialog()

    def __init__(self):
        super().__init__()
        self.save_dialog = QDialog()
        self.input_url = QLineEdit(self)
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

        set_save_btn = QPushButton('저장 장소 설정')
        set_save_btn.setToolTip('스크린샷이 저장될 위치를 선택합니다.')
        set_save_btn.clicked.connect(self.select_directory)  # 버튼이 클릭되면 해당 함수 실행

        open_btn = QPushButton('저장 장소 열기')
        open_btn.setToolTip('스크린샷이 저장된 위치를 엽니다.')
        open_btn.clicked.connect(open_directory)  # 버튼이 클릭되면 해당 함수 실행

        browser_btn = QPushButton('YouTube 열기')
        browser_btn.setToolTip('웹 브라우저를 엽니다.')
        browser_btn.clicked.connect(open_browser)  # 버튼이 클릭되면 해당 함수 실행

        save_btn = QPushButton('저장')
        save_btn.setToolTip('해당 동영상을 저장합니다')
        save_btn.clicked.connect(self.save_video)  # 버튼이 클릭되면 해당 함수 실행

        # 라벨 생성
        date_label = QLabel('오늘 날짜 : ' + self.datetime.toString('yyyy 년 MM 월 dd 일'))
        date_label.setFont(QFont("", 20))
        date_label.setStyleSheet("Color: #6495ED")

        manual_label = QLabel("사용법 : 저장하고 싶은 YouTube 동영상의 URL을 입력하여 주세요")
        manual_label.setFont(QFont("", 20))
        manual_label.setStyleSheet("Color: #6495ED")

        self.directory_label = QLabel(storage_text, self)
        self.directory_label.setFont(QFont("", 20))
        self.directory_label.setStyleSheet("Color: #6495ED")

        # 박스 레이아웃 생성
        box_1 = QHBoxLayout()
        box_1.addStretch(1)
        box_1.addWidget(date_label)
        box_1.addStretch(1)

        box_2 = QHBoxLayout()
        box_2.addStretch(1)
        box_2.addWidget(self.directory_label)
        box_2.addStretch(1)

        box_3 = QHBoxLayout()
        box_3.addStretch(1)
        box_3.addWidget(manual_label)
        box_3.addStretch(1)

        box_4 = QHBoxLayout()
        box_4.addWidget(QLabel("URL"))
        box_4.addWidget(self.input_url)
        # box_4.addWidget(save_btn)

        box_5 = QHBoxLayout()
        box_5.addWidget(save_btn)

        # 그리드 레이아웃 생성
        grid = QGridLayout()
        grid.addWidget(set_save_btn, 0, 0)
        grid.addWidget(open_btn, 0, 1)
        grid.addWidget(reset_str_btn, 0, 2)
        grid.addWidget(browser_btn, 0, 3)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(box_1)
        vbox.addStretch()
        vbox.addLayout(box_2)
        vbox.addStretch()
        vbox.addLayout(box_3)
        vbox.addStretch()
        vbox.addLayout(box_4)
        vbox.addLayout(box_5)
        vbox.addStretch()
        vbox.addLayout(grid)
        vbox.addStretch()

        self.setLayout(vbox)
        self.setWindowTitle('YouTube Downloader')  # 프로그램 제목 설정
        self.setGeometry(300, 300, 720, 400)  # 창 위치, 크기 설정 (X위치, Y위치, X크기, Y크기)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_blue.xml')
    ex = YoutubeDownloader()
    sys.exit(app.exec_())
