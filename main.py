import random as r
import math as m

# Генерация вероятностным методом
# k - размерность (бит)
# n - кол-во
def gen_ver(k,n):
    prost = []
    while 1 == 1:
        p = int((2**(k-1)) + (2**k - 2**(k-1))*r.random()) # Генерация случайного в заданном диапозоне
        if p%2 == 0:
            continue
        c = 0
        for i in range(7):
            x = int(2+(m.sqrt(p)-2)*r.random())
            b = int(x**2) # Квадратичные вычеты
            # Проверка тестов Ферма и Соловея-Штрассена
            if (pow(b,int((p-1)/2),p) != 1) or (pow(b,(p-1), p) != 1):
                break
            c = i
        # Добавление простых чисел в массиве
        if (c == 6) and not (p in prost):
            prost.append(p)
        if len(prost) == n:
            if n == 1:
                return prost[0]
            else:
                return prost

# Проверка детерминантным методом с помощью решета Эратосфена
def determ(n):
    sieve = set(range(2, int(m.sqrt(n))+1))
    arr_prime = []
    while sieve:
        prime = min(sieve)
        sieve -= set(range(prime, int(m.sqrt(n))+1, prime))
        arr_prime.append(prime)
    for i in range(len(arr_prime)):
        if n % arr_prime[i] == 0:
            return -1
    return 1

# Проверка детерминантным методом с помощью пробного деления
def determ0(n):
    for i in range(2, int(m.sqrt(n))+1):
        if n%i == 0:
            return -1
    return 1

# Генерация комбинарным методом
# k - размерность (бит)
def gen_komb(k):
    t = 2 # Кол-во множителей в произведении
    z = 5 # Число генерируемых псевдопростых чисел 
    psevd = gen_ver(k//t,z) # Генерация псевдослучайных чисел
    # Проверка детерминантным методом на простоту и редактирование списка
    for i in range(z):
        if determ(psevd[i]) == -1:
            psevd.pop(i)
            c = psevd[0]
            while c in psevd:
                c = gen_ver(k//t,1)
            psevd.append(c)
            i = i - 1
    # Генерация простого числа
    for i in range(z-t):
        p = 2
        for j in range(i,i+t):
            p = p*psevd[j]
        # Проверка
        if determ(p+1) == 1:
            return [p+1, psevd[i:i+t]]
    return [0,0]

# Генерация по ГОСТу
def GOST(k):
    # Генерация массива t (длины прмежуточных простых чисел)
    t = []
    t.append(k)
    while t[len(t)-1] > 6:
        if t[len(t)-1] % 2 == 0:
            t.append(int(t[len(t)-1]/2))
        else:
            t.append(int(t[len(t)-1]/2)+1)
    # Генерация случайного числа заданного размера
    p = 6
    while determ0(p) == -1:
        z = t[len(t)-1] + 1 
        p = int((2**(z-1)) + (2**z - 2**(z-1))*r.random()) 
    i = 0
    # Последовательная генерация простых чисел
    while p < 2**(k-1):
        N = 1
        q = p*N + 1 # По теореме
        if i == len(t)-1:
            break
        while (N % 2 == 1):
            z = t[-2-i] - (len(str(bin(q)[2:]))) # Проверка длины
            N = int((2**(z-1)) + (2**z - 2**(z-1))*r.random()) # Задание N
        q = p*N + 1
        # Увеличение N
        while (len(str(bin(q)[2:])) < t[-1-i]):
            N += 2
        # Проверка условий теоремы
        while (pow(2,p*N,q) != 1) and (pow(2,N,q) == 1):
            N += 2
            q = p*N + 1
        p = q
        i += 1
        # Проверка размера
        if q > 2**(int(k)+1):
            break
    return p

def euler_gen(k):
    t = 4 # Кол-во множителей
    z = 10 # Размерность
    psevd = []
    # Генерация детерминированным методом
    for i in range(z):
        psevd.append(int((2**(k//t)) + (2**(k//t + 1) - 2**((k//t)))*r.random()))
        while determ0(psevd[i]) == -1:
            psevd[i] = int((2**(k//t)) + (2**(k//t + 1) - 2**((k//t)))*r.random())
    # Комбинирование множителей
    for i in range(z-t):
        P = 2 
        for j in range(i,i+t):
            P = P*psevd[j]
        p = P + 1 # Вычисление случайного числа
        # Проверка на простоту вероятностными методами
        for i in range(10):
            x = int(2+(m.sqrt(p)-2)*r.random())
            b = int(x**2)
            if (pow(b,(p-1), p) == 1): # Тест Ферма
                for l in range(i,i+t):
                    y = psevd[l]
                    if (pow(b,int((p-1)/y),p) == 1): # Тест Соловея-Штрассена
                        break
                    return [p, psevd[i:i+t]]
            else:
                continue
    return [0]
             
# Вывод
while 1==1:
    print('Для генерации псевдослучайного числа вероятностным методом введите 1')
    print('Для генерации псевдослучайного числа комбинированным методом - 2')
    print('Для генерации псевдослучайного числа с изветным разложением функции Эйлера - 3')
    print('Для генерации псевдослучайного числа по ГОСТ Р 34.10-94 - 4')
    #h = int(input())
    h = 1
    if h == 1:
        print('Введите порядок k бит')
        k = int(input())
        n = 2
        print('p = ', gen_ver(k,n)[0])
        print('q = ', gen_ver(k,n)[1])
        print('\n')
    elif h == 2:
        print('Введите порядок k бит')
        k = int(input())
        p = gen_komb(k)
        while p[0] == 0:
            p = gen_komb(k)
        q = gen_komb(k)
        while (q[0] == 0) or (q[0] == p[0]):
            q = gen_komb(k)
        print('p = ', p[0],'= 1 + 2 *',p[1][0], '*',p[1][1])
        print('q = ', q[0],'= 1 + 2 *',q[1][0], '*',q[1][1])
        print('\n')
    elif h == 3:
        print('Введите порядок k бит')
        k = int(input())
        p = euler_gen(k)
        while p[0] == 0:
            p = euler_gen(k)
        q = euler_gen(k)
        while (q[0] == 0) or (q[0] == p[0]):
            q = euler_gen(k)
        print('p = ', p[0],'= 1 + 2 *',p[1][0], '*',p[1][1], '*',p[1][2], '*',p[1][3])
        print('q = ', q[0],'= 1 + 2 *',q[1][0], '*',q[1][1], '*',q[1][2], '*',q[1][3])
        print('\n')
    elif h == 4:
        print('Введите порядок k бит')
        k = int(input())
        p = GOST(k)
        while p == 0:
            p = GOST(k)
        q = GOST(k)
        while (q == 0) or (q == p):
            q = GOST(k)
        print('p = ', p)
        print('q = ', q)
        print('\n')





