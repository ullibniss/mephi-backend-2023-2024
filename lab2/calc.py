#!/usr/bin/env python3

import re
from operator import add, sub, mul, truediv
from stack import Stack
from compf import Compf


class Calc(Compf):
    """
    Интерпретатор арифметических выражений вычисляет значения
    правильных арифметических формул, в которых в качестве
    операндов допустимы только цифры [0-9]
    """

    SYMBOLS = re.compile("[0-9]")

    def __init__(self):
        # Инициализация (конструктор) класса Compf
        super().__init__()
        # Создание стека чисел для работы стекового калькулятора
        self.r = Stack()
        self.a = []
    # Интерпретация арифметического выражения
    def compile(self, str):
        self.a.clear()
        Compf.compile(self, str)

        return self.r.top()
    
    def process_symbol(self, c):
        if c == "(":
            self.s.push(c)
        elif c == ")":
            self.process_suspended_operators(c)
            self.s.pop()
        elif c in "+-*/":
            self.process_suspended_operators(c)
            self.s.push(c)
        elif c == "$":
            self.s.push(c)
        elif self.s.top() == "$":
            self.s.pop()
            self.check_symbol(c)
            self.process_variable(c)
        else:
            self.check_symbol(c)
            self.a.append(c)
            self.process_value(c)
    
    def process_variable(self, c):
        self.r.push(len([int(i) for i in self.a if int(i) <= int(c)]))

    # Обработка цифры
    def process_value(self, c):
        self.r.push(int(c))
    # Обработка символа операции
    def process_oper(self, c):
        second, first = self.r.pop(), self.r.pop()
        self.r.push({"+": add, "-": sub, "*": mul,
                     "/": truediv}[c](first, second))


if __name__ == "__main__":
    c = Calc()
    while True:
        str = input("Арифметическое выражение: ")
        print(f"Результат его вычисления: {c.compile(str)}")
        print()
