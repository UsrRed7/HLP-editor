# HLP-editor
A viewer and editor for Minecraft HLP solutions written using pygame

This program is intended to be a convenient way to visulize and test a given function. It has a couple useful utilities and the ability and structure to add more.

### Contents
* [About the problem](#whats-the-problem)
* [How to use](#usage)
* [Interfaces](#interfaces)
* [FAQ](#faq)

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
```
pip install pygame pygame_textinput pyperclip
```

Following that you can call the python script: `hlp_viewer.py` or otherwise running the python file.

You should then be greated with the following screen: ![starting screen](/screenshots/opening_screen.png)

If any issues are encountered, please first consult the FAQ and closed issues, then you may open a new issue.

## Interfaces

There isn't a dedicated in-app usage or help menu (or a menu of any kind at this time). Though the controls should be quite intuitive, they are all detailed here:

1. Copy/Paste  
The stardard `ctrl+c` and `ctrl+v` are used to copy/paste the entire string.
2. Control string movements  
Using `ctrl` in conjunction with `backspace`, `depete`, and the left/right arrow keys will perform the associoated action until a space or the end of the line is met.
3. To string  
Pressing `alt` will replace the current string with a string representation of the current function.
4. From string  
Pressing `enter`/`return` will attempt to parse the current string and updates the current function if successful, otherwise your cursor position will be reset to the beginning of the string and you will see and error message including the layer number the error was encountered on.
5. Pan  
To pan, simply hold _any_ button on your mouse and simply drag it around.
6. Zoom  
Wouldn't you know!? Just scroll in and out with your mouse wheel.
7. Function maipulation  
To manipulate the current function, just start clicking on it, and the output will automatically update live. Left/right clicking on the barrels will decrease/increase the value it's storing, and clicking with either on the forward facing comprators with toggle its state. (The state of the comparator facing sideways doesn't matter)  
To add/remove a layer click the respective left/right mouse buttons at whatever location in the function you wish

TODO: string represation exapmle/explanation

## FAQ

TODO: add any more basic ones that you can think of
* No such file/directory: make sure you are in the right directory.
* I'm getting errors that say: `No module named '...'`  
Double check you ran the above `pip install` command. If you still get module errors after installing the new packages, you can try running:
```
pip install --force-reinstall pygame pygame_textinput pyperclip
```
to forcefully re-install all the external packages this program uses
* String error? double check syntax where the error says, then make sure to remove the error.
* It's super jittery when I pan: this is simply becaue by default the refresh rate is set to 20 FPS. You can change this by simply opening the python file in any text editor and modify the `FRAMERATE` value to whatever you want.
