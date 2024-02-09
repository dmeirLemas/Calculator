# %%
import tkinter as tk


class ResizableEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        self.var = kwargs.get("textvariable", tk.StringVar())
        self.var.trace_add("write", self.adjust_width)
        self.width = 16
        self.config(width=self.width)

    def adjust_width(self, *args):
        text_length = len(self.var.get())
        new_width = max(self.width, text_length)
        self.config(width=new_width)


class Calculator(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Calculator")
        self.pack()

        self.entry_var = tk.StringVar()
        self.entry = ResizableEntry(
            self,
            textvariable=self.entry_var,
            font=("Helvetica", 25),
            bd=8,
            insertwidth=4,
            justify="right",
        )
        self.entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            "(",
            ")",
            "%",
            "CE",
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "x",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "=",
            "+",
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            tk.Button(
                self,
                text=button,
                font=("Helvetica", 12),
                height=1,
                width=1,
                padx=10,
                pady=10,
                command=lambda btn=button: self.on_button_click(btn),
            ).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def on_button_click(self, btn):
        if btn == "=":
            try:
                self._entry = self.entry_var.get()
                result = self.evaluate(self.entry_var.get())
                self.entry_var.set(str(result))
            except Exception as e:
                self.entry_var.set(f"Error: {e}")
        elif btn == "CE":
            self.entry_var.set("")
        else:
            if ":" in self.entry_var.get():
                self.entry_var.set("")
            curr_text = self.entry_var.get()
            new_text = curr_text + str(btn)
            self.entry_var.set(new_text)

    def evaluate(self, s: str) -> float:
        if "%" in s:
            return r"% is not implemented yet. (Sorry)"
        s = s.replace(" ", "")
        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "/": lambda x, y: x / y,
            "x": lambda x, y: x * y,
        }

        order = {"+": 1, "-": 1, "/": 2, "x": 2}

        t = self.parser(s, ops)

        numbers: list[float] = []
        opers: list[str] = []
        curr_num = ""

        for char in t:
            if char.isdigit() or char == ".":
                curr_num += char
            elif char in ops:
                numbers.append(float(curr_num))
                curr_num = ""
                while opers and order[opers[-1]] >= order[char]:
                    numbers.append(ops[opers.pop()](numbers.pop(-2), numbers.pop()))
                opers.append(char)

        if curr_num:
            numbers.append(float(curr_num))

        while opers:
            numbers.append(ops[opers.pop()](numbers.pop(-2), numbers.pop()))

        return numbers[0]

    def parser(self, s: str, ops: dict) -> str:
        i = 0
        curr_expr = ""
        while i < len(s):
            j = i + 1
            if s[i].isdigit() or s[i] == "." or s[i] in ops:
                curr_expr += s[i]
            elif s[i] == "(":
                inner_expr = ""
                open_parentheses = 1
                close_parentheses = 0
                while open_parentheses > close_parentheses:
                    if s[j] == "(":
                        open_parentheses += 1
                    elif s[j] == ")":
                        close_parentheses += 1
                    if open_parentheses > close_parentheses:
                        inner_expr += s[j]
                    j += 1
                t = self.evaluate(inner_expr)
                curr_expr += str(t)
            else:
                return f"Error: Unexpected character '{s[i]}' at position {i}. Parsing state: {curr_expr}"
            i = j

        return curr_expr


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    calculator.mainloop()
