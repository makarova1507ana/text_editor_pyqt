from FindDialog import  *

class TextOperations:
    """
    Класс для работы с текстом в QTextEdit.

    Методы:
    - __init__(main_window: QMainWindow) -> None: Инициализирует класс с указанным QMainWindow.
    - find_text() -> None: Открывает диалог поиска текста в QTextEdit.
    - replace_text() -> None: Открывает диалог замены текста в QTextEdit.
    """
    def __init__(self, main_window: QMainWindow) -> None:
        """
        Инициализирует класс с указанным QMainWindow.

        Args:
        - main_window (QMainWindow): Экземпляр главного окна для работы с текстом.
        """
        self.main_window = main_window

    def find_text(self) -> None:
        """
        Открывает диалог поиска текста в QTextEdit.
        """
        self.find_dialog = FindDialog(self.main_window)
        self.find_dialog.show()

    def replace_text(self) -> None:
        """
        Открывает диалог замены текста в QTextEdit.
        """
        find_text, ok1 = QInputDialog.getText(self.main_window, "Замена текста", "Найти:")
        if ok1:
            replace_text, ok2 = QInputDialog.getText(self.main_window, "Замена текста", "Заменить на:")
            if ok2:
                cursor = self.main_window.text_edit.textCursor()
                cursor.beginEditBlock()

                doc = self.main_window.text_edit.document()
                pos = 0
                while True:
                    cursor = doc.find(find_text, pos)
                    if cursor.isNull():
                        break
                    cursor.insertText(replace_text)
                    pos = cursor.position()

                cursor.endEditBlock()
