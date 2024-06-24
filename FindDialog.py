from ToolBar import  *

class FindDialog(QDialog):
    """
    Класс для создания диалога поиска текста.

    Методы:
    - __init__(parent=None) -> None: Инициализирует диалог с полем ввода и кнопкой "Далее".
    - find_next() -> None: Ищет следующий вхождение текста в QTextEdit.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск текста")
        self.setGeometry(300, 300, 300, 100)
        self.parent = parent
        self.layout = QVBoxLayout()

        self.label = QLabel("Найти:")
        self.layout.addWidget(self.label)

        self.search_input = QLineEdit()
        self.layout.addWidget(self.search_input)

        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.find_next)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

    def find_next(self):
        """
        Ищет следующее вхождение текста в QTextEdit.
        """
        search_text = self.search_input.text()
        if search_text:
            text_edit = self.parent.text_edit
            cursor = text_edit.textCursor()
            cursor = text_edit.document().find(search_text, cursor)

            if cursor.isNull():
                cursor.setPosition(0)
                cursor = text_edit.document().find(search_text, cursor)

            if not cursor.isNull():
                text_edit.setTextCursor(cursor)
