from typing import Protocol, Any
import tkinter as tk

# Protocols for Duck Typing
class DisplayProtocol(Protocol):
    def update(self, value: str) -> None:
        ...

    def clear(self) -> None:
        ...

class EngineProtocol(Protocol):
    expression: str

    def append(self, value: str) -> None:
        ...

    def clear(self) -> None:
        ...

    def calculate(self) -> str:
        ...

class Display:
    def __init__(self, parent: tk.Tk) -> None:
        self.entry = tk.Entry(parent, font=("Arial", 20), justify="right", bd=10)
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

    def update(self, value: str) -> None:
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

    def clear(self) -> None:
        self.update("")

class CalculatorEngine:
    def __init__(self) -> None:
        self.expression: str = ""

    def append(self, value: str) -> None:
        if value == "^":
            self.expression += "**"
        else:
            self.expression += value

    def clear(self) -> None:
        self.expression = ""

    def calculate(self) -> str:
        try:
            return str(eval(self.expression))
        except Exception:
            return "Error"

class CalculatorUI:
    def __init__(self, root: tk.Tk, display: DisplayProtocol, engine: EngineProtocol) -> None:
        self.engine = engine
        self.display = display

        for i in range(6):
            root.rowconfigure(i, weight=1)
        for i in range(4):
            root.columnconfigure(i, weight=1)

        self.create_buttons()
        root.bind("<Key>", self.handle_keypress)

    def create_buttons(self) -> None:
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0), ("(", 5, 1), (")", 5, 2), ("^", 5, 3),
        ]

        for (text, row, col) in buttons:
            button = tk.Button(
                text=text,
                font=("Arial", 18),
                bg=self.get_button_color(text),
                command=lambda t=text: self.on_button_click(t),
            )
            button.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

    def get_button_color(self, text: str) -> str:
        if text in "0123456789.":
            return "#f0f0f0"
        elif text in "+-*/^":
            return "#ffa07a"
        elif text == "=":
            return "#90ee90"
        elif text == "C":
            return "#ff6347"
        return "#d3d3d3"

    def on_button_click(self, char: str) -> None:
        if char == "C":
            self.engine.clear()
        elif char == "=":
            result = self.engine.calculate()
            self.display.update(result)
            return
        else:
            self.engine.append(char)

        self.display.update(self.engine.expression)

    def handle_keypress(self, event: Any) -> None:
        char = event.char
        if char in "0123456789+-*/().":
            self.engine.append(char)
        elif char == "\r":  # Enter key
            result = self.engine.calculate()
            self.display.update(result)
        elif char == "\x08":  # Backspace
            self.engine.expression = self.engine.expression[:-1]
        self.display.update(self.engine.expression)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Duck Type Calculator")
    root.geometry("400x600")

    display: DisplayProtocol = Display(root)
    engine: EngineProtocol = CalculatorEngine()
    calculator = CalculatorUI(root, display, engine)

    root.mainloop()