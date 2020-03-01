#!/usr/bin/python3

def calc3(arr):
	summa = 0;
	arr2 = []
	for e in arr:
		summa += e;
		arr2.append(e*2)	
	return (summa, summa/len(arr), arr2)
		
arr = [1, 2, 3, 4, 5, 6]

print('Входной массив')
print(arr)

(summa, avg, arr2) = calc3(arr)

print('Результат')
print(summa)
print(avg)
print(arr2)
