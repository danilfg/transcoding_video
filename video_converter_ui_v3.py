import sys
import os
import json
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
                             QLabel, QComboBox, QLineEdit, QMessageBox, QProgressBar, QTextEdit)
from PyQt6.QtCore import QThread, pyqtSignal

class ConversionThread(QThread):
    progress = pyqtSignal(int)
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, folder, output_format, size):
        super().__init__()
        self.folder = folder
        self.output_format = output_format
        self.size = size
        self.is_running = True

    def run(self):
        video_files = [f for f in os.listdir(self.folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv'))]
        total_files = len(video_files)
        self.progress.emit(0)

        # ffmpeg_path = os.path.join(os.path.dirname(sys.argv[0]), 'bin', 'ffmpeg', '7.1_4', 'bin', 'ffmpeg')
        if getattr(sys, 'frozen', False):
            # Путь для PyInstaller
            base_path = sys._MEIPASS
        else:
            # Путь для разработки
            base_path = os.path.dirname(os.path.abspath(__file__))

        ffmpeg_path = os.path.join(base_path, 'bin', 'ffmpeg', '7.1_4', 'bin', 'ffmpeg')

        for index, file in enumerate(video_files):
            if not self.is_running:
                break

            input_path = os.path.join(self.folder, file)
            output_path = os.path.join(self.folder, f'converted_{os.path.splitext(file)[0]}.{self.output_format}')

            if not os.path.exists(input_path):
                self.log_signal.emit(f'Файл не найден: {file}. Пропускаем...')
                continue

            command = [ffmpeg_path, '-i', input_path]

            if self.output_format == 'mp3':
                command += ['-vn', '-c:a', 'mp3']
            else:
                command += ['-c:v', 'libx264', '-c:a', 'aac']

            if self.size > 0:
                command += ['-fs', f'{self.size}M']

            command.append(output_path)
            self.log_signal.emit(f'Выполняем команду: {" ".join(command)}')

            process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if process.returncode != 0:
                self.log_signal.emit(f'Ошибка при конвертации файла {file}: {process.stderr.decode()}')

            self.progress.emit(int((index + 1) / total_files * 100))

        self.finished_signal.emit()

    def stop(self):
        self.is_running = False

class VideoConverter(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.thread = None

    def initUI(self):
        self.setWindowTitle('Видео Конвертер')
        self.setGeometry(200, 200, 400, 500)

        layout = QVBoxLayout()

        self.label = QLabel('Выберите папку с видео:', self)
        layout.addWidget(self.label)

        self.btn_select_folder = QPushButton('Выбрать папку', self)
        self.btn_select_folder.clicked.connect(self.select_folder)
        layout.addWidget(self.btn_select_folder)

        self.format_label = QLabel('Формат вывода:', self)
        layout.addWidget(self.format_label)

        self.format_combo = QComboBox(self)
        self.format_combo.addItems(['mp4', 'mp3'])
        self.format_combo.currentIndexChanged.connect(self.update_codecs)
        layout.addWidget(self.format_combo)

        self.size_label = QLabel('Конечный размер файла (MB, 0 = не изменять):', self)
        layout.addWidget(self.size_label)

        self.size_input = QLineEdit(self)
        self.size_input.setText('0')
        layout.addWidget(self.size_input)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.btn_convert = QPushButton('Конвертировать', self)
        self.btn_convert.clicked.connect(self.convert_videos)
        layout.addWidget(self.btn_convert)

        self.btn_stop = QPushButton('Завершить текущие операции', self)
        self.btn_stop.clicked.connect(self.stop_conversion)
        self.btn_stop.setEnabled(False)
        layout.addWidget(self.btn_stop)

        self.setLayout(layout)



    def update_codecs(self):
        output_format = self.format_combo.currentText()

    def log(self, message):
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        if folder:
            self.label.setText(f'Выбрана папка: {folder}')
            self.folder = folder


    def convert_videos(self):
        if not hasattr(self, 'folder'):
            QMessageBox.warning(self, 'Ошибка', 'Выберите папку с видео!')
            return

        output_format = self.format_combo.currentText()
        size = int(self.size_input.text())

        self.progress_bar.setValue(0)
        self.thread = ConversionThread(self.folder, output_format, size)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.log_signal.connect(self.log)
        self.thread.finished_signal.connect(self.conversion_finished)
        self.thread.start()

        self.update_buttons_state(False)

    def stop_conversion(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.log('Конвертация остановлена!')
            self.update_buttons_state(True)

    def conversion_finished(self):
        self.update_buttons_state(True)
        QMessageBox.information(self, 'Готово', 'Конвертация завершена!')

    def update_buttons_state(self, enable):
        self.btn_select_folder.setEnabled(enable)
        self.btn_convert.setEnabled(enable)
        self.btn_stop.setEnabled(not enable)
        self.format_combo.setEnabled(enable)
        self.size_input.setEnabled(enable)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoConverter()
    ex.show()
    sys.exit(app.exec())
