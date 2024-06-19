import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QWidget, QCheckBox, QRadioButton, QButtonGroup
from constants import *
from video_processor import VideoProcessor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread = None

    def initUI(self):
        self.setWindowTitle('Customer Counting System')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Input video
        self.video_path_label = QLabel('Input Video Path:')
        layout.addWidget(self.video_path_label)
        self.video_path_input = QLineEdit(self)
        layout.addWidget(self.video_path_input)
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        # Model path
        self.model_path_label = QLabel('YOLO Model Path:')
        layout.addWidget(self.model_path_label)
        self.model_path_input = QLineEdit(self)
        layout.addWidget(self.model_path_input)
        self.model_browse_button = QPushButton('Browse')
        self.model_browse_button.clicked.connect(self.browse_model)
        layout.addWidget(self.model_browse_button)

        # Default model radio button
        self.default_model_radio = QRadioButton('Use Default Model')
        self.default_model_radio.clicked.connect(self.toggle_model_input)
        layout.addWidget(self.default_model_radio)

        # Button group to manage the radio buttons
        self.model_radio_group = QButtonGroup()
        self.model_radio_group.addButton(self.default_model_radio)

        # Threshold
        self.threshold_label = QLabel('Score Threshold:')
        layout.addWidget(self.threshold_label)
        self.threshold_input = QLineEdit(self)
        self.threshold_input.setText('0.7')
        layout.addWidget(self.threshold_input)

        # Classes
        self.classes_label = QLabel('Classes to Track (comma-separated):')
        layout.addWidget(self.classes_label)
        self.classes_input = QLineEdit(self)
        self.classes_input.setText('1')
        layout.addWidget(self.classes_input)

        # Store name
        self.store_name_label = QLabel('Store Name:')
        layout.addWidget(self.store_name_label)
        self.store_name_input = QLineEdit(self)
        layout.addWidget(self.store_name_input)

        # Tracking
        self.tracking_label = QLabel('Enable Tracking:')
        layout.addWidget(self.tracking_label)
        self.tracking_input = QCheckBox(self)
        layout.addWidget(self.tracking_input)

        # Show results
        self.show_label = QLabel('Show Results:')
        layout.addWidget(self.show_label)
        self.show_input = QCheckBox(self)
        layout.addWidget(self.show_input)

        # Run button
        self.run_button = QPushButton('Run')
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)

        # Stop button
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_script)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_model_input(self):
        if self.default_model_radio.isChecked():
            self.model_path_input.setDisabled(True)
            self.model_browse_button.setDisabled(True)
        else:
            self.model_path_input.setDisabled(False)
            self.model_browse_button.setDisabled(False)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Video File')
        if file_path:
            self.video_path_input.setText(file_path)

    def browse_model(self):
        model_path, _ = QFileDialog.getOpenFileName(self, 'Open Model File')
        if model_path:
            self.model_path_input.setText(model_path)

    def run_script(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()

        video_path = self.video_path_input.text()
        imgsz = 640
        if self.default_model_radio.isChecked():
            model_path = DETECTION_MODEL_DIR  # Set your default model path here
        else:
            model_path = self.model_path_input.text()
        threshold = float(self.threshold_input.text())
        classes = [int(cls) for cls in self.classes_input.text().split(',')]
        store_name = self.store_name_input.text()
        tracking = int(self.tracking_input.isChecked())
        show = self.show_input.isChecked()

        self.thread = VideoProcessor(video_path, imgsz, model_path, threshold, classes, store_name, tracking, show)
        self.thread.start()

    def stop_script(self):
        if self.thread:
            self.thread.stop()

    def closeEvent(self, event):
        self.stop_script()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
