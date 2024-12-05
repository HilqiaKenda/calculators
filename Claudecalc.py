from tkinter import *

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        
        # Color scheme
        self.DIGIT_COLOR = "#ffffff"  # White
        self.OPERATOR_COLOR = "#ff9500"  # Orange
        self.CLEAR_COLOR = "#a5a5a5"  # Light gray
        self.EQUAL_COLOR = "#4CAF50"  # Green
        self.BUTTON_TEXT_COLOR = "#000000"  # Black
        
        # Initialize variables
        self.current_number = ""
        self.first_number = 0
        self.operation = ""
        
        # Create and configure entry widget
        self.display = Entry(root, width=35, borderwidth=5, justify=RIGHT)
        self.display.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        # Create buttons
        self.create_buttons()
        
        # Bind keyboard events
        self.bind_keyboard()

    def create_buttons(self):
        # Button layout configuration
        button_config = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 0)
        ]
        
        # Create digit buttons
        for (digit, row, col) in button_config:
            btn = Button(self.root, text=digit, padx=40, pady=20,
                        bg=self.DIGIT_COLOR, fg=self.BUTTON_TEXT_COLOR,
                        command=lambda x=digit: self.button_click(x))
            btn.grid(row=row, column=col)

        # Create operator buttons
        operators = [
            ('+', 5, 0), ('-', 6, 0),
            ('*', 6, 1), ('/', 6, 2)
        ]
        
        for (op, row, col) in operators:
            btn = Button(self.root, text=op, padx=39, pady=20,
                        bg=self.OPERATOR_COLOR, fg=self.BUTTON_TEXT_COLOR,
                        command=lambda x=op: self.button_operator(x))
            btn.grid(row=row, column=col)

        # Create clear button
        self.clear_btn = Button(self.root, text="Clear", padx=79, pady=20,
                              bg=self.CLEAR_COLOR, fg=self.BUTTON_TEXT_COLOR,
                              command=self.button_clear)
        self.clear_btn.grid(row=4, column=1, columnspan=2)

        # Create equals button
        self.equals_btn = Button(self.root, text="=", padx=91, pady=20,
                               bg=self.EQUAL_COLOR, fg=self.BUTTON_TEXT_COLOR,
                               command=self.button_equal)
        self.equals_btn.grid(row=5, column=1, columnspan=2)

    def bind_keyboard(self):
        # Bind digit keys
        self.root.bind('<Key>', self.handle_keypress)
        
        # Bind special keys
        self.root.bind('<Return>', lambda event: self.button_equal())
        self.root.bind('<Escape>', lambda event: self.button_clear())
        self.root.bind('<BackSpace>', self.handle_backspace)

    def handle_keypress(self, event):
        valid_chars = '0123456789+-*/.='
        if event.char in valid_chars:
            if event.char in '0123456789.':
                self.button_click(event.char)
            elif event.char in '+-*/':
                self.button_operator(event.char)
            elif event.char == '=':
                self.button_equal()

    def handle_backspace(self, event):
        current = self.display.get()
        self.display.delete(0, END)
        self.display.insert(0, current[:-1])

    def button_click(self, number):
        current = self.display.get()
        self.display.delete(0, END)
        self.display.insert(0, current + str(number))

    def button_clear(self):
        self.display.delete(0, END)
        self.first_number = 0
        self.operation = ""

    def button_operator(self, op):
        try:
            self.first_number = float(self.display.get())
            self.operation = op
            self.display.delete(0, END)
        except ValueError:
            self.display.delete(0, END)
            self.display.insert(0, "Error")

    def button_equal(self):
        try:
            second_number = float(self.display.get())
            self.display.delete(0, END)
            
            result = 0
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
                
            # Format result to remove trailing zeros if it's a whole number
            if result.is_integer():
                self.display.insert(0, int(result))
            else:
                self.display.insert(0, result)
                
        except ValueError:
            self.display.delete(0, END)
            self.display.insert(0, "Error")

if __name__ == "__main__":
    root = Tk()
    calculator = Calculator(root)
    root.mainloop()