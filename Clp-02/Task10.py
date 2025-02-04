import matplotlib.pyplot as plt
regions = ['Dhaka', 'Rajshahi', 'Sylhet', 'Chattogram']
sales_revenue = [50000, 70000, 60000, 55000]
plt.bar(regions, sales_revenue, color=['red', 'green', 'blue', 'orange'])
plt.title('Sales Revenue Comparison Across District')
plt.xlabel('District')
plt.ylabel('Sales Revenue (BD)')
plt.show()
