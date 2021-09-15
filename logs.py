import datetime
from sys import stdin
import re

#Бинарный поиск нужной даты в отсортированном списке логов
def binary(a,low,top,key):
    if top < low:
        return low
    mid = int((top + low) / 2)
    if key == a[mid]:
        return mid
    elif key < a[mid]:
        return binary(a, low, mid-1, key)
    else:
        return binary(a, mid+1, top, key)

# Поиск значения даты лога, в t окрестности которого содержится ошибок больше, чем e
def critical():
    errors = 0
    it = 0
    pointer = 0
    while (errors < e)&(it <= length-1):
        it_val = logs[it].timestamp()
        pointer_val = logs[pointer].timestamp()
        if it_val - pointer_val  <= t - 1:
            key_0 = logs[pointer] + datetime.timedelta(seconds = t)
            it_old = it
            # Ищем лог со значением времени равном pointer+t за логарифмическое время
            it = binary(logs, pointer, length-1, key_0)
            errors += it - it_old
            if errors > e:
                it -= errors - e
                errors = e
        else:
            key = logs[it] - datetime.timedelta(seconds = t-1)
            pointer_old = pointer
            #Ищем лог со значением it - t
            pointer = binary(logs, pointer, it, key)
            errors -= pointer - pointer_old
    if errors < e:
        return -1
    else:
        return logs[it-1]

# Ввод промежутка времени и допустимого количества ошибок на нем
t, e = tuple(map(int, input().split()))
more = True
logs = []
length = 0
#Стандартный ввод строк логов до EOF
for log in stdin:
    # Поиск шаблонного решения, которое в качестве статуса содержит ERROR
    m = re.search('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ([A-Z]*)',log)
    if m.group(1) == "ERROR":
        # Запись в массив только даты логов с ошибкой
        logs.append(datetime.datetime.strptime(m.group(0), '%Y-%m-%d %H:%M:%S'))
        length += 1
ans = critical()
print(ans)
