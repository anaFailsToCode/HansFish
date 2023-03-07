"""
Chess "AI"
made by Ana Williams 
aproximate elo 1100
uses minimax/alphabeta pruning
"""
import pygame 


import ChessEngine
import ChessAI
import sys
from multiprocessing import Process, Queue
global AIdepth
AIdepth = 3
height = 800
width = height 

files = 8
sSize = height // files
fps = 180
images = {}
whiteExtraPieces = []
blackExtraPieces = []


def loadimages():
    #load all of theimages into a array, only do this once to maximise efficiency
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
       images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (sSize, sSize))
def getAiDepth():
    return AIdepth

def main():
  
    
    pygame.init() 
    screen = pygame.display.set_mode((width * 4/3, height))
   
    pygame.display.set_caption('Hans Fish')
   
    screen.fill(pygame.Color("white"))
    
   
    moved = False  # tells you when a move has been made
    pieceMove = False  # when true we should animate a piece moveing across the board
    loadimages()  # load all of theimages into a list
    game = True
    clickedSquare = ()  # a tuple of the square the player last clicked
    playerClicks = []  # an array of the players clicks
    gameOver = False #false implies the game is still going on (duh)
    AiThinking = False #tells you if the AI is thinking about a move
    moveUndone = False #tells you wether the last move has just been undone
    move_finder_process = None
    fen ='rnbqkbnr/pppppppp/8/8/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPKPPP'
    game_state = ChessEngine.GameState(fen)
    currentMoves = game_state.getValidMoves()
  
    whitePlayer = False # shows wether white is a human
    blackPlayer = True # shows wether black is a human

    while game:
        human_turn = (game_state.white_to_move and whitePlayer) or (not game_state.white_to_move and blackPlayer) #checks if its a human to play
        for e in pygame.event.get(): #checks too see if there is any events
            if e.type == pygame.QUIT: #if the user exsits the program close it down
                pygame.quit() 
                sys.exit()
            
            elif e.type == pygame.MOUSEBUTTONDOWN: #if the user presses something
                if not gameOver: #only allow the user to interact if the game is still going on
                    location = pygame.mouse.get_pos()  # get the x and y location of the mouse
                    if  890 > location[0] > 820 and 670 > location[1] > 600:
                        game_state.undoMove()
                        moved = True
                        pieceMove = False
                        gameOver = False
                        if AiThinking:
                            move_finder_process.terminate()
                            AiThinking = False
                        moveUndone = True
                    if  1000 > location[0] > 910 and 670 > location[1] > 600:
                        game_state = ChessEngine.GameState(fen)
                        currentMoves = game_state.getValidMoves()
                        clickedSquare = ()
                        playerClicks = []
                        moved = False
                        pieceMove = False
                        gameOver = False
                        if AiThinking:
                            move_finder_process.terminate()
                            AiThinking = False
                        moveUndone = True
                    if  1070 > location[0] > 1000 and 670 > location[1] > 600:
                        print("Fen")
                        
                        input_box = pygame.Rect(300, 300, 250, 250)
                        color_inactive = pygame.Color('lightskyblue3')
                        color_active = pygame.Color('dodgerblue2')
                        color = color_inactive
                        active = False
                        text = 'enter FEN here. exsample: \'Q7/5p2/5P1p/5PPN/6Pk/4N1Rp/7P/6K1\''
                        done = False

                        while not done:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    done = True
                                if event.type == pygame.MOUSEBUTTONDOWN:
                
                                    if input_box.collidepoint(event.pos):
                    
                                        active = not active
                                    else:
                                        active = False
                                    
                # Change the current color of the input box.
                                    color = color_active if active else color_inactive
                                if event.type == pygame.KEYDOWN:
                                    if  text == 'enter FEN here. exsample: \'Q7/5p2/5P1p/5PPN/6Pk/4N1Rp/7P/6K1\'':
                                        text =''
                                    if active:
                                        if event.key == pygame.K_RETURN:
                                            fen = text
                                            done = True
                                            game_state = ChessEngine.GameState(fen)
                                            currentMoves = game_state.getValidMoves()
                                            clickedSquare = ()
                                            playerClicks = []
                                            moved = False
                                            pieceMove = False
                                            gameOver = False
                                            if AiThinking:
                                               move_finder_process.terminate()
                                               AiThinking = False
                                            moveUndone = True
                                           
                                        elif event.key == pygame.K_BACKSPACE:
                                            text = text[:-1]
                                        else:
                                            text += event.unicode
                            txt_surface = pygame.font.SysFont('Comic Sans MS', 14).render(text, True, color)
        # Resize the box if the text is too long.
                            boxwidth = max(500, txt_surface.get_width()+10)
                            pygame.draw.rect(screen,((30, 30, 30)), pygame.Rect(300, 300, boxwidth, 250))
                            input_box.w = boxwidth
        # Blit the text.
                            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
                            pygame.draw.rect(screen, color, input_box, 2)

                            pygame.display.flip()
                    if  890 > location[0] > 820 and 760 > location[1] > 690:
                        
                        
                        input_box = pygame.Rect(300, 300, 250, 250)
                        color_inactive = pygame.Color('lightskyblue3')
                        color_active = pygame.Color('dodgerblue2')
                        color = color_inactive
                        active = False
                        text = 'enter depth here exsample: \'3\''
                        done = False

                        while not done:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    done = True
                                if event.type == pygame.MOUSEBUTTONDOWN:
                
                                    if input_box.collidepoint(event.pos):
                    
                                        active = not active
                                    else:
                                        active = False
                # Change the current color of the input box.
                                    color = color_active if active else color_inactive
                                if event.type == pygame.KEYDOWN:
                                    if  text == 'enter depth here exsample: \'3\'':
                                        text =''
                                    if active:
                                        if event.key == pygame.K_RETURN:
                                            global AIdepth
                                            AIdepth = int(text)
                                            print("changed depth to " + text)
                                            done = True
                                           
                                        elif event.key == pygame.K_BACKSPACE:
                                            text = text[:-1]
                                        else:
                                            text += event.unicode

                            
        # Render the current text.
                            txt_surface = pygame.font.SysFont('Comic Sans MS', 14).render(text, True, color)
        # Resize the box if the text is too long.
                            boxwidth = max(500, txt_surface.get_width()+10)
                            pygame.draw.rect(screen,((30, 30, 30)), pygame.Rect(300, 300, boxwidth, 250))
                            input_box.w = boxwidth
        # Blit the text.
                            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
                            pygame.draw.rect(screen, color, input_box, 2)

                            pygame.display.flip()
                    

                                    

                            
        # Render the current text.
                            txt_surface = pygame.font.SysFont('Comic Sans MS', 14).render(text, True, color)
        # Resize the box if the text is too long.
                            boxwidth = max(500, txt_surface.get_width()+10)
                            pygame.draw.rect(screen,((30, 30, 30)), pygame.Rect(300, 300, boxwidth, 250))
                            input_box.w = boxwidth
        # Blit the text.
                            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
                            pygame.draw.rect(screen, color, input_box, 2)

                            pygame.display.flip()
        

                    else:
                        file = location[0] // sSize
                        rank = location[1] // sSize
                        if clickedSquare == (rank, file) or file >= 8:  # user clicked the same square twice
                            clickedSquare = ()  # deselect
                            playerClicks = []  # clear clicks
                        else:
                            clickedSquare = (rank, file)
                            playerClicks.append(clickedSquare)  # append for both 1st and 2nd click
                    if len(playerClicks) == 2 and human_turn:  # after 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], game_state.board)
                        for i in range(len(currentMoves)):
                            if move == currentMoves[i]:
                                game_state.makeMove(currentMoves[i])
                                moved = True
                                pieceMove = True
                                clickedSquare = ()  # reset user clicks
                                playerClicks = []
                        if not moved:
                            playerClicks = [clickedSquare]

            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    moved = True
                    pieceMove = False
                    gameOver = False
                    if AiThinking:
                        move_finder_process.terminate()
                        AiThinking = False
                    moveUndone = True
                if e.key == pygame.K_r:  # reset the game when 'r' is pressed
                    game_state = ChessEngine.GameState()
                    currentMoves = game_state.getValidMoves()
                    clickedSquare = ()
                    playerClicks = []
                    moved = False
                    pieceMove = False
                    gameOver = False
                    if AiThinking:
                        move_finder_process.terminate()
                        AiThinking = False
                    moveUndone = True

        # AI move finder
        
     
        if not gameOver and not human_turn and not moveUndone:
            if not AiThinking:
                AiThinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, currentMoves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = ChessAI.findRandomMove(currentMoves)
                game_state.makeMove(ai_move)
                moved = True
                pieceMove = True
                AiThinking = False

        if moved:
            if pieceMove:
                pieceMoveMove(game_state.move_log[-1], screen, game_state.board, 60)
            currentMoves = game_state.getValidMoves()
            moved = False
            pieceMove = False
            moveUndone = False

        drawGameState(screen, game_state, currentMoves, clickedSquare)

        

        if game_state.checkmate:
            gameOver = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            gameOver = True
            drawEndGameText(screen, "Stalemate")

        
        pygame.display.flip()


