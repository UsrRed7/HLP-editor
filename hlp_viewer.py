import os
import sys
import pygame
import pygame_textinput as textinput
import pyperclip as clipboard

# SYSTEM VALUES --------------------

# Title of the application
WINDOWTITLE = "HLP editor"

# Initial size of the application window
WINDOWSIZE = (1000, 600)
# Background color of the application
BACKGROUNDCOLOR = (70, 120, 200)

# Framerate of the application
FRAMERATE = 20

# Initial scale of each grid tile
GRIDSCALE = 32
# Initial position for the grid to be drawn based from the lower-left corner of the window
GRIDPOSITION = (10, 10)
# Maximum number of layers the grid can show (mostly just needs some sort of bound)
MAXLAYERS = 24

# Initial scale of the output
INOUTSCALE = 32
# Corner the output should be displayed in: tl, tr, ll, or lr
INOUTCORNER = "lr"
# (x, y) margin between the output display and the border of the window
INOUTMARGIN = (50, 50)
# Vertical space between the output index and actual output
INOUTSPACING = 10

# Font of the text in the text area and its size
TEXTFONT = pygame.font.SysFont("Consolas", 25)
# Default color of the text in the text area
TEXTCOLOR = (10, 10, 10)
# (x, y) margin between the text area and the border of the window
TEXTMARGIN = (20, 20)
# Corner the text area should be displayed in: tl, tr, ll, or lr (Currently lr and tr are the same as their left counterparts)
TEXTCORNER = "tl"

ZOOMSPEED = 3

# SYSTEM SPRITES --------------------

DIGITS = [pygame.image.load_basic(os.path.join("assets", "digits", "0.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "1.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "2.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "3.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "4.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "5.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "6.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "7.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "8.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "9.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "A.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "B.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "C.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "D.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "E.bmp")),
    pygame.image.load_basic(os.path.join("assets", "digits", "F.bmp"))]

COMPARATOR = pygame.image.load_basic(os.path.join("assets", "layer", "comparator.bmp"))
COMPARATORON = pygame.image.load_basic(os.path.join("assets", "layer", "comparator_on.bmp"))
BARREL = pygame.image.load_basic(os.path.join("assets", "layer", "barrel.bmp"))
DUST = pygame.image.load_basic(os.path.join("assets", "layer", "dust.bmp"))
BLOCK = pygame.image.load_basic(os.path.join("assets", "layer", "block.bmp"))

ADDDELETE = pygame.image.load_basic(os.path.join("assets", "buttons", "add_delete.bmp"))


