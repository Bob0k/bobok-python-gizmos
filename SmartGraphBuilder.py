import tkinter
from tkinter import filedialog
import pygame
from pygame.locals import *

root = tkinter.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(title = 'Выберете изображение',
                                       filetypes = (('Изображения', '*.png *.jpg *.jpeg'),
                                                    ('Все файлы', '*.*')))

if not (file_path.endswith('.png')
        or file_path.endswith('.PNG')
        or file_path.endswith('.jpg')
        or file_path.endswith('.JPG')
        or file_path.endswith('.jpeg')
        or file_path.endswith('.JPEG')):
    print('Wrong file format')
else:
    print("Selected file:", file_path)

    image = pygame.image.load(file_path)
    
    pygame.init()
    
    screen=pygame.display.set_mode(
        image.get_rect().size,
        0,
        32
        )
    screen.blit(
        image,
        (0,0)
        )
    positions = []
    pygame.display.flip()

    x0 = float(input('Please, enter real value of x0\n'))
    x1 = float(input('Please, enter real value of x1\n'))
    y0 = float(input('Please, enter real value of y0\n'))
    y1 = float(input('Please, enter real value of y1\n'))
    
    def get_m_x():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == MOUSEBUTTONDOWN:
                    return pygame.mouse.get_pos()[0]
    def get_m_y():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == MOUSEBUTTONDOWN:
                    click = False
                    return pygame.mouse.get_pos()[1]

    print('Please, click at any point on x0 line:')
    px0 = get_m_x()
    print('Please, click at any point on x1 line:')
    px1 = get_m_x()
    print('Please, click at any point on y0 line:')
    py0 = get_m_y()
    print('Please, click at any point on y1 line:')
    py1 = get_m_y()
    
    running = True
    print('Click on graph points now')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                
                positions.append(
                    ((pygame.mouse.get_pos()[0]-px0)/(px1-px0)*(x1-x0)+x0,
                     (py0-pygame.mouse.get_pos()[1])/(py0-py1)*(y1-y0)+y0)
                    )
                print('Got point ('
                       +str(positions[-1][0])
                       +'; '
                       +str(positions[-1][1])
                       +')'
                       )
    pygame.quit()
    print('Exit successful')
    with open(file_path + 'outputs.txt','w') as f:
        for x, y in positions:
            f.write(str(x)+'\t'+str(y)+'\n')
