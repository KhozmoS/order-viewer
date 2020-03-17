import pygame, sys, random, os
from pygame.locals import *

# CONSTANTS

# COLORS
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 0, 100)
DARK_BLUE = (48, 80, 132)
GOOGLE_BLUE = (66, 133, 244)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FANCY_GREEN = (69, 241, 115)
FANCY_PURPLE = (255, 69, 239)
# END COLORS

# GAME CONST
WINDOWWIDTH = 500
WINDOWHEIGHT = 650
SQUARESIDE = -1
BLOCKS = 50
FPS = 5
# END GAME CONST

# END CONSTANTS

mainClock = pygame.time.Clock()
pygame.init()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
rectangles = []
rect_colors = []
controls_IMG = pygame.image.load(os.path.join('assets', 'controls.png'))
controls_IMG_WIDTH = WINDOWWIDTH-((WINDOWWIDTH//2)+(WINDOWWIDTH // 6))
controls_IMG = pygame.transform.scale(controls_IMG, (controls_IMG_WIDTH, WINDOWHEIGHT-WINDOWWIDTH))


def set_top_message():
    pygame.display.set_caption("Sort Visualizer  SPEED: {}  BLOCKS: {}".format(FPS, BLOCKS // 2))


def compare(rect1, rect2):
    if rect1.height < rect2.height:
        return -1
    if rect1.height == rect2.height:
        return 0
    if rect1.height > rect2.height:
        return 1


def listen_main_events():
    global FPS, BLOCKS
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_i:
                fill_down_section(K_i)
                insertion_sort()
                return True
            if event.key == K_b:
                fill_down_section(K_b)
                burble_sort()
                return True
            if event.key == K_m:
                fill_down_section(K_m)
                merge_sort(0, len(rectangles)-1, [False])
                return True
            if event.key == K_s:
                fill_down_section(K_s)
                selection_sort()
                return True
            if event.key == K_r:
                fill_down_section(K_r)
                random_blocks(BLOCKS)
                return True

            if event.key == K_UP and FPS < 10:
                FPS += 1
                set_top_message()
            if event.key == K_DOWN and FPS > 2:
                FPS -= 1
                set_top_message()
            if event.key == K_RIGHT and BLOCKS < 100:
                BLOCKS += 2
                set_top_message()
            if event.key == K_LEFT and BLOCKS > 4:
                BLOCKS -= 2
                set_top_message()

    return False


def swap_rectangles(a, b):
    goal_a = rectangles[b].left
    goal_b = rectangles[a].left
    swap_speed = 1
    for _ in range((goal_a-goal_b+1)):
        rectangles[a].left += swap_speed
        rectangles[b].left -= swap_speed
        update_screen(BLOCKS)
        mainClock.tick(400)
    rectangles[a], rectangles[b] = rectangles[b], rectangles[a]
    rectangles[a].left, rectangles[b].left = goal_b, goal_a
    update_screen(BLOCKS)


# ALGORITHMS
def insertion_sort():

    def visual_part(i, j=-1):
        # VISUAL PART
        # EVERYONE LOWER THAN i WILL BE GREEN, EXCEPT j IF EXIST
        for k in range(0, len(rectangles)):
            if k == j-1:
                pygame.draw.rect(windowSurface, DARK_BLUE, rectangles[k])
                rect_colors[k] = DARK_BLUE
            elif k <= i:
                pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[k])
                rect_colors[k] = FANCY_GREEN
            else:
                pygame.draw.rect(windowSurface, GOOGLE_BLUE, rectangles[k])
                rect_colors[k] = GOOGLE_BLUE
        update_screen(BLOCKS)
        mainClock.tick(FPS)
        # END VISUAL PART

    for i in range(1, len(rectangles)):
        visual_part(i)
        for j in range(i, 0, -1):
            if compare(rectangles[j], rectangles[j-1]) != -1:
                break
            # SWAP RECTANGLES
            swap_rectangles(j-1, j)
            visual_part(i, j)
            # LISTENING IF THE USER PRESS ANY KEY
            if listen_main_events():
                # IF ANY OTHER EVEN WAS ACTIVATED, JUST TERMINATE CURRENT ACTION
                return
    all_green()


def burble_sort():
    def visual_part(i, j):
        # VISUAL PART
        for k in range(0, len(rectangles)):
            if k == j or k == j + 1:
                pygame.draw.rect(windowSurface, DARK_BLUE, rectangles[k])
                rect_colors[k] = DARK_BLUE
            elif k > len(rectangles) - i:
                pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[k])
                rect_colors[k] = FANCY_GREEN
            else:
                pygame.draw.rect(windowSurface, GOOGLE_BLUE, rectangles[k])
                rect_colors[k] = GOOGLE_BLUE
        update_screen(BLOCKS)
        mainClock.tick(FPS)
        # END VISUAL PART
    for i in range(1, len(rectangles)):
        for j in range(0, len(rectangles)-i):
            visual_part(i, j)

            if compare(rectangles[j], rectangles[j+1]) == 1:
                # SWAP RECTANGLES
                swap_rectangles(j, j+1)

            visual_part(i, j)

            if listen_main_events():
                return
    all_green()


def selection_sort():
    def visual_part(i, j):
        # VISUAL PART
        for k in range(len(rectangles)):
            if k < i:
                pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[k])
                rect_colors[k] = FANCY_GREEN
            elif k == pos:
                pygame.draw.rect(windowSurface, FANCY_PURPLE, rectangles[k])
                rect_colors[k] = FANCY_PURPLE
            elif k == j:
                pygame.draw.rect(windowSurface, DARK_BLUE, rectangles[k])
                rect_colors[k] = DARK_BLUE
            else:
                pygame.draw.rect(windowSurface, GOOGLE_BLUE, rectangles[k])
                rect_colors[k] = GOOGLE_BLUE
        update_screen(BLOCKS)
        mainClock.tick(FPS)
        # END VISUAL PART

    for i in range(len(rectangles)):
        pos = i
        for j in range(i, len(rectangles)):
            if listen_main_events():
                return

            visual_part(i, j)

            if listen_main_events():
                return

            if compare(rectangles[j], rectangles[pos]) == -1:
                pos = j

            visual_part(i, j)
        # SWAP
        swap_rectangles(i, pos)
        # END SWAP
    all_green()


# MERGE SORT ALGORITHM
def merge(low, mid, hig):
    tmp = low
    hi_tmp = mid+1
    lo_tmp = low
    copy = rectangles[:]

    while lo_tmp <= mid or hi_tmp <= hig:
        if lo_tmp > mid:
            rectangles[tmp] = pygame.Rect(copy[hi_tmp])
            rectangles[tmp].left = pygame.Rect(copy[tmp]).left
            hi_tmp += 1
            tmp += 1
        elif hi_tmp > hig:
            rectangles[tmp] = pygame.Rect(copy[lo_tmp])
            rectangles[tmp].left = pygame.Rect(copy[tmp]).left
            lo_tmp += 1
            tmp += 1
        else:
            if compare(copy[lo_tmp], copy[hi_tmp]) == -1:
                rectangles[tmp] = pygame.Rect(copy[lo_tmp])
                rectangles[tmp].left = pygame.Rect(copy[tmp]).left
                lo_tmp += 1
                tmp += 1
            else:
                rectangles[tmp] = pygame.Rect(copy[hi_tmp])
                rectangles[tmp].left = pygame.Rect(copy[tmp]).left
                hi_tmp += 1
                tmp += 1
    del copy


# THE STOP PARAMETER, JUST STOP ALL THE ALGORITHM
# WHEN HIS ELEMENT IS TRUE, THAT'S POSSIBLE CAUSE IT'S MUTABLE
def merge_sort(low, hig, stop):
    def visual_part():
        # VISUAL PART
        update_screen(BLOCKS)
        for i in range(0, len(rectangles)):
            if low <= i <= hig:
                pygame.draw.rect(windowSurface, DARK_BLUE, rectangles[i])
                rect_colors[i] = DARK_BLUE
            else:
                pygame.draw.rect(windowSurface, GOOGLE_BLUE, rectangles[i])
                rect_colors[i] = GOOGLE_BLUE
        pygame.display.update()
        mainClock.tick(FPS)
        # END VISUAL PART

    if low >= hig or stop[0]:
        return
    mid = (low+hig)//2
    merge_sort(low, mid, stop)
    merge_sort(mid+1, hig, stop)

    if listen_main_events() or stop[0]:
        stop[0] = True
        return
    visual_part()
    # MERGING LEFT AND RIGHT PART
    merge(low, mid, hig)

    visual_part()

    if hig-low+1 == len(rectangles):
        all_green()


# END MERGE SORT ALGORITHM

# END ALGORITHMS

def all_green():
    for i in range(len(rectangles)):
        pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[i])
        rect_colors[i] = FANCY_GREEN
    pygame.display.update()