# This is the core of the function part of the program. It is what allows pan and zoom and manages 
# the function, which includes the add/remove functionality.
class Grid:
    def __init__(self, pos: tuple[int, int], maxlayers: int, scale: int):
        # The (x, y) coordinate of the bottom left corner of this grid relative to the bottom left of the window
        self.pos = pos
        self.scale = scale
        self.clicked = False
        # The number of tiles (x, y)
        self.tiles = (maxlayers + 3, maxlayers * 2 + 2)
        # Stores the index of the grid space the cursor is in based from the bottom left of the grid
        self.mouseindex = tuple[int, int]
        self.function = Function([Layer.default()])
        # 16 because the .bmp sprites used are all 16x16
        self.gridsurface = pygame.Surface((self.tiles[0] * 16, self.tiles[1] * 16))

    # Called every frame to re-draw the function on the window.
    # Since the grid is static, it only updates if the mouse is clicked,
    # otherwise it just re-draws itself at the proper location and scale.
    def draw(self, window: pygame.Surface, forceupdate = False):
        mousestate = pygame.mouse.get_pressed()
        
        if not mousestate[0] and not mousestate[2] and not forceupdate:
            self.clicked = False
        elif not self.clicked or forceupdate:
            self.clicked = True

            mousepos = pygame.mouse.get_pos()
            self.mouseindex = ((mousepos[0] - self.pos[0]) // self.scale, (window.get_height() - mousepos[1] - self.pos[1]) // self.scale)
            
            self.gridsurface.fill(BACKGROUNDCOLOR)

            for (index, layer) in enumerate(self.function.layers):
                result = layer.update(index, index * 2, self)
                if result:
                    self.function.layers.insert(index + 1, Layer.default())
                elif result == False and index < (len(self.function.layers) - 1):
                    self.function.layers.remove(self.function.layers[index + 1])

            self.function.compute_output()

        scaledgrid = pygame.transform.scale(self.gridsurface, (self.tiles[0] * self.scale, self.tiles[1] * self.scale))
        window.blit(scaledgrid, (self.pos[0], window.get_height() - scaledgrid.get_height() - self.pos[1]))
    
    # Returns the (x, y) pos (top left) of the grid tile at the given tile index
    def rel_xy(self, xindex, yindex) -> tuple[int, int]:
        return (int(16 * xindex), int(self.gridsurface.get_height() - (16 * (yindex + 1))))



class Layer:
    def __init__(self, sidess: int, sidestate: bool, backss: int, backstate: bool):
        self.base = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.base.blit(DUST, (32, 32))
        self.base.blit(pygame.transform.rotate(COMPARATOR, 270), (16, 16))
        self.base.blit(BARREL, (0, 16))
        self.base.blit(BARREL, (48, 48))
        self.base.blit(COMPARATOR, (32, 16))
        self.base.blit(COMPARATOR, (48, 32))
        self.base.blit(BLOCK, (32, 0))
        self.base.blit(BLOCK, (48, 16))
        self.base.blit(ADDDELETE, (16, 0))

        self.sidebarrel = BarrelButton(sidess, DIGITS)
        self.sidecomparator = ComparatorButton(sidestate, COMPARATORON)
        self.backbarrel = BarrelButton(backss, DIGITS)
        self.backcomparator = ComparatorButton(backstate, COMPARATORON)

    def default():
        return Layer(0, False, 0, False)

    def compute_output(self, inputs):
        outputs = []
        for input in inputs:
            outputs.append(max(
                self.comparator(self.sidebarrel.value, input, self.sidecomparator.state),
                self.comparator(input, self.backbarrel.value, self.backcomparator.state)
            ))
        return outputs

    def comparator(self, side, back, state):
        if state:
            return(max(0, back - side))
        else:
            return(back if back >= side else 0)

    def update(self, xindex, yindex, grid: Grid):
        grid.gridsurface.blit(self.base, grid.rel_xy(xindex, yindex + 3))
        
        self.sidebarrel.clicked(xindex, yindex + 2, grid)
        self.sidecomparator.clicked(xindex + 2, yindex + 2, grid)
        self.backbarrel.clicked(xindex + 3, yindex, grid)
        self.backcomparator.clicked(xindex + 3, yindex + 1, grid)

        if grid.mouseindex == (xindex + 1, yindex + 3):
            if pygame.mouse.get_pressed()[0]:
                return True
            if pygame.mouse.get_pressed()[2]:
                return False



# Though a function is just a list of layers, this class is useful for relavent utility functions
# Currently included beyond the base compute_output() are: tostr and fromstr
# This would be an appropriate place for possible future functionality, such as the ability to
# export a .schem file of the function (then simply call the function from the command seciton with a new key and save the file)
class Function:
    def __init__(self, layers: list[Layer]):
        self.layers = layers
        self.output = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        self.compute_output()

    def compute_output(self):
        self.output = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        for layer in self.layers:
            self.output = layer.compute_output(self.output)
    
    def tostr(self) -> str:
        strfunction = ""
        for layer in self.layers:
            strfunction += "{sidecomp}{sidebarrel},{backcomp}{backbarrel}; ".format(
                sidecomp=   "*" if layer.sidecomparator.state else "",
                sidebarrel= layer.sidebarrel.value,
                backcomp=   "*" if layer.backcomparator.state else "",
                backbarrel= layer.backbarrel.value
            )
        return strfunction

    def fromstr(s: str):
        if len(s) == 0:
            return 0

        function = Function([])

        strlayers = s.split(";")
        for (index, strlayer) in enumerate(strlayers):
            if len(strlayer) > 0 and not strlayer.isspace():
                if not "," in strlayer:
                    return index
                (side, back) = strlayer.split(",", 1)
                side = side.strip()
                back = back.strip()
                if len(side) == 0 or len(back) == 0:
                    return index
                
                if side.startswith("*"):
                    sidestate = True
                    side = side[1:].strip()
                else:
                    sidestate = False

                if back.startswith("*"):
                    backstate = True
                    back = back[1:].strip()
                else:
                    backstate = False

                if side.isdecimal():
                    side = int(side, 10)
                elif side.isalnum():
                    try:
                        side = int(side.upper(), 16)
                    except:
                        return index
                else:
                    return index

                if back.isdecimal():
                    back = int(back, 10)
                elif back.isalnum():
                    try:
                        back = int(back.upper(), 16)
                    except:
                        return index
                else:
                    return index

                if 0 <= side < 16 and 0 <= back < 16:
                    function.layers.append(Layer(side, sidestate, back, backstate))
                else:
                    return index

        return function



class ComparatorButton:
    def __init__(self, state: bool, overlay: pygame.Surface):
        self.state = state
        self.overlay = overlay

    def clicked(self, xindex, yindex, grid: Grid) -> int:
        if grid.mouseindex == (xindex, yindex):
            self.state = not self.state

        if self.state:
            grid.gridsurface.blit(self.overlay, grid.rel_xy(xindex, yindex))



class BarrelButton:
    def __init__(self, value: int, digits: list[pygame.Surface]):
        self.value = value
        self.digits = digits

    def clicked(self, xindex, yindex, grid: Grid) -> int:
        if grid.mouseindex == (xindex, yindex):
            if pygame.mouse.get_pressed()[0]:
                self.value += 1
                if self.value > 15:
                    self.value = 0
            elif pygame.mouse.get_pressed()[2]:
                self.value -= 1
                if self.value < 0:
                    self.value = 15

        grid.gridsurface.blit(self.digits[self.value], grid.rel_xy(xindex, yindex))


# Used to get the position to draw the textarea based from the setting paramaters
def gettextpos(window: pygame.Surface) -> tuple[int, int]:
    if TEXTCORNER == "ll" or TEXTCORNER == "lr":
        return (TEXTMARGIN[0], window.get_height() - TEXTFONT.get_height() - TEXTMARGIN[1])
    else:
        return TEXTMARGIN

# Used to get the position to draw the input/output based from the setting paramaters
# return is ((inputx, inputy), outputy) ouputx is the same as inputx
def inoutpos(window: pygame.Surface) -> tuple[tuple[int, int], int]:
    if INOUTCORNER == "tl":
        inputpos = INOUTMARGIN
    elif INOUTCORNER == "tr":
        inputpos = (window.get_width() - (INOUTSCALE * 16) - INOUTMARGIN[0], INOUTMARGIN[1])
    elif INOUTCORNER == "ll":
        inputpos = (INOUTMARGIN[0], window.get_height() - (INOUTSCALE * 2) - INOUTMARGIN[1])
    else:
        inputpos = (window.get_width() - (INOUTSCALE * 16) - INOUTMARGIN[0], window.get_height() - (INOUTSCALE * 2) - INOUTMARGIN[1])
    return (inputpos, inputpos[1] + INOUTSCALE + INOUTSPACING)

def main(args):

    # SETUP --------------------

    pygame.init()

    pygame.display.set_caption("HLP editor")

    # Setup of the 3 main features of the viewer
    window = pygame.display.set_mode(WINDOWSIZE, pygame.RESIZABLE)
    grid = Grid(GRIDPOSITION, MAXLAYERS, GRIDSCALE)
    textarea = textinput.TextInputVisualizer(font_object=TEXTFONT, font_color=TEXTCOLOR)
    if len(args) > 1:
        textarea.value = args[1]

    # Initial positions of the textarea and the input/output
    # The differentation between the input and output is input is the static top row and the actual output is the bottom
    # These values are only changed if the screen is resized
    textpos = gettextpos(window)
    (inputpos, outputy) = inoutpos(window)

    # Whether the mouse is being dragged for pan
    drag = False

    # The top row of the output display, referred to as the input. Doesn"t change
    inputsurface = pygame.Surface((INOUTSCALE * 16, INOUTSCALE), pygame.SRCALPHA)
    for (index, digit) in enumerate(DIGITS):
        inputsurface.blit(pygame.transform.scale(digit, (INOUTSCALE, INOUTSCALE)), (index * INOUTSCALE, 0))

    # Set initial function by attempting to interpret the textarea string, which at this time
    # has the first argument of the command with which this python file was run
    # (args[0] would be the name of this file, making args[1] the actual first argument)
    grid.function = Function.fromstr(textarea.value)
    if not isinstance(grid.function, Function):
        grid.function = Function([Layer.default()])

    # Initial update of the window to set initial values
    grid.draw(window, True)

    clock = pygame.time.Clock()

    running = True    
    while running:
        clock.tick(FRAMERATE)

        # LOGIC --------------------

        forceupdate = False

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            # Zoom
            elif event.type == pygame.MOUSEWHEEL:
                grid.scale += event.y * ZOOMSPEED

            # Pan
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drag = True
                pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP:
                drag = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Attempt to parse the string in textarea
                elif event.key == pygame.K_RETURN:
                    newfunction = Function.fromstr(textarea.value)
                    if isinstance(newfunction, Function):
                        grid.function = newfunction
                        forceupdate = True
                    else:
                        textarea.manager.cursor_pos = 0
                        textarea.value = f"Err_layer_{newfunction} " + textarea.value
                
                # Set text area to the stirng representation of the funciton
                elif event.mod & pygame.KMOD_ALT:
                    events.remove(event)
                    textarea.value = grid.function.tostr()

                # Command section
                elif event.mod & pygame.KMOD_CTRL:
                    # If the keypress is modified by control it displays an undesired ⍰ character, so this event is simply removed
                    events.remove(event)

                    # Copy/paste
                    if event.key == pygame.K_v:
                        textarea.value = clipboard.paste()
                    elif event.key == pygame.K_c:
                        clipboard.copy(textarea.value)

                    # ctrl+left/right/backspace/delete
                    elif event.key == pygame.K_LEFT:
                        while len(textarea.manager.left) > 1 and textarea.manager.left[-1] != " ":
                            textarea.manager._process_left()
                        textarea.manager._process_left()
                    elif event.key == pygame.K_RIGHT:
                        while len(textarea.manager.right) > 1 and textarea.manager.right[0] != " ":
                            textarea.manager._process_right()
                        textarea.manager._process_right()
                    elif event.key == pygame.K_BACKSPACE:
                        while len(textarea.manager.left) > 1 and textarea.manager.left[-1] != " ":
                            textarea.manager._process_backspace()
                        textarea.manager._process_backspace()
                    elif event.key == pygame.K_DELETE:
                        while len(textarea.manager.right) > 1 and textarea.manager.right[0] != " ":
                            textarea.manager._process_delete()
                        textarea.manager._process_delete()

            elif event.type == pygame.WINDOWRESIZED:
                window == pygame.display.set_mode((event.x, event.y), pygame.RESIZABLE)
                textpos = gettextpos(window)
                (inputpos, outputy) = inoutpos(window)

        if drag:
            dragammount = pygame.mouse.get_rel()
            # Pos y must be subtracted rather than added since pos is based from the lower-left but .get_rel() is based from the top-left
            grid.pos = (grid.pos[0] + dragammount[0], grid.pos[1] - dragammount[1])

        # REFRESH --------------------

        textarea.update(events)

        window.fill(BACKGROUNDCOLOR)

        # Forces update when the grids' function is modified by hitting enter (assuming the string was interpreted without error)
        grid.draw(window, forceupdate)

        window.blit(textarea.surface, textpos)

        window.blit(inputsurface, inputpos)
        for index in range(0, 16):
            window.blit(pygame.transform.scale(DIGITS[grid.function.output[index]], (INOUTSCALE, INOUTSCALE)), (inputpos[0] + (INOUTSCALE * index), outputy))

        pygame.display.update()

    pygame.quit()



if __name__ == "__main__":
    main(sys.argv)