import time

print('О чем напомнить? ')
text = str(input())

print('Через сколько минут?')
localTime = float(input())

localTime = localTime * 60
time.sleep(localTime)
print(text)
