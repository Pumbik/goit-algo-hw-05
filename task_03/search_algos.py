import timeit
from pathlib import Path

# 1. Алгоритм Кнута-Морріса-Пратта (KMP)
def build_prefix_table(pattern):
    table = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = table[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        table[i] = j
    return table

def kmp_search(text, pattern):
    table = build_prefix_table(pattern)
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = table[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            return i - j + 1  # Знайшли входження
            # j = table[j - 1] # Якщо треба знайти всі входження
    return -1

# 2. Алгоритм Боєра-Мура (Boyer-Moore)
# Реалізація з евристикою "поганого символу" (Bad Character Heuristic)
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for i in range(length - 1):
        table[pattern[i]] = length - 1 - i
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    len_p = len(pattern)
    len_t = len(text)
    i = 0

    while i <= len_t - len_p:
        j = len_p - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i  # Знайшли входження
        else:
            # Зсув на основі таблиці або на 1, якщо символу немає в таблиці
            bad_char = text[i + len_p - 1]
            i += shift_table.get(bad_char, len_p)
    return -1

# 3. Алгоритм Рабіна-Карпа (Rabin-Karp)
def rabin_karp_search(text, pattern):
    len_t = len(text)
    len_p = len(pattern)
    
    if len_p > len_t:
        return -1

    base = 256 
    modulus = 101  # Просте число для хешування
    
    p_hash = 0
    t_hash = 0
    h = 1

    # Попереднє обчислення h = pow(base, len_p-1) % modulus
    for i in range(len_p - 1):
        h = (h * base) % modulus

    # Обчислення хешу для патерну і першого вікна тексту
    for i in range(len_p):
        p_hash = (base * p_hash + ord(pattern[i])) % modulus
        t_hash = (base * t_hash + ord(text[i])) % modulus

    for i in range(len_t - len_p + 1):
        if p_hash == t_hash:
            # Якщо хеші співпали, перевіряємо посимвольно (на випадок колізії)
            if text[i:i + len_p] == pattern:
                return i
        
        if i < len_t - len_p:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + len_p])) % modulus
            if t_hash < 0:
                t_hash += modulus
    return -1


 # ---------------------------------------------

def read_file(filename):
    try:
        with open(filename, 'r', encoding='cp1251') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

BASE_DIR = Path(__file__).resolve().parent

path_1 = BASE_DIR / "стаття 1.txt"
path_2 = BASE_DIR / "стаття 2.txt"

try:
    text1 = read_file(path_1)
    text2 = read_file(path_2)
    print(f"Файли успішно завантажено!")
except FileNotFoundError as e:
    print(f"Помилка! Файл не знайдено: {e}")
    print(f"Програма шукає тут: {BASE_DIR}")
    exit()

# Визначаємо підрядки для пошуку
# Для Статті 1 (Алгоритми)
real_sub_1 = "алгоритм"      # Існує
fake_sub_1 = "марсохід"      # Вигадане

# Для Статті 2 (Бази даних)
real_sub_2 = "рекомендацій"  # Існує
fake_sub_2 = "крокодил"      # Вигадане

print(f"{'Algorithm':<20} | {'Text':<10} | {'Type':<10} | {'Time (sec)':<15}")
print("-" * 65)

# Функція для зручного запуску тесту
def benchmark(algo, text, pattern, name):
    time = timeit.timeit(lambda: algo(text, pattern), number=100)
    print(f"{name:<20} | {'Art 1' if text == text1 else 'Art 2':<10} | {'Exist' if 'алгоритм' in pattern or 'рекомендацій' in pattern else 'Fake':<10} | {time:.5f}")

# --- ТЕСТУВАННЯ СТАТТЯ 1 ---
for algo, name in [(kmp_search, "KMP"), (boyer_moore_search, "Boyer-Moore"), (rabin_karp_search, "Rabin-Karp")]:
    benchmark(algo, text1, real_sub_1, name)
    benchmark(algo, text1, fake_sub_1, name)

print("-" * 65)

# --- ТЕСТУВАННЯ СТАТТЯ 2 ---
for algo, name in [(kmp_search, "KMP"), (boyer_moore_search, "Boyer-Moore"), (rabin_karp_search, "Rabin-Karp")]:
    benchmark(algo, text2, real_sub_2, name)
    benchmark(algo, text2, fake_sub_2, name)