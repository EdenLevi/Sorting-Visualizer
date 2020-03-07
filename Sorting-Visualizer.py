import random
import pygame
import math
import time

pygame.init()

win = pygame.display.set_mode((800, 630))
pygame.display.set_caption("Sorting Algorithm Visualizer")
pygame.draw.rect(win, (0, 0, 20), (0, 0, 800, 630))

elapsed_time, start_time = 0, 0

pygame.font.init()
arial14 = pygame.font.SysFont('Arial', 14)
arial12 = pygame.font.SysFont('Arial', 12)
impact20 = pygame.font.SysFont('Impact', 24)

circle_pos = [
    (15, 535),
    (15, 555),
    (15, 575),
    (15, 595),
    (15, 615),

    (105, 535),
    (105, 555),
    (105, 575),
    (105, 595),
    (105, 615),

    (200, 535),
    (200, 555),
    (200, 575),
    (200, 595),
    (200, 615)
]

button_pos = [
    (400, 530, 100, 50),
    (600, 530, 100, 50)
]

mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

array_size = 40  # default, 100 = huge, 80 = big, 40 = medium, 20 = small, 10 = very small
sort_speed = 2  # 0 = instant, 1 = fast, 2 = normal, 3 = slow, 4 = very slow
algorithm = 0  # 0 = Bubble Sort, 1 = Selection Sort, 2 = Quick Sort, 3 = Merge Sort, 4 = Heap Sort

line_width = int(round((800 - (array_size - 1) * 5 - 2 - 5) / array_size))
print("The width of every line should be: " + str(line_width) + " pixels.")

vet = []
while len(vet) < array_size:
    r = random.randint(10, 500)
    if r not in vet:
        vet.append(r)

color_dark_blue = (0, 0, 30)
color_blue = (75, 122, 230)
color_light_blue = (105, 152, 255)
color_green = (75, 229, 137)
color_red = (229, 42, 60)
color_purple = (200, 0, 200)
colors = [color_blue for _ in range(array_size)]

r_pressed = False
s_pressed = False

merge_index = 0


def draw_lines():
    line_x = 2
    index = 0
    for line in vet:
        pygame.draw.rect(win, colors[index], (line_x, 500, line_width, line - 500))
        line_x += line_width + 5
        index += 1
    pygame.display.update()


def clear_screen():
    pygame.draw.rect(win, (0, 0, 20), (0, 0, 800, 501))


def refresh_lines():
    clear_screen()
    global vet, line_width, colors
    vet = []
    while len(vet) < array_size:
        r2 = random.randint(10, 500)
        if r2 not in vet:
            vet.append(r2)
    line_width = int(round((800 - (array_size - 1) * 5 - 2 - 5) / array_size))
    colors = [color_blue for _ in range(array_size)]
    for i2 in range(0, len(colors)):
        colors[i2] = color_blue
    draw_lines()


def swap_pos(pos1, pos2):
    global vet
    vet[pos1], vet[pos2] = vet[pos2], vet[pos1]


def slow_down():
    if sort_speed == 2:
        pygame.time.delay(5)
    if sort_speed == 3:
        pygame.time.delay(20)
    if sort_speed == 4:
        pygame.time.delay(100)


def show_off():
    vet2 = vet.copy()
    vet2.sort(reverse=True)
    if vet == vet2:
        for index in range(len(vet)):
            pygame.event.get()
            set_line_color(index, color_blue)
            slow_down()
        for index in range(len(vet)):
            pygame.event.get()
            if index+1 < len(vet):
                set_line_color(index+1, color_purple)
            set_line_color(index, color_purple)
            slow_down()
            set_line_color(index, color_green)


def sort():
    global start_time
    start_time = time.time()
    if sort_speed == 0:
        vet.sort(reverse=True)
        for i2 in range(0, len(colors)):
            colors[i2] = color_green
        clear_screen()
        draw_lines()
        return
    if algorithm == 0:
        bubble_sort()
    elif algorithm == 1:
        selection_sort()
    elif algorithm == 2:
        quick_sort(vet, 0, len(vet)-1)
    elif algorithm == 3:
        merge_sort(vet, 0, len(vet)-1)
    elif algorithm == 4:
        heap_sort(vet)
    start_time = 0
    if algorithm != 3:
        show_off()


