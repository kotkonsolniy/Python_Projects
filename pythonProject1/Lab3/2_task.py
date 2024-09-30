import sys
import aiohttp
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget


class HtmlFetcher(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Fetcher")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.fetch_button = QPushButton("Fetch HTML", self)
        self.fetch_button.clicked.connect(self.fetch_html)

        layout = QVBoxLayout()
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    async def fetch_google(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://google.com') as resp:
                text = await resp.text()
                return text.splitlines()

    def fetch_html(self):
        self.text_edit.clear()  # Очистить текстовое поле
        loop = asyncio.get_event_loop()
        lines = loop.run_until_complete(self.fetch_google())

        for line in lines:
            self.text_edit.append(line)  # Добавляем строку в текстовое поле


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HtmlFetcher()
    window.show()
    sys.exit(app.exec_())
