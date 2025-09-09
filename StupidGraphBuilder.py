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
        or file_path.endswith('.jpg')
        or file_path.endswith('.jpeg')):
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
    
    running = True
    click = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                click = False
                positions.append(
                    pygame.mouse.get_pos()
                    )
    pygame.quit()
    with open('outputs.txt','w') as f:
        for x, y in positions:
            f.write(str(x)+'\t'+str(y)+'\n')