def bubble_sort():
    for i in range(len(vet) - 1, -1, -1):
        for j in range(i):
            pygame.event.get()
            set_line_color(j, color_red)
            set_line_color(j + 1, color_red)
            slow_down()
            if vet[j] < vet[j + 1]:
                swap_pos(j, j + 1)
                clear_screen()
                draw_lines()
            set_line_color(j, color_blue)
            set_line_color(j + 1, color_blue)
            draw_timer()
        set_line_color(i, color_purple)


def selection_sort():
    for i in range(len(vet) - 1, -1, -1):
        max_index = 0
        for j in range(i + 1):
            pygame.event.get()
            set_line_color(j, color_red)
            slow_down()
            if vet[j] < vet[max_index] or j == 0:
                set_line_color(max_index, color_blue)
                max_index = j
                set_line_color(max_index, (200, 200, 255))
            else:
                set_line_color(j, color_blue)
            draw_timer()
        set_line_color(max_index, color_blue)
        swap_pos(i, max_index)
        set_line_color(i, color_purple)
        clear_screen()
        draw_lines()


def quick_sort(array, low, high):
    if low < high:
        q = quick(array, low, high)
        quick_sort(array, low, q - 1)
        quick_sort(array, q + 1, high)
    clear_screen()
    draw_lines()


def quick(array, low, high):
    i = low-1
    pivot = array[high]
    for j in range(low, high):
        set_line_color(j, color_red)
        set_line_color(i+1, color_red)
        draw_timer()
        slow_down()
        if array[j] >= pivot:
            i = i + 1
            set_line_color(i, color_blue)
            swap_pos(i, j)
        set_line_color(i+1, color_blue)
        set_line_color(j, color_blue)
        clear_screen()
        draw_lines()
    swap_pos(i+1, high)
    set_line_color(i+1, color_purple)
    return i+1


def merge_sort(array, left, right):
    draw_timer()
    slow_down()
    middle = (left + right) // 2
    if left < right:
        merge_sort(array, left, middle)
        merge_sort(array, middle + 1, right)
        merge(array, left, middle, middle + 1, right)


def merge(array, left, middle, middle2, right):
    i, j = left, middle2
    temp = []
    pygame.event.get()
    while i <= middle and j <= right:
        set_line_color(i, color_red)
        set_line_color(j, color_red)
        clear_screen()
        draw_lines()
        slow_down()
        draw_timer()
        set_line_color(i, color_blue)
        set_line_color(j, color_blue)
        if array[i] > array[j]:
            temp.append(array[i])
            i += 1
        else:
            temp.append(array[j])
            j += 1
    while i <= middle:
        set_line_color(i, color_red)
        clear_screen()
        draw_lines()
        slow_down()
        draw_timer()
        set_line_color(i, color_blue)
        temp.append(array[i])
        i += 1
    while j <= right:
        set_line_color(j, color_red)
        clear_screen()
        draw_lines()
        slow_down()
        draw_timer()
        set_line_color(j, color_blue)
        temp.append(array[j])
        j += 1
    j = 0
    for i in range(left, right + 1):
        pygame.event.pump()
        array[i] = temp[j]
        j += 1
        set_line_color(i, color_purple)
        clear_screen()
        draw_lines()
        slow_down()
        draw_timer()
        if right - left == len(array) - 2:
            set_line_color(i, color_blue)
        else:
            set_line_color(i, color_green)


def heap_sort(array):
    draw_timer()
    clear_screen()
    draw_lines()

    size = len(array)
    for i in range(size, -1, -1):
        draw_timer()
        max_heapify(array, i, size)

    size -= 1
    while size > 0:
        pygame.event.get()
        set_line_color(0, color_red)
        set_line_color(size, color_red)
        if size+1 < len(array):
            set_line_color(size+1, color_purple)
        draw_timer()
        slow_down()
        slow_down()
        swap_pos(0, size)
        slow_down()
        set_line_color(0, color_blue)
        set_line_color(size, color_blue)
        max_heapify(array, 0, size)
        size -= 1

    clear_screen()
    draw_lines()

    return array


