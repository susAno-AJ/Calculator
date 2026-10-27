import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("Calculator")
        root.configure(bg="#1e1e2e")
        root.resizable(False, False)

        self.expr = ""
        self.display = tk.Entry(root, font=("Arial", 24), justify="right",
                                bd=0, bg="#111", fg="white", insertbackground="white")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=12, sticky="we")

        buttons = [
            ("C", 1, 0), ("⌫", 1, 1), ("%", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2),
        ]
        for text, r, c in buttons:
            color = "#3b3b52"
            if text in "/*-+": color = "#f59e0b"
            elif text == "=": color = "#22c55e"
            elif text == "C": color = "#ef4444"
            span = 2 if text == "=" else 1
            tk.Button(root, text=text, font=("Arial", 16), bg=color, fg="white",
                      bd=0, width=4, height=2,
                      command=lambda t=text: self.press(t)
                      ).grid(row=r, column=c, columnspan=span, padx=4, pady=4, sticky="we")

        root.bind("<Key>", self.key)

    def update(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr or "0")

    def press(self, t):
        if t == "C":
            self.expr = ""
        elif t == "⌫":
            self.expr = self.expr[:-1]
        elif t == "%":
            try: self.expr = str(float(self.expr) / 100)
            except ValueError: self.expr = "Error"
        elif t == "=":
            try:
                # restrict to safe characters before evaluating
                if not set(self.expr) <= set("0123456789.+-*/ "):
                    raise ValueError
                result = eval(self.expr)
                self.expr = str(round(result, 10)).rstrip("0").rstrip(".") if "." in str(result) else str(result)
            except Exception:
                self.expr = "Error"
        else:
            if self.expr == "Error": self.expr = ""
            self.expr += t
        self.update()

    def key(self, e):
        if e.char in "0123456789.+-*/": self.press(e.char)
        elif e.keysym == "Return": self.press("=")
        elif e.keysym == "BackSpace": self.press("⌫")
        elif e.keysym == "Escape": self.press("C")

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
