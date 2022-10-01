from cgitb import text
import pygame
import helpers as h
import globals as gv
import map as m
import pygame.freetype
import pygame.mouse as mouse
import math


def draw_grid():
    for x in range(0, gv.WINDOW_WIDTH, gv.BLOCK_SIZE):
        for y in range(0, gv.WINDOW_HEIGHT, gv.BLOCK_SIZE):
            rect = pygame.Rect(x, y, gv.BLOCK_SIZE, gv.BLOCK_SIZE)
            pygame.draw.rect(gv.SCREEN, gv.WHITE, rect, 1)


# def generate_terrain():
#     for x in range(0, gv.number_of_x_blocks):
#         for y in range(0, gv.number_of_y_blocks):
#             if (h.randomBoolean(0.15)):
#                 gv.terrainList.append(gv.Node(x, y))
#                 gv.map[x][y] = 1

#     generate_islands()

def generate_islands():
    for x in range(0, gv.number_of_x_blocks):
        for y in range(0, gv.number_of_y_blocks):
            if (gv.map[x][y] == 1):
                if (x > 0):
                    if (h.randomBoolean(0.2)):
                        if (gv.map[x-1][y] == 0):
                            gv.map[x-1][y] = 1
                            gv.terrainList.append(gv.Node(x-1, y))
                if (x < gv.number_of_x_blocks - 1):
                    if (h.randomBoolean(0.2)):
                        if (gv.map[x+1][y] == 0):
                            gv.map[x+1][y] = 1
                            gv.terrainList.append(gv.Node(x+1, y))
                if (y > 0):
                    if (h.randomBoolean(0.2)):
                        if (gv.map[x][y-1] == 0):
                            gv.map[x][y-1] = 1
                            gv.terrainList.append(gv.Node(x, y-1))
                if (y < gv.number_of_y_blocks - 1):
                    if (h.randomBoolean(0.2)):
                        if (gv.map[x][y+1] == 0):
                            gv.map[x][y+1] = 1
                            gv.terrainList.append(gv.Node(x, y+1))

# def mouse_choose_terrain():

#     (b1, _, _) = mouse.get_pressed(num_buttons = 3)

#     if b1:
#         (x, y) = mouse.get_pos()
#         x_pos = round_to_block_size(x)
#         y_pos = round_to_block_size(y)
#         gv.terrainList.append(gv.Node(x_pos,y_pos))
#         gv.map[x_pos][y_pos] = 1
#         h.draw_rectangle(x_pos, y_pos, gv.SCREEN, gv.BLOCK_SIZE, (210, 180, 140))
#         # print("x=", x, "x_pos=", x_pos, "y=", y, "y_pos=", y_pos)


# def mouse_choose_starting_node():
#     (b1, _, _) = mouse.get_pressed(num_buttons = 3)

#     if b1:
#         (x, y) = mouse.get_pos()
#         x_pos = round_to_block_size(x)
#         y_pos = round_to_block_size(y)
#         start = gv.Node(x_pos, y_pos)
#         gv.openList.append(start)
#         h.draw_rectangle(x_pos, y_pos, gv.SCREEN, gv.BLOCK_SIZE, (149, 54, 146))
#         return start






def generate_walkable_list():

    skip_node = False

    for x in range(0, gv.number_of_x_blocks):
        for y in range(0, gv.number_of_y_blocks):
            walkable = gv.Node(x, y)
            gv.walkableList.append(walkable) #dodany bez terrain

            # if (gv.map[x][y] == 1):
            #     skip_node = True

            # if (not skip_node):
            #     gv.walkableList.append(walkable)
            # skip_node = False


def draw_starting_node(starting_node):
    h.draw_rectangle(starting_node.x, starting_node.y,
                     gv.SCREEN, gv.BLOCK_SIZE, (149, 54, 146))


def draw_ending_node(ending_node):
    h.draw_rectangle(ending_node.x, ending_node.y,
                     gv.SCREEN, gv.BLOCK_SIZE, (54, 63, 149))


def draw_terrain():
    for terrain in gv.terrainList:
        h.draw_rectangle(terrain.x, terrain.y, gv.SCREEN,
                         gv.BLOCK_SIZE, (210, 180, 140))


