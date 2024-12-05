import tkinter as tk
import math

class Display:
    def __init__(self, parent) -> None:
        root.title("Kenda Calculator")
        root.geometry("350x550")
        self.entry = tk.Entry(parent, font=("Arial", 24), justify="right", bd=10)
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

    def update(self, value) -> None:
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

    def clear(self) -> None:
        self.update("")

class CalculatorEngine:
    def __init__(self) -> int:
        self.expression = ""

    def append(self, value) -> int:
        if value == "^":
            self.expression += "**"
        else:
            self.expression += value

    def clear(self) -> None:
        self.expression = ""
    def percentage(self):
        try:
            if self.expression.endswith('%'):
                value=float(self.expression[:-1])
                return str(value/100)
            else:
                # value = float(self.expression[:-1])
                return str(eval(self.expression)/100)
            # else:
            #     return "Error"
        except Exception:
            return 'Errror'
        
    def sqrt(self):
        try:
            if self.expression('✓'):
                value=float(self.expression)
                return str(math.sqrt(value))
            elif self.expression:
                value = float(self.expression[:-1])
                return str(math.sqrt(value))
            else:
                return "Error"
        except Exception:
            return 'Errror'
    
    def calculate(self) -> int:
        try:
            return str(eval(self.expression))
        except Exception:
            return "Error"

class CalculatorUI:
    def __init__(self, root) -> int:
        self.engine = CalculatorEngine()
        self.display = Display(root)

        # Configure rows and columns
        for i in range(7):
            root.rowconfigure(i, weight=1)
        for i in range(4):
            root.columnconfigure(i, weight=1)

        self.create_buttons()
        root.bind("<Key>", self.handle_keypress)

    def create_buttons(self) -> int:
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0), ("(", 5, 1), (")", 5, 2), ("^", 5, 3),
            ("%", 6, 2), ("✓", 6, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(
                text=text,
                font=("Arial", 18),
                bg=self.get_button_color(text),
                command=lambda t=text: self.on_button_click(t),
            )
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def get_button_color(self, text) -> str:
        if text in "0123456789.":
            return "#f0f0f0"
        elif text in "+-*/^":
            return "#ffa07a"
        elif text == "=":
            return "#90ee90"
        elif text == "C":
            return "#ff6347"
        return "#d3d3d3"

    def on_button_click(self, char) -> int:
        if char == "C":
            self.engine.clear()
        elif char == "=":
            result = self.engine.calculate()
            return self.display.update(result)
        else:
            self.engine.append(char)

        self.display.update(self.engine.expression)

    def handle_keypress(self, event) -> int:
        char = event.char
        if char in "0123456789+-*/().":
            self.engine.append(char)

        elif char == "\r":  # Enter key
            result = self.engine.calculate()
            return self.display.update(result)
        
        elif char == '%':
            result = self.engine.percentage()
            self.display.update(result)
            return
        
        elif char == '✓':
            result = self.engine.sqrt()
            self.display.update(result)
            return

        elif char == "\x08":  # Backspace
            # self.engine.expression = self.engine.expression[:-1]
            self.engine.clear()
        self.display.update(self.engine.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = CalculatorUI(root)
    root.mainloop()