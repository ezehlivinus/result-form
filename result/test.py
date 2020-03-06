
colours = ('blue', 'red', 'white', 'green', 'brown')
numbers = ('one', 'two', 'three', 'four', 'five', 'six')

grades = {
    'one': colours,
    'two': colours,
    'three': colours,
    'four': colours,
    'five': colours,
    'six': colours
}

for num in numbers:
    for c in colours:
        print((num))
        print(((f'{num} {c}'), (f'{num} {c}')) )



# print(grades)