from config import *
class ToolBar:
    """
    Класс для создания и управления панелью инструментов в главном окне.

    Методы:
    - __init__(parent: QMainWindow) -> None: Инициализирует панель инструментов и добавляет элементы управления для выбора шрифта, размера шрифта и цвета текста.
    - add_toolbar_action(name: str, method: callable) -> None: Добавляет действие с указанным именем и методом на панель инструментов.
    """
    def __init__(self, parent: QMainWindow) -> None:
        """
        Инициализирует панель инструментов и добавляет элементы управления для выбора шрифта, размера шрифта и цвета текста.

        Args:
        - parent (QMainWindow): Родительское окно главного приложения.
        """
        self.parent = parent
        self.tool_bar = QToolBar()
        self.parent.addToolBar(self.tool_bar)
        self.create_toolbar()

    def create_toolbar(self) -> None:
        """
        Создает панель инструментов с элементами управления для выбора шрифта, размера шрифта и цвета текста.
        """
        self.parent.font_combo = QFontComboBox()
        self.parent.font_combo.currentFontChanged.connect(self.parent.change_font)
        self.parent.font_combo.setFixedHeight(40)
        self.tool_bar.addWidget(self.parent.font_combo)

        self.parent.size_spin = QSpinBox()
        self.parent.size_spin.setValue(14)
        self.parent.size_spin.valueChanged.connect(self.parent.change_font_size)
        self.parent.size_spin.setFixedHeight(40)
        self.tool_bar.addWidget(self.parent.size_spin)

        self.parent.color_button = QAction(QIcon(), "Цвет", self.parent)
        self.parent.color_button.triggered.connect(self.parent.change_color)
        self.tool_bar.addAction(self.parent.color_button)

        self.tool_bar.setIconSize(QSize(32, 32))

        self.add_toolbar_action("Жирный", self.parent.format_bold)
        self.add_toolbar_action("Курсив", self.parent.format_italic)
        self.add_toolbar_action("Подчеркнутый", self.parent.format_underline)

    def add_toolbar_action(self, name: str, method: callable) -> None:
        """
        Добавляет действие с указанным именем и методом на панель инструментов.

        Args:
        - name (str): Название действия.
        - method (callable): Функция или метод, который будет вызываться при активации действия.
        """
        action = QAction(name, self.parent)
        action.triggered.connect(method)
        self.tool_bar.addAction(action)