def max_heapify(array, i, size):
    largest = i
    left_child = (i * 2) + 1
    right_child = (i * 2) + 2

    clear_screen()
    draw_lines()

    if left_child < size and array[left_child] < array[largest]:
        largest = left_child
    if right_child < size and array[right_child] < array[largest]:
        largest = right_child

    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        max_heapify(array, largest, size)

    clear_screen()
    draw_lines()


def set_line_color(index, color):
    line_x = 2 + index * (5 + line_width)
    pygame.draw.rect(win, color, (line_x, vet[index] - 1, line_width, 500 - vet[index] + 2))
    pygame.display.update()
    colors[index] = color


def draw_timer():
    global elapsed_time
    pygame.event.get()
    elapsed_time = time.time() - start_time
    pygame.draw.rect(win, (0, 0, 20), (640, 615, 160, 15))
    win.blit(arial12.render('Elapsed time: ' + str(round(elapsed_time, 2)) + ' seconds', False, (255, 255, 255)), (640,
                                                                                                                   615))


def draw_text():
    win.blit(arial14.render('Speed:', False, (255, 255, 255)), (5, 505))  # Speed Title
    win.blit(arial12.render('Instant', False, (255, 255, 255)), (25, 528))  # Speed 0 - Instant
    win.blit(arial12.render('Fast', False, (255, 255, 255)), (25, 548))  # Speed 1 - Fast
    win.blit(arial12.render('Normal', False, (255, 255, 255)), (25, 568))  # Speed 2 - Normal
    win.blit(arial12.render('Slow', False, (255, 255, 255)), (25, 588))  # Speed 3 - Slow
    win.blit(arial12.render('Very slow', False, (255, 255, 255)), (25, 608))  # Speed 4 - Very slow

    win.blit(arial14.render('Array Size:', False, (255, 255, 255)), (95, 505))  # Array Size Title
    win.blit(arial12.render('Huge', False, (255, 255, 255)), (115, 528))  # Size 5 - Huge
    win.blit(arial12.render('Big', False, (255, 255, 255)), (115, 548))  # Size 6 - Big
    win.blit(arial12.render('Medium', False, (255, 255, 255)), (115, 568))  # Size 7 - Medium
    win.blit(arial12.render('Small', False, (255, 255, 255)), (115, 588))  # Size 8 - Small
    win.blit(arial12.render('Very small', False, (255, 255, 255)), (115, 608))  # Size 9 - Very small

    win.blit(arial14.render('Algorithm:', False, (255, 255, 255)), (190, 505))  # Algorithm Title
    win.blit(arial12.render('Bubble Sort', False, (255, 255, 255)), (210, 528))  # Algorithm 10 - Bubble Sort
    win.blit(arial12.render('Selection Sort', False, (255, 255, 255)), (210, 548))  # Algorithm 11 - Selection Sort
    win.blit(arial12.render('Quick Sort', False, (255, 255, 255)), (210, 568))  # Algorithm 12 - Quick Sort
    win.blit(arial12.render('Merge Sort', False, (255, 255, 255)), (210, 588))  # Algorithm 13 - Merge Sort
    win.blit(arial12.render('Heap Sort', False, (255, 255, 255)), (210, 608))  # Algorithm 14 - Heap Sort


def draw_circles():
    for num in range(len(circle_pos)):
        pygame.draw.circle(win, (255, 255, 255), circle_pos[num], 5)  # main circle
        pygame.draw.circle(win, (255, 255, 255), circle_pos[num], 3)  # smaller circle

    if sort_speed == 0:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[0][0], circle_pos[0][1]), 3)
    elif sort_speed == 1:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[1][0], circle_pos[1][1]), 3)
    elif sort_speed == 2:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[2][0], circle_pos[2][1]), 3)
    elif sort_speed == 3:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[3][0], circle_pos[3][1]), 3)
    elif sort_speed == 4:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[4][0], circle_pos[4][1]), 3)

    if array_size == 100:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[5][0], circle_pos[5][1]), 3)
    elif array_size == 80:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[6][0], circle_pos[6][1]), 3)
    elif array_size == 40:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[7][0], circle_pos[7][1]), 3)
    elif array_size == 20:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[8][0], circle_pos[8][1]), 3)
    elif array_size == 10:
        pygame.draw.circle(win, (0, 0, 0), (circle_pos[9][0], circle_pos[9][1]), 3)

    pygame.draw.circle(win, (0, 0, 0), (circle_pos[algorithm+10][0], circle_pos[algorithm+10][1]), 3)

    pygame.display.update()


