# Функция для приветствия
def greet(name):
    return f"Hello, {name}!"

# Ввод имени пользователя
name = input("Введите ваше имя: ")

# Приветствие пользователя
print(greet(name))

# Пример работы с числами
a = 10
b = 5

# Операции с числами
sum_result = a + b
diff_result = a - b
prod_result = a * b
div_result = a / b

# Вывод результатов операций
print(f"Сумма: {sum_result}")
print(f"Разность: {diff_result}")
print(f"Произведение: {prod_result}")
print(f"Частное: {div_result}")

# Простая проверка с условием
if a > b:
    print(f"{a} больше чем {b}")
else:
    print(f"{b} больше чем {a}")

