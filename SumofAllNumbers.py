TotalSum = 0

for num in range(50, 101):  
    if num % 3 == 0 and num % 5 != 0:  
        TotalSum += num  

print("The sum is:", TotalSum)