def update_screen(blocks):
    global SQUARESIDE
    SQUARESIDE = WINDOWWIDTH / blocks
    pygame.draw.rect(windowSurface, WHITE, (0, 0, WINDOWWIDTH, WINDOWWIDTH))
    for i in range(len(rectangles)):
        pygame.draw.rect(windowSurface, rect_colors[i], rectangles[i])
    pygame.display.update()


def random_blocks(blocks):
    global rectangles, rect_colors
    rectangles, rect_colors = [], []

    def rectangles_fall():
        fall_speed = 2
        iterations = 0
        magic_constant = 20
        while rectangles[-1].bottom < WINDOWWIDTH:
            for i in range(len(rectangles)):
                if iterations >= i * magic_constant and rectangles[i].bottom < WINDOWWIDTH:
                    rectangles[i].top += fall_speed
            iterations += 1
            update_screen(BLOCKS)
            mainClock.tick(1000)
        for rect in rectangles:
            rect.bottom = WINDOWWIDTH
    update_screen(BLOCKS)
    for i in range(1, blocks, 2):
        h = random.randint(1, blocks)
        rectangles.append(pygame.Rect(i * SQUARESIDE, # WIDTH
                                      (-h*SQUARESIDE if WINDOWWIDTH - h * SQUARESIDE >= 0 # IF ELSE TO SELECT THE HEIGHT
                                       else WINDOWWIDTH), SQUARESIDE, h*SQUARESIDE))
        rect_colors.append(GOOGLE_BLUE)
    rectangles_fall()
    pygame.display.update()

