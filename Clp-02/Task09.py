import matplotlib.pyplot as plt
days = [ 'Saturday', 'Sunday', 'Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday' ]
temperatures = [18, 25, 21, 14, 23, 26, 20]
plt.plot(days, temperatures, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
plt.title('Temperature Variations Over a Week')
plt.xlabel('Days of the Week')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.show()
