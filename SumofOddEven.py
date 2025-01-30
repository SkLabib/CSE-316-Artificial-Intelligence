numbers = input("Enter numbers: ")
odd = 0
even = 0

for num in numbers:
    num = int(num) 
    if num % 2 == 0:
        even += num
    else:
        odd += num

print("Sum of odd numbers:", odd)
print("Sum of even numbers:", even)