def drawGameState(screen, game_state, currentMoves, clickedSquare):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, currentMoves, clickedSquare)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares
    drawMoveLog(screen, game_state, pygame.font.SysFont('Comic Sans MS', 14))
    drawUndoButton(screen)
    drawRestartButton(screen)
    drawFenButton(screen)
    drawDepthButton(screen)
    drawSaveButton(screen)
    drawAIButton(screen)

def drawUndoButton(screen):
    UndoImage = pygame.transform.scale(pygame.image.load("images/undo.jfif"), (70, 70))
    screen.blit(UndoImage, pygame.Rect(820, 600, 70, 70))
def drawRestartButton(screen):
    restartImage = pygame.transform.scale(pygame.image.load("images/restart.jfif"), (70, 70))
    screen.blit(restartImage, pygame.Rect(910, 600, 70, 70))
def drawFenButton(screen):
    fenImage = pygame.transform.scale(pygame.image.load("images/FEN.png"), (70, 70))
    screen.blit(fenImage, pygame.Rect(1000, 600, 70, 70))
def drawDepthButton(screen):
    DepthImage = pygame.transform.scale(pygame.image.load("images/Depth.png"), (70, 70))
    screen.blit(DepthImage, pygame.Rect(820, 690, 70, 70))
def drawSaveButton(screen):
    DepthImage = pygame.transform.scale(pygame.image.load("images/save.jfif"), (70, 70))
    screen.blit(DepthImage, pygame.Rect(910, 690, 70, 70))
