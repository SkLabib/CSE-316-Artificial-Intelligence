students = (
    ("Labib", 25, 3.80),
    ("Fahim", 29, 3.50),
    ("Rofy", 23, 3.92),
    ("Richi", 20, 3.70)
)

SortedStudents = sorted(students, key=lambda x: x[2])

print(SortedStudents)
