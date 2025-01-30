numbers = [10, 5, 12, 8, 15]  # Example set of numbers

# Assume the first two numbers are the highest and second highest
highest = numbers[0]
second_highest = numbers[1]

for num in numbers:
    if num > highest:
        second_highest = highest
        highest = num
    elif num > second_highest and num != highest:
        second_highest = num

print("The second highest number is:", second_highest)