def check_distance(x, y, x2, y2):
    return math.sqrt((x - x2) ** 2 + (y - y2) ** 2)


def mark_circle():
    global sort_speed, array_size, algorithm
    for num in range(5):  # loop through speed buttons
        if check_distance(mouse_x, mouse_y, int(circle_pos[num][0]), int(circle_pos[num][1])) < 5:
            sort_speed = num
            return num
    for num in range(5):  # loop through speed buttons
        if check_distance(mouse_x, mouse_y, int(circle_pos[num + 5][0]), int(circle_pos[num + 5][1])) < 5:
            if num + 5 == 5:
                array_size = 100
            elif num + 5 == 6:
                array_size = 80
            elif num + 5 == 7:
                array_size = 40
            elif num + 5 == 8:
                array_size = 20
            elif num + 5 == 9:
                array_size = 10
            refresh_lines()
            return num + 5
    for num in range(5):  # loop through algorithm buttons
        if check_distance(mouse_x, mouse_y, int(circle_pos[num + 10][0]), int(circle_pos[num + 10][1])) < 5:
            if num + 10 == 10:
                algorithm = 0
            elif num + 10 == 11:
                algorithm = 1
            elif num + 10 == 12:
                algorithm = 2
            elif num + 10 == 13:
                algorithm = 3
            elif num + 10 == 14:
                algorithm = 4
            return num + 10
    return False


def draw_buttons():
    if mark_button() == 1:
        pygame.draw.rect(win, color_light_blue, button_pos[0])
        pygame.draw.rect(win, color_blue, button_pos[1])
    elif mark_button() == 2:
        pygame.draw.rect(win, color_light_blue, button_pos[1])
        pygame.draw.rect(win, color_blue, button_pos[0])
    else:
        pygame.draw.rect(win, color_blue, button_pos[0])
        pygame.draw.rect(win, color_blue, button_pos[1])
    win.blit(impact20.render('SORT!', False, color_dark_blue),
             (button_pos[0][0] + 20, button_pos[0][1] + 10))  # Button 1
    win.blit(arial12.render('or press s', False, (255, 255, 255)), (button_pos[0][0] + 20, button_pos[0][1] + 55))
    win.blit(impact20.render('REFRESH', False, color_dark_blue),
             (button_pos[1][0] + 10, button_pos[1][1] + 10))  # Button 2
    win.blit(arial12.render('or press r', False, (255, 255, 255)), (button_pos[1][0] + 20, button_pos[1][1] + 55))
    pygame.display.update()


def mark_button():
    global mouse_x, mouse_y
    mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
    for num in range(len(button_pos)):
        if button_pos[num][0] < mouse_x < button_pos[num][0] + button_pos[num][2] and \
                button_pos[num][1] < mouse_y < button_pos[num][1] + button_pos[num][3]:
            return num + 1
    return False


def reset_timer():
    global elapsed_time, start_time
    elapsed_time = 0
    start_time = time.time()
    draw_timer()


draw_buttons()
draw_lines()
draw_text()
draw_circles()
reset_timer()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            draw_buttons()
        if event.type == pygame.MOUSEBUTTONUP:
            pygame.event.get()
            mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            mark_circle()
            draw_circles()
            if mark_button() == 1:  # sort button pressed
                sort()
            elif mark_button() == 2:  # refresh button pressed
                reset_timer()
                refresh_lines()
                clear_screen()
                draw_lines()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and r_pressed is False:
                r_pressed = True
                reset_timer()
                refresh_lines()
                clear_screen()
                draw_lines()
            if event.key == pygame.K_s and s_pressed is False:
                s_pressed = True
                sort()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                r_pressed = False
            if event.key == pygame.K_s:
                s_pressed = False
            if event.key == pygame.K_e:
                e_pressed = False

pygame.quit()
