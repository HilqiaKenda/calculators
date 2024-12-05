from tkinter import *
from typing import Union, Tuple, List, Optional, Protocol, Any
from typing_extensions import TypedDict

# Protocol for widget positioning
class Positionable(Protocol):
    def grid(self, **kwargs: Any) -> None: ...

# TypedDict for button configuration
class ButtonConfig(TypedDict):
    padx: int
    pady: int
    font: Tuple[str, int, str]
    borderwidth: int
    relief: str

class Calculator:
    def __init__(self, root: Any) -> None:  # Using Any for root allows duck typing for Tk-like objects
        if not hasattr(root, 'title') or not callable(getattr(root, 'title')):
            raise TypeError("root must have a 'title' method")
            
        self.root = root
        self.root.title("Calculator")
        self.root.configure(padx=15, pady=15)
        
        # Color constants with semantic typing
        ColorHex = str  # Type alias for hex color strings
        self.COLORS: dict[str, ColorHex] = {
            'DIGIT': "#ffffff",     # White
            'OPERATOR': "#ff9500",  # Orange
            'CLEAR': "#ff4444",     # Red
            'EQUAL': "#4CAF50",     # Green
            'TEXT': "#000000",      # Black
            'DISPLAY_BG': "#f0f0f0" # Light gray
        }
        
        # State variables with explicit typing
        self.current_number: str = ""
        self.first_number: float = 0
        self.operation: str = ""
        
        # Create UI components
        self._setup_display()
        self._configure_grid()
        self._create_buttons()
        self._bind_keyboard()

    def _setup_display(self) -> None:
        self.display = Entry(
            self.root, 
            width=20,
            borderwidth=5,
            justify=RIGHT,
            font=('Arial', 24),
            bg=self.COLORS['DISPLAY_BG']
        )
        self._position_widget(
            self.display,
            row=0, 
            column=0, 
            columnspan=3, 
            padx=10, 
            pady=20,
            sticky='nsew'
        )

    def _configure_grid(self) -> None:
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)

    def _position_widget(self, widget: Positionable, **grid_args: Any) -> None:
        """Position any widget that supports the grid method"""
        widget.grid(**grid_args)

    def _create_buttons(self) -> None:
        # Button style configuration using TypedDict
        button_style: ButtonConfig = {
            'padx': 45,
            'pady': 25,
            'font': ('Arial', 14, 'bold'),
            'borderwidth': 2,
            'relief': 'raised'
        }

        # Create digit buttons
        self._create_digit_buttons(button_style)
        # Create operator buttons
        self._create_operator_buttons(button_style)
        # Create special buttons (clear and equals)
        self._create_special_buttons(button_style)

    def _create_digit_buttons(self, style: ButtonConfig) -> None:
        button_config: List[Tuple[str, int, int]] = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 0)
        ]

        for digit, row, col in button_config:
            btn = self._create_button(
                text=digit,
                bg=self.COLORS['DIGIT'],
                fg=self.COLORS['TEXT'],
                command=lambda x=digit: self.button_click(x),
                **style
            )
            self._position_widget(btn, row=row, column=col, padx=5, pady=5, sticky='nsew')

    def _create_operator_buttons(self, style: ButtonConfig) -> None:
        operators: List[Tuple[str, int, int]] = [
            ('+', 5, 0), ('-', 6, 0),
            ('*', 6, 1), ('/', 6, 2)
        ]

        for op, row, col in operators:
            btn = self._create_button(
                text=op,
                bg=self.COLORS['OPERATOR'],
                fg=self.COLORS['TEXT'],
                command=lambda x=op: self.button_operator(x),
                **style
            )
            self._position_widget(btn, row=row, column=col, padx=5, pady=5, sticky='nsew')

    def _create_special_buttons(self, style: ButtonConfig) -> None:
        # Clear button
        clear_btn = self._create_button(
            text="Clear",
            bg=self.COLORS['CLEAR'],
            fg='white',
            command=self.button_clear,
            **style
        )
        self._position_widget(clear_btn, row=4, column=1, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Equals button
        equals_btn = self._create_button(
            text="=",
            bg=self.COLORS['EQUAL'],
            fg='white',
            command=self.button_equal,
            **style
        )
        self._position_widget(equals_btn, row=5, column=1, columnspan=2, padx=5, pady=5, sticky='nsew')

    def _create_button(self, **kwargs: Any) -> Button:
        return Button(self.root, **kwargs)

    def _bind_keyboard(self) -> None:
        self.root.bind('<Key>', self._handle_keypress)
        self.root.bind('<Return>', lambda e: self.button_equal())
        self.root.bind('<Escape>', lambda e: self.button_clear())
        self.root.bind('<BackSpace>', self._handle_backspace)

    def _handle_keypress(self, event: Any) -> None:
        if not hasattr(event, 'char'):
            return
            
        valid_chars = '0123456789+-*/.='
        if event.char in valid_chars:
            if event.char in '0123456789.':
                self.button_click(event.char)
            elif event.char in '+-*/':
                self.button_operator(event.char)
            elif event.char == '=':
                self.button_equal()

    def _handle_backspace(self, _: Any) -> None:
        current = self.display.get()
        self.display.delete(0, END)
        self.display.insert(0, current[:-1])

    def button_click(self, number: Union[str, int]) -> None:
        current = self.display.get()
        self.display.delete(0, END)
        self.display.insert(0, current + str(number))

    def button_clear(self) -> None:
        self.display.delete(0, END)
        self.first_number = 0
        self.operation = ""

    def button_operator(self, op: str) -> None:
        try:
            self.first_number = float(self.display.get())
            self.operation = op
            self.display.delete(0, END)
        except ValueError:
            self._show_error("Invalid input")

    def button_equal(self) -> None:
        try:
            second_number = float(self.display.get())
            self.display.delete(0, END)
            
            result = self._calculate(second_number)
            if result is not None:
                self._display_result(result)
                
        except ValueError:
            self._show_error("Invalid input")

    def _calculate(self, second_number: float) -> Optional[float]:
        """Perform calculation based on operation"""
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else None
        }
        
        operation_func = operations.get(self.operation)
        if operation_func is None:
            self._show_error("Invalid operation")
            return None
            
        result = operation_func(self.first_number, second_number)
        if result is None:
            self._show_error("Division by zero")
            return None
            
        return result

    def _display_result(self, result: float) -> None:
        """Format and display the calculation result"""
        if result.is_integer():
            self.display.insert(0, int(result))
        else:
            self.display.insert(0, f"{result:.8g}")

    def _show_error(self, message: str) -> None:
        """Display error message"""
        self.display.delete(0, END)
        self.display.insert(0, f"Error: {message}")

if __name__ == "__main__":
    root = Tk()
    calculator = Calculator(root)
    root.mainloop()