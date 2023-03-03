import cv2
import pygame

alf = 'N@#wD$987654321?!abc;:+=-,._ '


# TODO:
#    settings
#    GUI
#    custom alfabet

def set_alf(stroke):
    global alf
    if len(stroke) > 1:
        alf = stroke
    else:
        print('too small ! needs to be > 1')


# convert light index to char
def to_ask(dens):
    index = round(dens / 255 * (len(alf) - 1))
    return alf[index]


def get_image(source):
    return cv2.imread(source, cv2.IMREAD_GRAYSCALE)


def get_sides_from_scale(image, scale):
    return round(image.shape[1] * scale), round(image.shape[0] * scale)


# algorithm resize image using cv2 and work with new image
def algo1(image, re_h, re_w):
    def resize(orig_image, h, w):
        f = w / orig_image.shape[0]
        new_w = int(orig_image.shape[1] * f)
        new_h = int(orig_image.shape[0] * f)
        resized = cv2.resize(orig_image, (new_w, new_h), cv2.INTER_CUBIC)
        return resized

    resized = resize(image, re_h, re_w)
    resized = cv2.transpose(resized)

    w = resized.shape[0]
    h = resized.shape[1]

    ascii_image = []

    for i in range(h):
        ascii_image.append(''.join([to_ask(resized[j][i]) for j in range(w)]) + '\n')

    return ascii_image


# algorithm divide image to chunk and fill incomplete chunks (mode chunks) with 0
def algo2(image, re_h, re_w):
    image = image.transpose()

    # return all pixels lights from chunck
    def dots(image, x, y, chunk_x, chunk_y):
        return [image[x + i][y + j] for i in range(chunk_x) for j in range(chunk_y)]

    # calculate average light
    def calc(dots, add=0):
        mean = sum(dots) / (len(dots) + add)
        return mean

    w = image.shape[0]
    h = image.shape[1]
    # sides of pixels chunk
    chunk_x = round(w / re_w)
    chunk_y = round(h / re_h)
    # count of full chunk
    full_chunk_x = w // chunk_x - 1
    full_chunk_y = h // chunk_y - 1
    # mode chunk
    mode_x = w % chunk_x
    mode_y = h % chunk_y
    ascii_image = []

    for i in range(full_chunk_y):
        row = ''
        for j in range(full_chunk_x):
            dense = calc(dots(image, chunk_x * j, chunk_y * i, chunk_x, chunk_y))
            row += to_ask(dense)
        if mode_x != 0:
            dense = calc(dots(image, chunk_x * full_chunk_x, (chunk_y * full_chunk_y), mode_x, chunk_y),
                         add=(chunk_x - mode_x) * chunk_y)
            row += to_ask(dense)

        ascii_image.append(row + '\n')
    if mode_y != 0:
        row = ''
        for j in range(full_chunk_x):
            dense = calc(dots(image, chunk_x * j, chunk_y * full_chunk_y, chunk_x, mode_y),
                         add=(chunk_y - mode_y) * chunk_x)
            row += to_ask(dense)
        if mode_x != 0:
            dense = calc(dots(image, chunk_x * full_chunk_x, chunk_y * full_chunk_y, mode_x, chunk_y),
                         add=(chunk_x - mode_x) * mode_y + (mode_y * chunk_x))
            row += to_ask(dense)
        ascii_image.append(row + '\n')

    return ascii_image


# write image to file
def to_file(res, name):
    with open(f'{name}.txt', 'w') as f:
        for line in res:
            f.write(line)


# draw a pygame ascii
def to_pygame(res, name, font_size=10):
    pygame.init()
    pygame.font.init()

    font_h = round(font_size * 0.8)
    font_w = round(font_size * 0.8)

    font = pygame.font.SysFont('PT Serif', font_size)

    screen = pygame.display.set_mode((len(res[0]) * font_w + 2, len(res) * font_h))
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()

    for i in range(len(res)):
        ofset_w = 2
        for j in range(len(res[i])):
            if res[i][j] == ' ':
                ofset_w += font_w
            else:
                text = font.render(res[i][j], False, (0, 0, 0))
                screen.blit(text, (ofset_w + j * font_w, font_h * i))

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

    pygame.image.save(screen, name)
    print('was saved to ' + name)
