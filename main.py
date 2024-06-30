import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QToolBar,
    QFileDialog, QFontDialog, QColorDialog, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
)
from PyQt5.QtGui import QTextCharFormat, QFont, QTextCursor, QColor
from PyQt5.QtCore import pyqtSignal, QObject


# Паттерн Command
class Command:
    """Абстрактный базовый класс для команд."""

    def execute(self) -> None:
        """Метод для выполнения команды. Должен быть переопределен в подклассах."""
        pass


class TextEditCommand(Command):
    """Команда для установки текста в QTextEdit."""

    def __init__(self, text_edit: QTextEdit, text: str) -> None:
        """
        Инициализация команды.

        :param text_edit: QTextEdit, в котором нужно установить текст.
        :param text: Текст, который нужно установить.
        """
        self.text_edit = text_edit
        self.text = text

    def execute(self) -> None:
        """Устанавливает текст в QTextEdit."""
        self.text_edit.setPlainText(self.text)


class FontCommand(Command):
    """Команда для установки шрифта в QTextEdit."""

    def __init__(self, text_edit: QTextEdit, font: QFont) -> None:
        """
        Инициализация команды.

        :param text_edit: QTextEdit, в котором нужно установить шрифт.
        :param font: QFont, который нужно установить.
        """
        self.text_edit = text_edit
        self.font = font

    def execute(self) -> None:
        """Устанавливает шрифт для выделенного текста в QTextEdit."""
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            format = cursor.charFormat()
            format.setFont(self.font)
            cursor.setCharFormat(format)
        else:
            self.text_edit.setFont(self.font)


class ColorCommand(Command):
    """Команда для установки цвета текста в QTextEdit."""

    def __init__(self, text_edit: QTextEdit, color: QColor) -> None:
        """
        Инициализация команды.

        :param text_edit: QTextEdit, в котором нужно установить цвет текста.
        :param color: QColor, который нужно установить.
        """
        self.text_edit = text_edit
        self.color = color

    def execute(self) -> None:
        """Устанавливает цвет для выделенного текста в QTextEdit."""
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            format = cursor.charFormat()
            format.setForeground(self.color)
            cursor.setCharFormat(format)
        else:
            self.text_edit.setTextColor(self.color)


# Паттерн Observer
class Observer:
    """Абстрактный базовый класс для наблюдателей."""

    def update(self, state: str) -> None:
        """
        Метод для обновления состояния наблюдателя. Должен быть переопределен в подклассах.

        :param state: Новое состояние для наблюдателя.
        """
        pass


class Document(QObject):
    """Документ, который уведомляет наблюдателей о изменении текста."""

    text_changed = pyqtSignal(str)

    def __init__(self) -> None:
        """Инициализация документа."""
        super().__init__()
        self._text = ""

    def set_text(self, text: str) -> None:
        """
        Устанавливает текст и уведомляет наблюдателей.

        :param text: Текст для установки.
        """
        self._text = text
        self.text_changed.emit(self._text)

    def get_text(self) -> str:
        """
        Возвращает текущий текст.

        :return: Текущий текст документа.
        """
        return self._text


# Паттерн Bridge
class WidgetImplementation:
    """Абстрактный базовый класс для реализации виджетов."""

    def draw(self) -> None:
        """Метод для отрисовки виджета. Должен быть переопределен в подклассах."""
        pass


class TextEditImplementation(WidgetImplementation):
    """Реализация TextEdit виджета."""

    def __init__(self, text_edit: QTextEdit) -> None:
        """
        Инициализация реализации.

        :param text_edit: QTextEdit для реализации.
        """
        self.text_edit = text_edit

    def draw(self) -> None:
        """Отрисовывает текстовое поле."""
        self.text_edit.setPlainText("TextEdit Implementation")


class LabelImplementation(WidgetImplementation):
    """Реализация Label виджета."""

    def __init__(self, label: QLabel) -> None:
        """
        Инициализация реализации.

        :param label: QLabel для реализации.
        """
        self.label = label

    def draw(self) -> None:
        """Отрисовывает метку."""
        self.label.setText("Label Implementation")


class AbstractWidget:
    """Абстрактный виджет, который использует реализацию."""

    def __init__(self, implementation: WidgetImplementation) -> None:
        """
        Инициализация виджета.

        :param implementation: Реализация виджета.
        """
        self.implementation = implementation

    def draw(self) -> None:
        """Вызывает метод отрисовки реализации."""
        self.implementation.draw()


# Паттерн Strategy
class TextFormatter:
    """Абстрактный базовый класс для форматирования текста."""

    def format(self, text: str) -> str:
        """
        Метод для форматирования текста. Должен быть переопределен в подклассах.

        :param text: Текст для форматирования.
        :return: Форматированный текст.
        """
        pass