"""
def showMainScreen():
    # SHOWING PRINCIPAL MESSAGE
    pygame.draw.rect(windowSurface, WHITE, (0, 0, WINDOWWIDTH, WINDOWWIDTH))
    basicFont = pygame.font.SysFont("monospace", 25, False)
    text = basicFont.render("Pick one of the options below", True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery-(WINDOWWIDTH//7)
    windowSurface.blit(text, textRect)
    pygame.display.update()
    # END SHOWING    
"""


def fill_down_section(key_pressed=None):
    # LEFT SECTION
    basicFont = pygame.font.SysFont("monospace", 12, False)

    textAlgo = basicFont.render("Algorithms", True, WHITE, GRAY)
    textRectAlgo = textAlgo.get_rect()
    textRectAlgo.top = WINDOWWIDTH + 5
    textRectAlgo.left = 5
    # ALGORITHM UNDERLINE
    pygame.draw.line(windowSurface, WHITE, (textRectAlgo.left, textRectAlgo.bottom),
                                           (textRectAlgo.right, textRectAlgo.bottom))
    windowSurface.blit(textAlgo, textRectAlgo)

    textInsertion = basicFont.render("press i: Insertion Sort", True,
                                     (FANCY_GREEN if K_i == key_pressed else WHITE), GRAY)
    textRectInsertion = textInsertion.get_rect()
    textRectInsertion.top = textRectAlgo.bottom + 5
    textRectInsertion.left = 5
    windowSurface.blit(textInsertion, textRectInsertion)

    textBubleSort = basicFont.render("press b: Bubble Sort", True,
                                     (FANCY_GREEN if K_b == key_pressed else WHITE), GRAY)
    textRectBubble = textBubleSort.get_rect()
    textRectBubble.top = textRectInsertion.bottom + 2
    textRectBubble.left = 5
    windowSurface.blit(textBubleSort, textRectBubble)

    textSelectionSort = basicFont.render("press s: Selection Sort", True,
                                         (FANCY_GREEN if K_s == key_pressed else WHITE), GRAY)
    textRectSelection = textSelectionSort.get_rect()
    textRectSelection.top = textRectBubble.bottom + 2
    textRectSelection.left = 5
    windowSurface.blit(textSelectionSort, textRectSelection)

    textMergeSort = basicFont.render("press m: Merge Sort", True,
                                     (FANCY_GREEN if K_m == key_pressed else WHITE), GRAY)
    textRectMerge = textMergeSort.get_rect()
    textRectMerge.top = textRectSelection.bottom + 2
    textRectMerge.left = 5
    windowSurface.blit(textMergeSort, textRectMerge)

    # RIGHT SECTION
    textOptions = basicFont.render("Options", True, WHITE, GRAY)
    textRectOptions = textOptions.get_rect()
    textRectOptions.top = WINDOWWIDTH + 5
    textRectOptions.left = (WINDOWWIDTH // 2)-(WINDOWWIDTH // 8)
    # OPTIONS UNDERLINE
    pygame.draw.line(windowSurface, WHITE, (textRectOptions.left, textRectOptions.bottom),
                     (textRectOptions.right, textRectOptions.bottom))
    windowSurface.blit(textOptions, textRectOptions)

    text = basicFont.render("press r: Restart", True, WHITE, GRAY)
    textRect = text.get_rect()
    textRect.top = textRectOptions.bottom + 5
    textRect.left = textRectOptions.left
    windowSurface.blit(text, textRect)

    textEsc = basicFont.render("press esc: Quit", True, WHITE, GRAY)
    textRectEsc = textEsc.get_rect()
    textRectEsc.top = textRect.bottom + 2
    textRectEsc.left = textRect.left
    windowSurface.blit(textEsc, textRectEsc)
    # IMAGE CONTROLS
    img_rect = pygame.Rect((WINDOWWIDTH-controls_IMG_WIDTH), WINDOWWIDTH,  controls_IMG_WIDTH, WINDOWHEIGHT-WINDOWWIDTH)
    windowSurface.blit(controls_IMG, img_rect)


def main():
    windowSurface.fill(GRAY)
    pygame.display.update()
    fill_down_section()
    random_blocks(BLOCKS)
    while True:
        listen_main_events()
        update_screen(BLOCKS)


if __name__ == '__main__':
    set_top_message()
    main()

