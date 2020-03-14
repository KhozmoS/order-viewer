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
FANCY_GREEN = (132, 253, 164)
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


def setTopMessage():
    pygame.display.set_caption("Ordering Visualizer   SPEED: {}  BLOCKS: {}".format(FPS, BLOCKS // 2))


def compare(rect1, rect2):
    if rect1.height < rect2.height:
        return -1
    if rect1.height == rect2.height:
        return 0
    if rect1.height > rect2.height:
        return 1


def listenMainEvents():
    global FPS, BLOCKS
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_i:
                insertion_sort()
                return True
            if event.key == K_b:
                burble_sort()
                return True
            if event.key == K_m:
                merge_sort(0, len(rectangles)-1, [False])
                return True
            if event.key == K_r:
                random_blocks(BLOCKS)
                return True

            if event.key == K_UP and FPS < 10:
                FPS += 1
                setTopMessage()
            if event.key == K_DOWN and FPS > 2:
                FPS -= 1
                setTopMessage()
            if event.key == K_RIGHT and BLOCKS < 100:
                BLOCKS += 2
                setTopMessage()
            if event.key == K_LEFT and BLOCKS > 4:
                BLOCKS -= 2
                setTopMessage()

    return False


# ALGORITHMS
def insertion_sort():
    for i in range(1, len(rectangles)):
        # VISUAL PART
        initialScreen(BLOCKS)

        for j in range(0, len(rectangles)):
            if j == i:
                pygame.draw.rect(windowSurface, DARK_BLUE, rectangles[j])
                rect_colors[j] = DARK_BLUE
            elif j < i:
                pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[j])
                rect_colors[j] = FANCY_GREEN
            else:
                pygame.draw.rect(windowSurface, GOOGLE_BLUE, rectangles[j])
                rect_colors[j] = GOOGLE_BLUE

        pygame.display.update()
        mainClock.tick(FPS)
        # END VISUAL PART
        for j in range(i, 0, -1):
            if compare(rectangles[j], rectangles[j-1]) != -1:
                break
            # SWAP RECTANGLES
            rectangles[j], rectangles[j-1] = rectangles[j-1], rectangles[j]
            rectangles[j].left, rectangles[j-1].left = rectangles[j-1].left, rectangles[j].left

            # VISUAL PART
            initialScreen(BLOCKS)

            for k in range(0, len(rectangles)):
                if k == (j-1):
                    pygame.draw.rect(windowSurface, DARK_BLUE, rectangles[k])
                    rect_colors[k] = DARK_BLUE
                elif k <= i:
                    pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[k])
                    rect_colors[k] = FANCY_GREEN
                else:
                    pygame.draw.rect(windowSurface, GOOGLE_BLUE, rectangles[k])
                    rect_colors[k] = GOOGLE_BLUE

            pygame.display.update()
            mainClock.tick(FPS)
            # END VISUAL PART

            # LISTENING IF THE USER PRESS ANY KEY
            if listenMainEvents():
                # IF ANY OTHER EVEN WAS ACTIVATED, JUST TERMINATE CURRENT ACTION
                return
    for i in range(len(rectangles)):
        pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[i])
        rect_colors[i] = FANCY_GREEN


def burble_sort():
    for i in range(1, len(rectangles)):
        for j in range(0, len(rectangles)-i):
            # VISUAL PART
            initialScreen(BLOCKS)
            for k in range(0, len(rectangles)):
                if k == j or k == j+1:
                    pygame.draw.rect(windowSurface, DARK_BLUE, rectangles[k])
                    rect_colors[k] = DARK_BLUE
                elif k > len(rectangles)-i:
                    pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[k])
                    rect_colors[k] = FANCY_GREEN
                else:
                    pygame.draw.rect(windowSurface, GOOGLE_BLUE, rectangles[k])
                    rect_colors[k] = GOOGLE_BLUE
            pygame.display.update()
            mainClock.tick(FPS)
            # END VISUAL PART

            if compare(rectangles[j], rectangles[j+1]) == 1:
                # SWAP RECTANGLES
                rectangles[j], rectangles[j + 1] = rectangles[j + 1], rectangles[j]
                rectangles[j].left, rectangles[j + 1].left = rectangles[j + 1].left, rectangles[j].left

            # VISUAL PART
            initialScreen(BLOCKS)
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
            pygame.display.update()
            mainClock.tick(FPS)
            # END VISUAL PART

            if listenMainEvents():
                return
    for i in range(len(rectangles)):
        pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[i])
        rect_colors[i] = FANCY_GREEN


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
    if low >= hig or stop[0]:
        return
    mid = (low+hig)//2
    merge_sort(low, mid, stop)
    merge_sort(mid+1, hig, stop)

    if listenMainEvents() or stop[0]:
        stop[0] = True
        return
    # VISUAL PART
    initialScreen(BLOCKS)
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

    # MERGING LEFT AND RIGHT PART
    merge(low, mid, hig)

    # VISUAL PART
    initialScreen(BLOCKS)
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

    if hig-low+1 == len(rectangles):
        for i in range(len(rectangles)):
            pygame.draw.rect(windowSurface, FANCY_GREEN, rectangles[i])
            rect_colors[i] = FANCY_GREEN


