<img width="1428" height="864" alt="screenshot of neotimer" src="https://github.com/user-attachments/assets/0ecaa2eb-04d2-476f-9a70-d5926282cf25" />

# neotimer
A simple, in-terminal Speedcubing terminal

neotimer is made using the Textual library, making it neotimer's only dependency, so you should install it on your system before trying to use neotimer. Other than it, neotimer is designed to be minimal by having a simple interface and a small codebase.

## Installation
As of now, neotimer isn't distributed through any package manager. However, due to its simplicity, installation is still quite simple.

On most systems, you'll just need to make sure you have `textual` installed (usually something similar to `python3-textual` in most package managers), then copy the `main.py` and `neotimer.tcss` files to your system and run it with `python main.py`. You could then use a shell alias to start it easily (such as `alias ntimer="python <path to main.py>"` in your `.bashrc`), or continue to use it via python directly.

On Windows, the process is similar, but you'll likely need to get textual from pip instead.

If there is demand, neotimer could be packaged through something such as pipx in the future or any other requested platforms.

## Usage
Due to limitations in how terminals capture keyboard input, neotimer (and most terminal apps) can't know if you're holding a key or just pressing it once. For this reason, instead of holding and then releasing space to start, you **hold `alt` and then quickly press `space`** to start the timer. This should be easy to get used to from regular cubing timers. To stop, you can just *press space*. To add a *+2* to your last solve, just press `2` on your keyboard, and to delete your last solve, just press `x` on your keyboard.

## Customization
To change the average counter display, currently there is no standard settings menu, so you'll need to change the hardcoded value in the source code. *However, this is quite simple*. Just open `main.py` in any text editor, locate the line `average_view = "avg5"` and change `"avg5"` to one of the following: `"avg", "avg & avg5", "avg & avg5 & avg12", "avg5"`.

A proper settings system will probably be added in a future update

You can also modify `neotimer.tcss` to directly edit the app's styling, which is quite minimal by default, however, there isn't a lot to change with the app's current widgets.
