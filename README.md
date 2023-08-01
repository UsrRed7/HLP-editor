# HLP-editor
A viewer and editor for Minecraft HLP solutions written using pygame

This program is intended to be a convenient way to visulize and test a given function. It has a couple useful utilities and the ability and structure to add more.

### Contents
* [About the problem](#whats-the-problem)
* [How to use](#usage)
* [Interfaces](#interfaces)
* [Function representation](#function-representation)
* [FAQ](#faq)
* [Contributing]()

## What's the problem?

The Hex Layer Problem (HLP) is a np-hard problem that asks: _What is the minimum length function to solve for the given output?_ Where "the given output" is a series of 16 arbitrary hex numbers (0-15).

A function in this case is simply a chain of layers, though that's not helpful if you don't know what a layer is.  
A layer is best described with a picture:  
![layer](/screenshots/layer.png)  

With a function then being a simple extension of that:  
![function](/screenshots/function.png)

*Both of the above images were pulled from this [discord server](https://discord.com/invite/g9XF2wf) whose primary topic is this problem.*

### What is it for?

Though the technology could be be used in a wide variety of Minecraft applications, it's primarily used in computational Minecraft redstone as a form of decoder/lut (Look Up Table). A great example of where this technology is used can be seen in this [youtube video](https://www.youtube.com/watch?v=ySxPHYExxyA).

If you want to learn more about the problem itself, I would recommend checking out [Robolta's HLP solver](https://github.com/Robolta/HLP-Brute-Force-V2). There you will find some great info on the problem itself and current optimizations to programs using brute-force to solve the HLP.

## Usage

To use this program, you will need a python interpreter.  

First you must download the source. Whether with a git clone or a simple download and unzip doesn't matter, though for most downloading and unzipping may be simplest.

Then open your python interpreter and before running it the first time, do a quick:
```bash
pip install pygame pygame_textinput pyperclip
```

Following that you can call the python script: `hlp_viewer.py` or otherwise running the python file.

You should then be greated with the following screen: ![starting screen](/screenshots/opening_screen.png)

If any issues are encountered, please first consult the FAQ and closed issues, then you may open a new issue.

## Interfaces

There isn't a dedicated in-app usage or help menu (or a menu of any kind at this time). Though the controls should be quite intuitive, they are all detailed here:

1. Function maipulation  
To manipulate the current function, left/right click on the comparators, barrels, and the add/delete button.  
* Left clicking on the barrels will increase their value, right clicking will decrease it. The value will automatically loop.
* Clicking with either mouse button on the comprators will toggle its state.
* To add/remove a layer click the add/delete button with the respective left/right mouse buttons wherever you want to add/remove a layer.
2. Pan  
To pan, simply hold _any_ button on your mouse and simply drag it around.
3. Zoom  
Wouldn't you know!? Just scroll in and out with your mouse wheel.
4. Copy/Paste  
The stardard `ctrl+c` and `ctrl+v` are used to copy/paste the entire string.
5. `ctrl` string movements  
Using `ctrl` in conjunction with `backspace`, `delete`, or the left/right arrow keys will perform the associoated action until a passing a space or meeting an end of the line.
6. To string  
Pressing `alt` will replace the current string with a string representation of the current function.
7. From string  
Pressing `enter`/`return` will attempt to parse the current string and updates the current function if successful, otherwise your cursor position will be reset to the beginning of the string and you will see an error message including the layer number the error was encountered on.


## Function representation

The string representation of a function can be understood from an example: ![example_1](/screenshots/example1.png)  
As can be seen, it's a fairly simple system with input to output going from left to right.
* Each layer is seperated by a semicolon.
* Each layer has two parts, the side and the back seperated by a comma.
* Each part has a number that may be preceded by an asterisk, which indicates the state of the comparator.
    * Numbers must be 0-15 or 0-F.

The parser implementation is space-agnostic, so unless you put a space between a two digit number (`14` -> `1 4`) they don't matter to the parser.  
The presence of an asterisk indicates the comparator is in subtract mode (on), its absence indicates compare mode (off).  
Any other unexpected/unknown characters will almost certainly confuse the parser and give an error.

## FAQ

* Q: When I try to run it it just says: `'hlp-viewer.py' is not recognized as an internal or external command, operable program or batch file.`  
A: Please make sure make sure you are in the right directory.

* Q: I'm getting errors that say: `No module named '...'`  
A: Double check you ran the above `pip install` command. If you still get module errors after installing the packages, you can try forcefully re-installing all the modules:
```bash
pip install --force-reinstall pygame pygame_textinput pyperclip
```

* Q: Even after fixing the error in my string, it still says there's an error.  
A: Double check your syntax in the layer the error says, then **make sure to remove the error**.

* Q: Why is it so jittery when I pan?  
A: This is simply becaue by default the refresh rate is set to 20 FPS. You can change this by simply opening the python file in any text editor and modify the `FRAMERATE` value to whatever you want.

* Q: The side comparator isn't working.  
A: The state of sideways comparator to the furthest left in each layer doesn't actually affect the function in any way, and thus isn't considered a button. **The side comparator referrs to the upwards facing comparator in the middle**. Directly to it's right and down one is the 'back' comparator.

## Contributing

Any contributions/ideas you have to improve this application and this repo as a whole are welcome! All the code is in the single python file, and beyond changing the default values at the top of the file for your own prefrences, the code itself is quite structured and is commented throughout.

Whatever your idea is, you may submit an issue labeled as an enhancement if you want feedback before implementing it, or simply submitting a pull request with your change.

Some current ideas that I don't intend to implement myself at this time:
* More robust parser, perhaps the ability to parse additional function syntaxes
* Perhaps a better string error system?
* Alternate text font(s)
* Additional functionality to generate .schem files of the function for easy importation to Minecraft