class UpperCaseFormatter(TextFormatter):
    """Форматирует текст в верхний регистр."""

    def format(self, text: str) -> str:
        """
        Форматирует текст в верхний регистр.

        :param text: Текст для форматирования.
        :return: Текст в верхнем регистре.
        """
        return text.upper()


class LowerCaseFormatter(TextFormatter):
    """Форматирует текст в нижний регистр."""

    def format(self, text: str) -> str:
        """
        Форматирует текст в нижний регистр.

        :param text: Текст для форматирования.
        :return: Текст в нижнем регистре.
        """
        return text.lower()


class TextEditor:
    """Текстовый редактор с поддержкой стратегии форматирования текста."""

    def __init__(self, formatter: TextFormatter) -> None:
        """
        Инициализация текстового редактора.

        :param formatter: Стратегия форматирования текста.
        """
        self.formatter = formatter

    def set_formatter(self, formatter: TextFormatter) -> None:
        """
        Устанавливает стратегию форматирования.

        :param formatter: Новая стратегия форматирования текста.
        """
        self.formatter = formatter

    def format_text(self, text: str) -> str:
        """
        Форматирует текст согласно текущей стратегии.

        :param text: Текст для форматирования.
        :return: Форматированный текст.
        """
        return self.formatter.format(text)


# Паттерн Factory Method
class DialogFactory:
    """Абстрактный базовый класс для фабрики диалогов."""

    def create_dialog(self):
        """Метод для создания диалога. Должен быть переопределен в подклассах."""
        pass


class OpenFileDialogFactory(DialogFactory):
    """Фабрика диалогов открытия файлов."""

    def create_dialog(self) -> tuple[str, str]:
        """
        Создает диалог открытия файла.

        :return: Кортеж с путем к файлу и фильтром файлов.
        """
        return QFileDialog.getOpenFileName()


class SaveFileDialogFactory(DialogFactory):
    """Фабрика диалогов сохранения файлов."""

    def create_dialog(self) -> tuple[str, str]:
        """
        Создает диалог сохранения файла.

        :return: Кортеж с путем к файлу и фильтром файлов.
        """
        return QFileDialog.getSaveFileName()


# Диалоги поиска и замены
class FindDialog(QDialog):
    """Диалог поиска текста."""

    def __init__(self, parent=None) -> None:
        """
        Инициализация диалога поиска.

        :param parent: Родительский виджет, по умолчанию None.
        """
        super().__init__(parent)
        self.setWindowTitle("Find")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Find:", self)
        self.layout.addWidget(self.label)

        self.find_input = QLineEdit(self)
        self.layout.addWidget(self.find_input)

        self.find_button = QPushButton("Find", self)
        self.layout.addWidget(self.find_button)
        self.find_button.clicked.connect(self.find_text)

        self.text_edit = parent.text_edit

        # Настройка шрифтов и стилей для диалога поиска
        self.setFont(QFont("Arial", 24))
        self.find_button.setStyleSheet("QPushButton {font-size: 24px;}")
        self.find_input.setStyleSheet("QLineEdit {font-size: 24px;}")

    def find_text(self) -> None:
        """Ищет текст, введенный в поле ввода."""
        text_to_find = self.find_input.text()
        if text_to_find:
            cursor = self.text_edit.textCursor()
            document = self.text_edit.document()

            found = False
            while not cursor.isNull() and not cursor.atEnd():
                cursor = document.find(text_to_find, cursor)
                if not cursor.isNull():
                    self.text_edit.setTextCursor(cursor)
                    found = True
                    break
            if not found:
                cursor.movePosition(QTextCursor.Start)
                self.text_edit.setTextCursor(cursor)


