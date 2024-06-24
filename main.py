
from TextOperations import *
class MainWindow(QMainWindow):
    """
    Главное окно текстового редактора.

    Методы:
    - __init__() -> None: Инициализирует главное окно с заголовком и размерами, вызывает init_ui() для настройки пользовательского интерфейса.
    - init_ui() -> None: Настраивает пользовательский интерфейс с QTextEdit в качестве центрального виджета, создает меню и панель инструментов.
    - format_bold() -> None: Включает или выключает жирное начертание для выделенного текста в QTextEdit.
    - format_italic() -> None: Включает или выключает курсивное начертание для выделенного текста в QTextEdit.
    - format_underline() -> None: Включает или выключает подчеркивание для выделенного текста в QTextEdit.
    - change_font(font) -> None: Изменяет шрифт для выделенного текста в QTextEdit.
    - change_font_size(size) -> None: Изменяет размер шрифта для выделенного текста в QTextEdit.
    - change_color() -> None: Открывает диалог выбора цвета для изменения цвета выделенного текста в QTextEdit.
    """
    def __init__(self):
        """
        Инициализирует главное окно с заголовком и размерами, вызывает init_ui() для настройки пользовательского интерфейса.
        """
        super().__init__()
        self.setWindowTitle("Текстовый редактор")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        """
        Настраивает пользовательский интерфейс с QTextEdit в качестве центрального виджета, создает меню и панель инструментов.
        """
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.tool_bar = ToolBar(self)
        self.text_operations = TextOperations(self)

        self.create_menu()

    def create_menu(self):
        """
        Создает меню приложения.
        """
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")
        edit_menu = menu_bar.addMenu("Правка")
        format_menu = menu_bar.addMenu("Формат")

        open_action = self.create_action("Открыть", self.open_file)
        save_action = self.create_action("Сохранить", self.save_file)
        exit_action = self.create_action("Выход", self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        undo_action = self.create_action("Отменить", self.text_edit.undo)
        redo_action = self.create_action("Повторить", self.text_edit.redo)
        cut_action = self.create_action("Вырезать", self.text_edit.cut)
        copy_action = self.create_action("Копировать", self.text_edit.copy)
        paste_action = self.create_action("Вставить", self.text_edit.paste)
        find_action = self.create_action("Найти", self.text_operations.find_text)
        replace_action = self.create_action("Заменить", self.text_operations.replace_text)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(find_action)
        edit_menu.addAction(replace_action)

        bold_action = self.create_action("Жирный", self.format_bold)
        italic_action = self.create_action("Курсив", self.format_italic)
        underline_action = self.create_action("Подчеркнутый", self.format_underline)

        format_menu.addAction(bold_action)
        format_menu.addAction(italic_action)
        format_menu.addAction(underline_action)

    def create_action(self, name: str, method: callable) -> QAction:
        """
        Создает действие (QAction) для указанного метода.

        Args:
        - name (str): Название действия.
        - method (callable): Функция или метод, которая будет вызываться при активации действия.

        Returns:
        - QAction: Созданное действие.
        """
        action = QAction(name, self)
        action.triggered.connect(method)
        return action

    def format_bold(self) -> None:
        """
        Включает или выключает жирное начертание для выделенного текста в QTextEdit.
        """
        fmt = self.text_edit.currentCharFormat()
        if fmt.fontWeight() == QFont.Bold:
            fmt.setFontWeight(QFont.Normal)
        else:
            fmt.setFontWeight(QFont.Bold)
        self.text_edit.setCurrentCharFormat(fmt)

    def format_italic(self) -> None:
        """
        Включает или выключает курсивное начертание для выделенного текста в QTextEdit.
        """
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.text_edit.setCurrentCharFormat(fmt)

    def format_underline(self) -> None:
        """
        Включает или выключает подчеркивание для выделенного текста в QTextEdit.
        """
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.text_edit.setCurrentCharFormat(fmt)

    def change_font(self, font: QFont) -> None:
        """
        Изменяет шрифт для выделенного текста в QTextEdit.

        Args:
        - font (QFont): Выбранный шрифт.
        """
        fmt = self.text_edit.currentCharFormat()
        fmt.setFont(font)
        self.text_edit.setCurrentCharFormat(fmt)

    def change_font_size(self, size: int) -> None:
        """
        Изменяет размер шрифта для выделенного текста в QTextEdit.

        Args:
        - size (int): Размер шрифта.
        """
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontPointSize(size)
        self.text_edit.setCurrentCharFormat(fmt)

    def change_color(self) -> None:
        """
        Открывает диалог выбора цвета для изменения цвета выделенного текста в QTextEdit.
        """
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = self.text_edit.currentCharFormat()
            fmt.setForeground(color)
            self.text_edit.setCurrentCharFormat(fmt)

    def open_file(self) -> None:
        """
        Открывает диалог выбора файла для открытия и загружает содержимое файла в QTextEdit.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.setPlainText(content)

    def save_file(self) -> None:
        """
        Открывает диалог выбора файла для сохранения и сохраняет содержимое QTextEdit в выбранный файл.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Текстовые файлы (*.txt)")
        if file_path:
            content = self.text_edit.toPlainText()
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
