from tkinter import *
from typing import Tuple, List, Optional

class Calculator:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("Calculator")
        
        # Add padding around the window
        self.root.configure(padx=15, pady=15)
        
        # Color scheme
        self.DIGIT_COLOR: str = "#ffffff"
        self.OPERATOR_COLOR: str = "#ff9500"
        self.CLEAR_COLOR: str = "#ff4444"
        self.EQUAL_COLOR: str = "#4CAF50"
        self.BUTTON_TEXT_COLOR: str = "#000000"
        
        # Initialize variables
        self.current_number: str = ""
        self.first_number: float = 0
        self.operation: str = ""
        
        # Create and configure entry widget with larger size and font
        self.display = Entry(
            root, 
            width=20,              # Reduced width since we're using larger font
            borderwidth=5,
            justify=RIGHT,
            font=('Arial', 24),    # Larger font for better visibility
            bg='#f0f0f0'          # Light gray background
        )
        self.display.grid(
            row=0, 
            column=0, 
            columnspan=3, 
            padx=10, 
            pady=20,
            sticky='nsew'         # Make display expand to fill space
        )
        
        # Configure grid columns to expand properly
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        
        # Create buttons
        self.create_buttons()

        # Bind keyboard events
        self.bind_keyboard()

    def create_buttons(self) -> None:
        # Button layout configuration
        button_config: List[Tuple[str, int, int]] = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 0)
        ]

        # Common button style
        button_style = {
            'padx': 35,
            'pady': 15,
            'font': ('Arial', 14, 'bold'),
            'borderwidth': 2,
            'relief': 'raised'
        }

        # Create digit buttons
        for (digit, row, col) in button_config:
            btn = Button(
                self.root,
                text=digit,
                bg=self.DIGIT_COLOR,
                fg=self.BUTTON_TEXT_COLOR,
                command=lambda x=digit: self.button_click(x),
                **button_style
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

        # Create operator buttons
        operators: List[Tuple[str, int, int]] = [
            ('+', 5, 0), ('-', 6, 0),
            ('*', 6, 1), ('/', 6, 2)
        ]

        for (op, row, col) in operators:
            btn = Button(
                self.root,
                text=op,
                bg=self.OPERATOR_COLOR,
                fg=self.BUTTON_TEXT_COLOR,
                command=lambda x=op: self.button_operator(x),
                **button_style
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

        # Create clear button
        self.clear_btn = Button(
            self.root,
            text="Clear",
            bg=self.CLEAR_COLOR,
            fg='white',
            command=self.button_clear,
            **button_style
        )
        self.clear_btn.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Create equals button
        self.equals_btn = Button(
            self.root,
            text="=",
            bg=self.EQUAL_COLOR,
            fg='white',
            command=self.button_equal,
            **button_style
        )
        self.equals_btn.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky='nsew')

    def bind_keyboard(self) -> None:
        self.root.bind('<Key>', self.handle_keypress)
        self.root.bind('<Return>', lambda event: self.button_equal())
        self.root.bind('<Escape>', lambda event: self.button_clear())
        self.root.bind('<BackSpace>', self.handle_backspace)

    def handle_keypress(self, event: Event) -> None:
        valid_chars = '0123456789+-*/.='
        if event.char in valid_chars:
            if event.char in '0123456789.':
                self.button_click(event.char)
            elif event.char in '+-*/':
                self.button_operator(event.char)
            elif event.char == '=':
                self.button_equal()

    def handle_backspace(self, event: Event) -> None:
        current = self.display.get()
        self.display.delete(0, END)
        self.display.insert(0, current[:-1])

    def button_click(self, number: str) -> None:
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
            self.display.delete(0, END)
            self.display.insert(0, "Error")

    def button_equal(self) -> None:
        try:
            second_number = float(self.display.get())
            self.display.delete(0, END)
            
            result: Optional[float] = None
            
            if self.operation == "+":
                result = self.first_number + second_number
            elif self.operation == "-":
                result = self.first_number - second_number
            elif self.operation == "*":
                result = self.first_number * second_number
            elif self.operation == "/":
                if second_number != 0:
                    result = self.first_number / second_number
                else:
                    self.display.insert(0, "Error: Div by 0")
                    return
            
            if result is not None:
                # Format result to remove trailing zeros if it's a whole number
                if result.is_integer():
                    self.display.insert(0, int(result))
                else:
                    # Limit decimal places to 8 for cleaner display
                    self.display.insert(0, f"{result:.8g}")
                
        except ValueError:
            self.display.delete(0, END)
            self.display.insert(0, "Error")

if __name__ == "__main__":
    root = Tk()
    calculator = Calculator(root)
    root.mainloop()