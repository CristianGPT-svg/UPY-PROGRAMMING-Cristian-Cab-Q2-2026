import random
import stddraw
from color import Color


def bubble_sort(numbers):
    n = len(numbers)

    for sweep in range(n):
        for pair in range(0, n - 1 - sweep):
            if numbers[pair] > numbers[pair + 1]:
                numbers[pair], numbers[pair + 1] = numbers[pair + 1], numbers[pair]


def insertion_sort(numbers: list[int]) -> list[int]:
    n = len(numbers)
    for i in range(1, n):
        j = i
        while j > 0 and numbers[j - 1] > numbers[j]:
            numbers[j - 1], numbers[j] = numbers[j], numbers[j - 1]
            j -= 1
    return numbers


def selection_sort(numbers):
    n = len(numbers)

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if numbers[j] < numbers[min_index]:
                min_index = j
        numbers[i], numbers[min_index] = numbers[min_index], numbers[i]


def draw_bars(numbers, selected=()):
    stddraw.clear()
    n = len(numbers)
    bar_width = 10.0 / n

    for i, number in enumerate(numbers):
        x = i * bar_width + bar_width / 2
        color = Color(255, 90, 90) if i in selected else Color(70, 130, 220)
        stddraw.setPenColor(color)
        stddraw.filledRectangle(x - bar_width / 2, 0, bar_width * 0.9, number)
    stddraw.show(100)


def bubble_sort_animated(numbers):
    # Config
    stddraw.setXscale(-0.1, 10)
    stddraw.setYscale(-0.5, max(numbers) + 1)
    n = len(numbers)

    for sweep in range(n):
        swapped = False
        for pair in range(0, n - 1 - sweep):
            draw_bars(numbers, selected=(pair, pair + 1))
            if numbers[pair] > numbers[pair + 1]:
                numbers[pair], numbers[pair + 1] = numbers[pair + 1], numbers[pair]
                swapped = True
            draw_bars(numbers, selected=(pair, pair + 1))

        if not swapped:
            break

    draw_bars(numbers)
    stddraw.show()


def insertion_sort_animated(numbers):
    # Config
    stddraw.setXscale(-0.1, 10)
    stddraw.setYscale(-0.5, max(numbers) + 1)
    n = len(numbers)

    for i in range(1, n):
        j = i
        draw_bars(numbers, selected=(j,))
        while j > 0 and numbers[j - 1] > numbers[j]:
            numbers[j - 1], numbers[j] = numbers[j], numbers[j - 1]
            j -= 1
            draw_bars(numbers, selected=(j, j + 1))

    draw_bars(numbers)
    stddraw.show()


def selection_sort_animated(numbers):
    # Config
    stddraw.setXscale(-0.1, 10)
    stddraw.setYscale(-0.5, max(numbers) + 1)
    n = len(numbers)

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            draw_bars(numbers, selected=(i, min_index, j))
            if numbers[j] < numbers[min_index]:
                min_index = j
        numbers[i], numbers[min_index] = numbers[min_index], numbers[i]
        draw_bars(numbers, selected=(i,))

    draw_bars(numbers)
    stddraw.show()


numbers = [random.randint(0, 100) for _ in range(10)]
print(f"Before bubble sort: {numbers}")
bubble_sort_animated(numbers)
print(f"After bubble sort: {numbers}")

numbers = [random.randint(0, 100) for _ in range(10)]
print(f"Before insertion sort: {numbers}")
insertion_sort_animated(numbers)
print(f"After insertion sort: {numbers}")

numbers = [random.randint(0, 100) for _ in range(10)]
print(f"Before selection sort: {numbers}")
selection_sort_animated(numbers)