def draw_closed_list(starting_node, ending_node):
    i = 0
    for closed in gv.closedList:
        i += 1
        if (not closed.equals(starting_node) and not closed.equals(ending_node)):
            h.draw_rectangle(closed.x, closed.y, gv.SCREEN,
                             gv.BLOCK_SIZE, (255, 0, 0))
            # text = gv.font.render(str(i), True, (0, 0, 255))
            # text = gv.font.render(str(closed.f), True, (0, 0, 255))
            # text_rect = text.get_rect(topleft=((closed.x * gv.BLOCK_SIZE) + 5, (closed.y * gv.BLOCK_SIZE) + 5))
            # gv.f_list.append(gv.FRect(text, text_rect))
            # print((closed.x, closed.y))


distance_rect_list = []
final_rect_list = []

def draw_open_list(starting_node, ending_node):
    for o_n in gv.openList:
        if (not o_n.equals(starting_node) and not o_n.equals(ending_node)):
            h.draw_rectangle(o_n.x, o_n.y, gv.SCREEN,
                             gv.BLOCK_SIZE, (0, 255, 0))

            generate_distances(o_n)


def generate_distances(node, final = False):
    g_append = True
    g_distRect = gv.DistRect("g", node.x, node.y, node.g)
    if final:
        for f_r in final_rect_list:
            if f_r.equals(g_distRect):
                f_r.value = g_distRect.value
                g_append = False
        if (g_append):
            final_rect_list.append(g_distRect)
    else:
        for d_r in distance_rect_list:
            if d_r.equals(g_distRect):
                d_r.value = g_distRect.value
                g_append = False
        if (g_append):
            distance_rect_list.append(g_distRect)


    h_append = True
    h_distRect = gv.DistRect("h", node.x, node.y, node.h)
    if final:
        for f_r in final_rect_list:
            if f_r.equals(h_distRect):
                f_r.value = h_distRect.value
                h_append = False
        if (h_append):
            final_rect_list.append(h_distRect)
    else:
        for d_r in distance_rect_list:
            if d_r.equals(h_distRect):
                d_r.value = h_distRect.value
                h_append = False
        if (h_append):
            distance_rect_list.append(h_distRect)


    f_append = True
    f_distRect = gv.DistRect("f", node.x, node.y, node.f)
    if final:
        for f_r in final_rect_list:
            if f_r.equals(f_distRect):
                f_r.value = f_distRect.value
                f_append = False
        if (f_append):
            final_rect_list.append(f_distRect)
    else:
        for d_r in distance_rect_list:
            if d_r.equals(f_distRect):
                d_r.value = f_distRect.value
                f_append = False
        if (f_append):
            distance_rect_list.append(f_distRect)
        

def draw_final_list():

    if (gv.finalList):
        for f_n in gv.finalList:
            h.draw_rectangle(f_n.x, f_n.y, gv.SCREEN,
                             gv.BLOCK_SIZE, (52, 134, 235))

            generate_distances(f_n, True)


def draw_distance_values(final = False):

    GAME_FONT = pygame.freetype.Font("open-sans.ttf", 16)

    text_list = []

    if final:
        text_list = final_rect_list
    else:
        text_list = distance_rect_list

    if (text_list):
        for dist_rect in text_list:

            if (dist_rect.dist_val_name == "g"):
                GAME_FONT.render_to(gv.SCREEN, (dist_rect.rect_x * gv.BLOCK_SIZE + 5,
                                    dist_rect.rect_y * gv.BLOCK_SIZE + 5), "g: " + str(dist_rect.value), (0, 0, 0))

            if (dist_rect.dist_val_name == "h"):
                GAME_FONT.render_to(gv.SCREEN, (dist_rect.rect_x * gv.BLOCK_SIZE + 5,
                                    dist_rect.rect_y * gv.BLOCK_SIZE + 25), "h: " + str(dist_rect.value), (0, 0, 0))

            if (dist_rect.dist_val_name == "f"):
                GAME_FONT.render_to(gv.SCREEN, (dist_rect.rect_x * gv.BLOCK_SIZE + 5,
                                    dist_rect.rect_y * gv.BLOCK_SIZE + 40), "f: " + str(dist_rect.value), (0, 0, 0))
