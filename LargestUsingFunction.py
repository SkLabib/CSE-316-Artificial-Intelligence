def FindLargest(a, b):  
    if a > b:  
        return a  
    else:  
        return b  

x = int(input("Enter first number: "))  
y = int(input("Enter second number: "))  

largest = FindLargest(x, y)  
print("The largest number is:", largest)