class ReplaceDialog(QDialog):
    """Диалог замены текста."""

    def __init__(self, parent=None) -> None:
        """
        Инициализация диалога замены.

        :param parent: Родительский виджет, по умолчанию None.
        """
        super().__init__(parent)
        self.setWindowTitle("Replace")
        self.layout = QVBoxLayout(self)

        self.label_find = QLabel("Find:", self)
        self.layout.addWidget(self.label_find)

        self.find_input = QLineEdit(self)
        self.layout.addWidget(self.find_input)

        self.label_replace = QLabel("Replace with:", self)
        self.layout.addWidget(self.label_replace)

        self.replace_input = QLineEdit(self)
        self.layout.addWidget(self.replace_input)

        self.replace_button = QPushButton("Replace", self)
        self.layout.addWidget(self.replace_button)
        self.replace_button.clicked.connect(self.replace_text)

        self.replace_all_button = QPushButton("Replace All", self)
        self.layout.addWidget(self.replace_all_button)
        self.replace_all_button.clicked.connect(self.replace_all_text)

        self.text_edit = parent.text_edit

        # Настройка шрифтов и стилей для диалога замены
        self.setFont(QFont("Arial", 24))
        self.replace_button.setStyleSheet("QPushButton {font-size: 24px;}")
        self.replace_all_button.setStyleSheet("QPushButton {font-size: 24px;}")
        self.find_input.setStyleSheet("QLineEdit {font-size: 24px;}")
        self.replace_input.setStyleSheet("QLineEdit {font-size: 24px;}")

    def replace_text(self) -> None:
        """Заменяет первое вхождение текста."""
        text_to_find = self.find_input.text()
        text_to_replace = self.replace_input.text()
        if text_to_find:
            cursor = self.text_edit.textCursor()
            document = self.text_edit.document()

            found = document.find(text_to_find, cursor)
            if found.isNull():
                cursor.movePosition(QTextCursor.Start)
                found = document.find(text_to_find, cursor)

            if not found.isNull():
                cursor = self.text_edit.textCursor()
                cursor.setPosition(found.selectionStart())
                cursor.setPosition(found.selectionEnd(), QTextCursor.KeepAnchor)
                cursor.insertText(text_to_replace)
                self.text_edit.setTextCursor(cursor)

    def replace_all_text(self) -> None:
        """Заменяет все вхождения текста."""
        text_to_find = self.find_input.text()
        text_to_replace = self.replace_input.text()
        if text_to_find:
            cursor = self.text_edit.textCursor()
            document = self.text_edit.document()

            cursor.beginEditBlock()
            pos = 0
            while True:
                found = document.find(text_to_find, pos)
                if found.isNull():
                    break
                pos = found.selectionStart() + len(text_to_replace)
                cursor.setPosition(found.selectionStart())
                cursor.setPosition(found.selectionEnd(), QTextCursor.KeepAnchor)
                cursor.insertText(text_to_replace)
            cursor.endEditBlock()


# Основное приложение
class MainWindow(QMainWindow):
    """Главное окно приложения."""

    def __init__(self) -> None:
        """Инициализация главного окна."""
        super().__init__()

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 24))
        self.setCentralWidget(self.text_edit)

        self.document = Document()
        self.document.text_changed.connect(self.on_text_changed)

        self.init_ui()

    def init_ui(self) -> None:
        """Инициализация пользовательского интерфейса."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Создание действий для тулбара
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        font_action = QAction("Choose Font", self)
        font_action.triggered.connect(self.choose_font)
        toolbar.addAction(font_action)

        color_action = QAction("Choose Color", self)
        color_action.triggered.connect(self.choose_color)
        toolbar.addAction(color_action)

        find_action = QAction("Find", self)
        find_action.triggered.connect(self.find_text)
        toolbar.addAction(find_action)

        replace_action = QAction("Replace", self)
        replace_action.triggered.connect(self.replace_text)
        toolbar.addAction(replace_action)

        # Увеличение размера шрифта кнопок тулбара
        toolbar.setStyleSheet("QToolBar {font-size: 24px;}")

    def execute_command(self, command: Command) -> None:
        """
        Выполняет переданную команду.

        :param command: Команда для выполнения.
        """
        command.execute()

    def on_text_changed(self, text: str) -> None:
        """
        Обработчик изменения текста документа.

        :param text: Новый текст документа.
        """
        self.statusBar().showMessage("Document modified")

    def open_file(self) -> None:
        """Открывает файл и загружает его содержимое в QTextEdit."""
        open_dialog = OpenFileDialogFactory().create_dialog()
        file_path, _ = open_dialog
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.execute_command(TextEditCommand(self.text_edit, text))
                self.document.set_text(text)

    def save_file(self) -> None:
        """Сохраняет текущее содержимое QTextEdit в файл."""
        save_dialog = SaveFileDialogFactory().create_dialog()
        file_path, _ = save_dialog
        if file_path:
            with open(file_path, 'w') as file:
                text = self.text_edit.toPlainText()
                file.write(text)
                self.document.set_text(text)
                self.statusBar().showMessage("File saved")

    def choose_font(self) -> None:
        """Открывает диалог выбора шрифта и применяет выбранный шрифт к выделенному тексту."""
        font, ok = QFontDialog.getFont()
        if ok:
            self.execute_command(FontCommand(self.text_edit, font))

    def choose_color(self) -> None:
        """Открывает диалог выбора цвета и применяет выбранный цвет к выделенному тексту."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.execute_command(ColorCommand(self.text_edit, color))

    def find_text(self) -> None:
        """Открывает диалог поиска текста."""
        find_dialog = FindDialog(self)
        find_dialog.exec_()

    def replace_text(self) -> None:
        """Открывает диалог замены текста."""
        replace_dialog = ReplaceDialog(self)
        replace_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 19))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



