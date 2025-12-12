def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] < target:
            # Якщо елемент <, не підходить як верхня межа.
            # --> праву частину.
            low = mid + 1
        else:
            # Якщо елемент >=, потенційно підходить
            # потенційна верхня межа
            upper_bound = arr[mid]
            
            # перевіряємо чи є меньше.
            # --> ліву частину 
            high = mid - 1

    return iterations, upper_bound


arr = [0.1, 0.5, 1.3, 2.4, 3.8, 4.9, 5.5, 8.1]

print(f"Масив: {arr}")

# є в масиві
result = binary_search(arr, 2.4)
print(f"Шукаємо 2.4 -> Ітерацій: {result[0]}, Верхня межа: {result[1]}")

# немає, шукаємо проміжне
result = binary_search(arr, 3.0)
print(f"Шукаємо 3.0 -> Ітерацій: {result[0]}, Верхня межа: {result[1]}")

# більше за всі елементи
result = binary_search(arr, 10.0)
print(f"Шукаємо 10.0 -> Ітерацій: {result[0]}, Верхня межа: {result[1]}")