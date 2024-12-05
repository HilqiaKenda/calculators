import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Mbenza Calculator")
        self.root.geometry("400x400")

        self.expression = ""
        self.display = tk.Entry(self.root, font=("Arial", 24), justify='right', bd=10)
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew')

        # Configure rows and columns
        for I in range(5):
            self.root.rowconfigure(I, weight=1)
        for I in range(4):
            self.root.columnconfigure(I, weight=1)

        self.create_button()
        self.root.bind('<Key>', self.key_press)

    
    def create_button(self) -> int:
        buttons = [
            ('7', 1, 1), ('8', 1, 2), ('9', 1, 3), ('/', 1, 0),
            ('4', 2, 1), ('5', 2, 2), ('6', 2, 3), ('*', 2, 0),
            ('1', 3, 1), ('2', 3, 2), ('3', 3, 3), ('-', 3, 0),
            ('0', 4, 2), ('.', 4, 3), ('=', 5, 1), ('+', 4, 0),
            ('C', 4, 1), ('(', 5, 2), (')', 5, 3), ('^', 5, 0),
        ]

        for (text, row, col) in buttons:
            if text in "0123456789":
                bg_color = '#f0f0f0'
            elif text in "-+*/^":
                bg_color = "#b8860b"
            elif text in "=":
                bg_color = "#008000"
            elif text in "C":
                bg_color = "#ff0000"
                
            else:
                bg_color = "#ff8c00"
                
            Button = tk.Button(self.root, text=text, font=("Arial", 18), bg=bg_color, command=lambda t=text: self.button_click(t))
            Button.grid(row=row, column=col, stick='nsew', padx=5, pady=5)

    def button_click(self, char) -> int:
        if char == "C":
            self.expression = ""
        elif char == "=":
            self.calculate()
        elif char == "^":
            self.expression += "**"
        else:
            self.expression += char
        self.update_display()
    
    def key_press(self, event) -> int:
        char = event.char
        if char in "0123456789+-*/().":
            self.expression += char
        elif char == "\r":
            self.calculate()
        elif char == "\x08":
            self.expression = self.expression[:-1]
        self.update_display()
    
    def calculate(self) -> int:
        try:
            result = eval(self.expression)
            self.expression = str(result)
        except Exception as e:
            self.expression = "Error"
        self.update_display()

    
    def update_display(self) -> None:
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
