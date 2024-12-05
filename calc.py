from tkinter import *

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Class-based Calculator")
        
        # Entry widget for input
        self.entry = Entry(root, width=35, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
        # Variables for calculations
        self.f_num = None
        self.math = None
        
        # Create buttons
        self.create_buttons()
    
    def create_buttons(self):
        # Define button texts and commands
        button_texts = [
            ("7", self.button_click), ("8", self.button_click), ("9", self.button_click), ("/", self.button_operator),
            ("4", self.button_click), ("5", self.button_click), ("6", self.button_click), ("*", self.button_operator),
            ("1", self.button_click), ("2", self.button_click), ("3", self.button_click), ("-", self.button_operator),
            ("C", self.button_clear), ("0", self.button_click), ("=", self.button_equal), ("+", self.button_operator),
        ]
        
        # Colors for buttons
        operator_color = "orange"
        clear_color = "red"
        equal_color = "green"
        
        # Define button properties and place them
        for i, (text, command) in enumerate(button_texts):
            row = i // 4 + 1
            col = i % 4
            if text in "+-*/":
                btn = Button(self.root, text=text, padx=20, pady=10, bg=operator_color, command=lambda t=text: command(t))
            elif text == "C":
                btn = Button(self.root, text=text, padx=20, pady=10, bg=clear_color, command=command)
            elif text == "=":
                btn = Button(self.root, text=text, padx=20, pady=10, bg=equal_color, command=command)
            else:
                btn = Button(self.root, text=text, padx=20, pady=10, command=lambda t=text: command(t))
            btn.grid(row=row, column=col)

    def button_click(self, number):
        current = self.entry.get()
        self.entry.delete(0, END)
        self.entry.insert(0, str(current) + str(number))
    
    def button_clear(self):
        self.entry.delete(0, END)
    
    def button_operator(self, operator) -> int:
        self.f_num = self.entry.get()
        self.math = operator
        self.entry.delete(0, END)
    
    def button_equal(self) -> int:
        second_number = self.entry.get()
        self.entry.delete(0, END)
        try:
            if self.math == "+":
                self.entry.insert(0, self.f_num + second_number)
            elif self.math == "-":
                self.entry.insert(0, self.f_num - second_number)
            elif self.math == "*":
                self.entry.insert(0, self.f_num * second_number)
            elif self.math == "/":
                if second_number != 0:
                    self.entry.insert(0, self.f_num / second_number)
                else:
                    self.entry.insert(0, "Error")
        except Exception as e:
            self.entry.insert(0, "Error")

# Initialize the application
if __name__ == "__main__":
    root = Tk()
    app = CalculatorApp(root)
    root.mainloop()