# END MERGE SORT ALGORITHM

# END ALGORITHMS


def initialScreen(blocks):
    global SQUARESIDE
    SQUARESIDE = WINDOWWIDTH / blocks
    pygame.draw.rect(windowSurface, WHITE, (0, 0, WINDOWWIDTH, WINDOWWIDTH))
    for i in range(len(rectangles)):
        pygame.draw.rect(windowSurface, rect_colors[i], rectangles[i])
    pygame.display.update()
    # ORDERED BLOCKS


def random_blocks(blocks):
    global rectangles, rect_colors
    rectangles, rect_colors = [], []

    initialScreen(BLOCKS)
    for i in range(1, blocks, 2):
        h = random.randint(1, blocks)
        rectangles.append(pygame.Rect(i * SQUARESIDE, WINDOWWIDTH - h*SQUARESIDE, SQUARESIDE, h*SQUARESIDE))
        rect_colors.append(GOOGLE_BLUE)
        assert (WINDOWWIDTH - h*SQUARESIDE >= 0), "Altura del rectangulo sobresale la pantalla"
        pygame.draw.rect(windowSurface, rect_colors[-1], rectangles[-1])
    pygame.display.update()


def showMainScreen():
    """
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
    # while True:


def fillDownSection():
    # LEFT SECTION
    basicFont = pygame.font.SysFont("arial", 15, False)
    textInsertion = basicFont.render("press i: Insertion Sort", True, WHITE, GRAY)
    textRectInsertion = textInsertion.get_rect()
    textRectInsertion.top = WINDOWWIDTH + 5
    textRectInsertion.left = 5
    windowSurface.blit(textInsertion, textRectInsertion)

    textBubleSort = basicFont.render("press b: Bubble Sort", True, WHITE, GRAY)
    textRectBubble = textBubleSort.get_rect()
    textRectBubble.top = textRectInsertion.bottom + 2
    textRectBubble.left = 5
    windowSurface.blit(textBubleSort, textRectBubble)

    textMergeSort = basicFont.render("press m: Merge Sort", True, WHITE, GRAY)
    textRectMerge = textMergeSort.get_rect()
    textRectMerge.top = textRectBubble.bottom + 2
    textRectMerge.left = 5
    windowSurface.blit(textMergeSort, textRectMerge)

    # RIGHT SECTION
    basicFont = pygame.font.SysFont("arial", 15, False)
    text = basicFont.render("press r: Restart", True, WHITE, GRAY)
    textRect = text.get_rect()
    textRect.top = WINDOWWIDTH + 5
    textRect.left = (WINDOWWIDTH // 2)-(WINDOWWIDTH // 8)
    windowSurface.blit(text, textRect)
    # IMAGE CONTROLS
    img_rect = pygame.Rect((WINDOWWIDTH-controls_IMG_WIDTH), WINDOWWIDTH,  controls_IMG_WIDTH, WINDOWHEIGHT-WINDOWWIDTH)
    windowSurface.blit(controls_IMG, img_rect)
    random_blocks(BLOCKS)


def main():
    windowSurface.fill(GRAY)
    pygame.display.update()
    fillDownSection()
    while True:
        # print(len(rectangles))
        listenMainEvents()
        initialScreen(BLOCKS)


if __name__ == '__main__':
    setTopMessage()
    main()

