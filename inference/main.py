import msvcrt
import time

from functional import Game

from prompt_toolkit.shortcuts import clear
from prompt_toolkit import print_formatted_text, HTML

def game_instruction():
    top_row = "+-------------------- INSTRUCTION ---------------------+\n"
    content = "|   1. Pieces's Movement :                             |\n"
    content += "|        1.1 Press 'r' to move left                    |\n"
    content += "|        1.2 Press 't' to move right                   |\n"
    content += "|        1.3 Press 's' to soft drop                    |\n"
    content += "|        1.4 Press 'n' to rotate left                  |\n"
    content += "|        1.1 Press 'e' to move right                   |\n"
    content += "|        1.1 Press space to hard drop                  |\n"
    content += "|   2. Press q to quit the program.                    |\n"
    content += "|   3. Press Ecs to Pause the game.                    |\n"
    bot_row = "+------------------------------------------------------+"

    print_formatted_text(HTML(f"<ansicyan><b>{top_row}</b></ansicyan>" 
                              f"<ansicyan><b>{content}</b></ansicyan>" 
                              f"<ansicyan><b>{bot_row}</b></ansicyan>"
                              ))
    
    inp = input("Press any key for playing ...")

def game_pause():
    clear()
    top_row = '+--------------------- PAUSE --------------------+\n'
    bot_row = '+------------------------------------------------+\n'
    content = '|    1. Press q to quit the program              |\n'
    content += '|    2. Press any others key to continue play    |\n'
    print_formatted_text(HTML(f"<ansicyan><b>{top_row}</b></ansicyan>" 
                              f"<ansicyan><b>{content}</b></ansicyan>" 
                              f"<ansicyan><b>{bot_row}</b></ansicyan>"
                              ))
    inp = input()
    if inp == 'q' : 
        return False
    return True

def gameover():
    top_row = "+------------------ GAME OVER --------------------+\n"
    content = f"|    Your point : {point}{' ' * (32 - len(str(point)))}|\n"
    content += "+-------------------------------------------------+\n"
    content += "|    1. Press q to quit the program.              |\n"
    content += "|    2. Press any others key to play again.       |\n"
    bot_row = "+-------------------------------------------------+\n"
    print_formatted_text(HTML(f"<ansicyan><b>{top_row}</b></ansicyan>" 
                              f"<ansicyan><b>{content}</b></ansicyan>" 
                              f"<ansicyan><b>{bot_row}</b></ansicyan>"
                              ))

    inp = input()
    if inp == 'q':
        return False
    return True

def main():
    global point
    game = Game()
    game.current_lines_clear = 0
    drop_interval = game.speed
    last_drop = time.monotonic()
    running = True

    # print("Tetris running. Press any key to move/rotate; 'q' or ESC to quit.")

    # Initial setup

    game.spawn_pieces()
    game.shadow_piece()
    game.update_board()

    game_instruction()

    game.board.printBoard()

    next_shape, game.next_shape_val = game.piece.generate_pieces()
    game.board.print_next_shape(next_shape, game.point)

    while running:
        # 1) Handle any pending keypress (non-blocking)
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in (b'q'):  # 'q' or ESC
                print("\nQuit key pressed.")
                break
            if ch in (b'\x1b'): 
                running = game_pause()
                if not running : 
                    break
            
            touched = game._check_touch()
            key = ch.decode('utf-8', errors='ignore')
            if key == ' ':
                    print("hard drop")
                    game.current_coor = game.place_down()
                    if game._piece_val in game.board.placed_coor : 
                        game.board.placed_coor[game._piece_val].extend(game.current_coor)
                    else : 
                        game.board.placed_coor[game._piece_val] = [*game.current_coor]
                    touched = True

            if not touched: 

                if key == 'r':
                    print("← move left")
                    game.current_coor = game.move_left()
                elif key == 't':
                    print("→ move right")
                    game.current_coor = game.move_right()
                elif key == 's':
                    print("↓ soft drop")
                    game.current_coor = game.drop_piece()
                elif key == 'n':
                    print("↑ rotate left")
                    game.current_coor = game.rotate_left()
                elif key == 'e': 
                    print("rotate right")
                    game.current_coor = game.rotate_right()

            else : 
                running = not game.game_over()
                game.current_coor = None
                game.update_board()
                game.board.placed_coor, droprow = game.delete_completed_row()
                game.update_board()

                game.point_and_level()
                game.update_board()

                if droprow: 
                    game.down_row()

                game.board.placed_coor = game.update_placed_coor()
                game.update_board()

                game.spawn_pieces(next = next_shape)
                next_shape, game.next_shape_val = game.piece.generate_pieces()

            # --------------------------------

        # Update : 

        game.update_board()
        game.board.printBoard()
        game.board.print_next_shape(next_shape, game.point)

        running = not game.game_over()
        drop_interval = game.speed

        

        # 2) Automatic drop when interval elapsed
        now = time.monotonic()
        if now - last_drop >= drop_interval:
            # Replace this with your piece-fall + render logic:
            # print("\nPiece falls one step")
            touched = game._check_touch()
            if not touched : 
                game.current_coor = game.drop_piece()
            else : 
                running = not game.game_over()

                game.current_coor = None
                game.update_board()
                game.board.placed_coor, droprow = game.delete_completed_row()
                game.update_board()

                game.point_and_level()
                game.update_board()

                if droprow: 
                    game.drop_row()

                game.board.placed_coor = game.update_placed_coor()
                game.update_board()

                game.spawn_pieces(next = next_shape)
                next_shape, game.next_shape_val = game.piece.generate_pieces()

            game.update_board()
            game.board.printBoard()
            game.board.print_next_shape(next_shape, game.point)
            running = not game.game_over()
            drop_interval = game.speed

            last_drop = now

        # small sleep so we don't peg 100% CPU
        time.sleep(0.01)

    point = game.point
        

if __name__ == '__main__':
    play = True 
    while play: 
        main()
        play = gameover()
