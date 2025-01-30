numbers = input("Enter numbers: ")
small = int(numbers[0])

for num in numbers[1:]:
    if int(num) <= small:
        small = int(num)

print("The smallest number is:", small)