def drawAIButton(screen):
    DepthImage = pygame.transform.scale(pygame.image.load("images/Ai.jfif"), (70, 70))
    screen.blit(DepthImage, pygame.Rect(1000, 690, 70, 70))


def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = pygame.Rect(width, 0, width/3, height)
    pygame.draw.rect(screen, pygame.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding+100
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, pygame.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

        """
        Draw pieces taken
        """
        material =  pygame.font.SysFont('Comic Sans MS', 30).render(str(ChessAI.countMaterial(game_state)), True, pygame.Color('white'))
        if ChessAI.countMaterial(game_state) != 0:
            screen.blit(material, (820, 30))



def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [pygame.Color(234, 235, 200), pygame.Color(119, 154, 88)]
    for rank in range(files):
        for file in range(files):
            color = colors[((rank + file) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(file * sSize, rank * sSize, sSize, sSize))


def highlightSquares(screen, game_state, currentMoves, clickedSquare):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = pygame.Surface((sSize, sSize))
        s.set_alpha(100)
        s.fill(pygame.Color('green'))
        screen.blit(s, (last_move.end_file * sSize, last_move.end_rank * sSize))
    if clickedSquare != ():
        rank, file = clickedSquare
        if game_state.board[rank][file][0] == (
                'w' if game_state.white_to_move else 'b'):  # clickedSquare is a piece that can be moved
            # highlight selected square
            s = pygame.Surface((sSize, sSize))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(pygame.Color('blue'))
            screen.blit(s, (file * sSize, rank * sSize))
            # highlight moves from that square
            s.fill(pygame.Color('yellow'))
            for move in currentMoves:
                if move.start_rank == rank and move.start_file == file:
                  
                    
                    screen.blit(s, (move.end_file * sSize, move.end_rank * sSize))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for rank in range(files):
        for file in range(files):
            piece = board[rank][file]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(file * sSize, rank * sSize, sSize, sSize))




def drawEndGameText(screen, text):
    font = pygame.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, pygame.Color("gray"))
    text_location = pygame.Rect(0, 0, width, height).move(width / 2 - text_object.get_width() / 2,
                                                                 height / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, pygame.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


def pieceMoveMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_rank = move.end_rank - move.start_rank
    d_file = move.end_file - move.start_file
    frames_per_square = 30  # frames to move one square
    frame_count = (abs(d_rank) + abs(d_file)) * frames_per_square
    for frame in range(frame_count + 1):
        rank, file = (move.start_rank + d_rank * frame / frame_count, move.start_file + d_file * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_file + move.end_rank) % 2]
        end_square = pygame.Rect(7 - (move.end_file)  * sSize, move.end_rank * sSize, sSize, sSize)
        pygame.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_rank = move.end_file + 1 if move.piece_captured[0] == 'b' else move.end_file - 1
                end_square = pygame.Rect(move.end_file * sSize, enpassant_rank * sSize, sSize, sSize)
            screen.blit(images[move.piece_captured], end_square)
        # draw moving piece
       # print(move.piece_moved)
        if move.piece_moved != "--":
            screen.blit(images[move.piece_moved], pygame.Rect(file * sSize, rank * sSize, sSize, sSize))
        pygame.display.flip()
        


if __name__ == "__main__":
    main()
