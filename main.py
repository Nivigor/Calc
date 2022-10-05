from PyQt5.QtWidgets import QMainWindow, QApplication

import operator

from vis import Ui_kalkuliktor

# Константы состояния калькулятора.
READY = 0
INPUT = 1


class MainWindow(QMainWindow, Ui_kalkuliktor):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Кнопки цифр привязываем к одной функции через обертку
        for n in range(0, 10):
            getattr(self, 'k_%s' % n).pressed.connect(lambda v=n: self.input_number(v))

        # Кнопки операций привязываем к одной функции через обертку
        # Вместо операторов +-*/ будем использовать фукции из модуля operator
        self.k_sum.pressed.connect(lambda: self.operation(operator.add))
        self.k_vich.pressed.connect(lambda: self.operation(operator.sub))
        self.k_mnog.pressed.connect(lambda: self.operation(operator.mul))
        self.k_del.pressed.connect(lambda: self.operation(operator.truediv))

        self.k_result.pressed.connect(self.equals) # =
        self.k_num.pressed.connect(self.signum) # +/-
        self.k_clear.pressed.connect(self.reset) # <
        self.k_stir.pressed.connect(self.reset_input) # C

        self.reset() #Начальный сброс

    # Отобразить число на вершине стека
    def display(self):
        self.lcdNumber.display(self.stack[-1])

    # Ввод цифры
    def input_number(self, v):
        if self.state == READY: #Первая цифра
            self.state = INPUT
            self.stack[-1] = v
        else:
            self.stack[-1] = self.stack[-1] * 10 + (-v if self.stack[-1] < 0 else v)
        self.display()

    def operation(self, op):
        if self.current_op:  # Завершаем текущую операцию
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = op

    def equals(self):
        # Используем '=' для повторения операции
        # если не было ввода
        if self.state == READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            try:
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.lcdNumber.display('Err')
                self.stack = [0]
                self.last_operation = None
            else:
                self.display()
            finally:
                self.current_op = None
                self.state = READY


    #Начальные установки, сброс
    def reset(self):
        self.state = READY #Состояние
        self.stack = [0] #Стек (до 2 элементов)
        self.last_operation = None #Последняя операция
        self.current_op = None #Текущая операция
        self.display()

    # Очистка ввода
    def reset_input(self):
        if self.state == INPUT:
            self.stack[-1] = 0
            self.display()

    #Смена знака
    def signum(self):
        self.stack[-1] = -self.stack[-1]
        self.display()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()