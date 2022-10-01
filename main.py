import pygame
import sys
import globals as gv
import helpers as h
import map as m
import calculate as c
import pygame.freetype
import pygame.mouse as mouse


def choose_start_end_terrain():

    starting_node = None
    ending_node = None

    while True:

        gv.CLOCK.tick(30)
        m.draw_grid()

        terrain_drawn = False

        if(starting_node and ending_node):
            (b1, _, _) = mouse.get_pressed(num_buttons = 3)

            if b1:
                (x, y) = mouse.get_pos()
                x_pos = h.round_to_block_size(x)
                y_pos = h.round_to_block_size(y)

                t_n = gv.Node(x_pos,y_pos)
                if(not t_n.equals(starting_node) and not t_n.equals(ending_node)):
                    gv.terrainList.append(t_n)
                    gv.map[x_pos][y_pos] = 1
                    h.draw_rectangle(x_pos, y_pos, gv.SCREEN, gv.BLOCK_SIZE, (210, 180, 140))

                if(len(gv.terrainList) > 600):
                    terrain_drawn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 0):
                (x, y) = mouse.get_pos()
                x_pos = h.round_to_block_size(x)
                y_pos = h.round_to_block_size(y)
                if(not starting_node):
                    starting_node = gv.Node(x_pos, y_pos, g = 0, f = 0)
                    gv.openList.append(starting_node)
                    h.draw_rectangle(x_pos, y_pos, gv.SCREEN, gv.BLOCK_SIZE, (149, 54, 146))
                elif(not ending_node):
                    ending_node = gv.Node(x_pos, y_pos)
                    if(not ending_node.equals(starting_node)):
                        h.draw_rectangle(x_pos, y_pos, gv.SCREEN, gv.BLOCK_SIZE, (54, 63, 149))
                    else:
                        ending_node = None

        if(starting_node and ending_node and terrain_drawn):
            return (starting_node, ending_node)

        pygame.display.update()



def run_game(starting_node, ending_node):

    draw_nodes_event = pygame.USEREVENT + 1
    pygame.time.set_timer(draw_nodes_event, 20)

    while True:
        gv.CLOCK.tick(30)
        if gv.game_end:
            m.draw_final_list()
        
        m.draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == draw_nodes_event:
                if not gv.game_end:
                    c.process_open_list(ending_node)
                    m.draw_closed_list(starting_node, ending_node)
                    m.draw_open_list(starting_node, ending_node)
                    m.draw_grid()

        # print(pygame.time.get_ticks())
        pygame.display.update()



if __name__ == '__main__':

    m.generate_walkable_list()

    pygame.init()
    pygame.display.set_caption('A* Search Algorithm')

    (starting_node, ending_node) = choose_start_end_terrain()
    
    run_game(starting_node, ending_node)
