from libqtile.manager import Click, Drag, Group, Key, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

LEFT_ALT = 'mod1'
WINDOWS = 'mod4'
FONT = 'Envy Code R'
FONTSIZE = 13
CHAM1 = '8AE234'
CHAM3 = '4E9A06'
GRAPH_KW = dict(line_width=1,
                graph_color=CHAM3,
                fill_color=CHAM3+'.3',
                border_width=1,
                border_color=CHAM3
                )

print "NAME", __name__

import sys
print sys.argv
if 'dev.py' in sys.argv[-1]:
    # running dev as this:
    # Xephyr +extension RANDR -screen 800x600  :1 -ac & (sleep 1; env DISPLAY=:1 ~/work/pylibs/qtile/qtile -d -c /home/matt/.config/qtile/mattdev.py & env DISPLAY=:1 xterm)
    # hard to debug/while using qtile as main wm
    MOD = LEFT_ALT
else:
    MOD = WINDOWS # use xev and xmodmap to figure out name
             # this is the windows key
keys = [
    # First, a set of bindings to control the layouts
    Key(
        [MOD], "k",
        lazy.layout.down()
    ),
    Key(
        [MOD], "j",
        lazy.layout.up()
    ),
    Key(
        [MOD, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [MOD, "control"], "j",
        lazy.layout.shuffle_up()
    ),
    # Key(
    #     [MOD], "space",
    #     lazy.layout.next()
    # ),
    # Key(
    #     [MOD, "shift"], "space",
    #     lazy.layout.rotate()
    # ),
    Key(
        [MOD, "shift"], "Return",
        lazy.layout.toggle_split()
    ),

    Key([MOD], "n",      lazy.spawn("firefox")),
    Key([MOD], "h",      lazy.to_screen(1)),
    Key([MOD], "l",      lazy.to_screen(0)),
    # ~/bin/x starts a terminal program
    #Key([MOD], "Return", lazy.spawn("~/bin/x")),
    Key([MOD], "Return", lazy.spawn("terminator -p tango")),
    #Key([MOD], "Tab",    lazy.nextlayout()),
    Key([MOD], "space",    lazy.nextlayout()),
    Key([MOD, 'shift'], "space",    lazy.prevlayout()),
    Key([MOD], "Tab",    lazy.group.next_window()),
    Key([MOD, 'shift'], "Tab",    lazy.group.prev_window()),
    Key([MOD, 'shift'], "c",      lazy.window.kill()),
    Key([MOD], "f",      lazy.window.toggle_floating()),
    Key([MOD], "m",      lazy.window.toggle_minimize()),
    Key([MOD], "x",      lazy.window.toggle_maximize()),
    Key([MOD], "u",      lazy.window.toggle_fullscreen()),
    #Key([MOD], "[",   lazy.window.move_floating(-10,0)),
    #Key([MOD], "]",   lazy.window.move_floating(10,0)),
    Key([MOD, 'shift'], "r",      lazy.restart()),
    Key([MOD], "p",      lazy.spawncmd()),
    #Key([MOD, 'shift'], "Down", lazy.window.down_opacity()),
    Key([MOD], "z", lazy.window.down_opacity()),
    Key([MOD], "downarrow", lazy.window.down_opacity()),
    #Key([MOD, 'shift'], "Up", lazy.window.up_opacity()),
    Key([MOD], "a", lazy.window.up_opacity()),


    # The bindings below control Amarok, and my sound volume.
    Key(
        [MOD, "shift"], "k",
        lazy.spawn("amixer -c 1 -q set Speaker 2dB+")
    ),
    Key(
        [MOD, "shift"], "j",
        lazy.spawn("amixer -c 1 -q set Speaker 2dB-")
    ),
    Key(
        [MOD, "shift"], "n",
        lazy.spawn("amarok -t")
    ),
    Key(
        [MOD, "shift"], "l",
        lazy.spawn("amarok -f")
    ),
    Key(
        [MOD, "shift"], "h",
        lazy.spawn("amarok -r")
    ),
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = [Group(str(x)) for x in range(1,10)]

for i in groups:
    keys.append(
        Key([MOD], i.name, lazy.group[i.name].toscreen())
    )
    keys.append(
        Key([MOD, "shift"], i.name, lazy.window.togroup(i.name))
    )


# Two simple layout instances:
layouts = [
    layout.Tile(),
    layout.Max(),
    layout.Stack(stacks=2),
    layout.RatioTile(),
    layout.RatioTile(fancy=True),
    layout.RatioTile(ratio=.618),
    layout.RatioTile(ratio=.618, fancy=True)
]


floating_layout = layout.floating.Floating(float_rules=[dict(wmclass="skype"),
                                                        dict(wmclass="Xephyr"),
                                                        dict(wmclass="gimp")])

cursor_warp = True

mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front())
]

# I have two screens, each of which has a Bar at the bottom. Each Bar has two
# simple widgets - a GroupBox, and a WindowName.
screens = [
    Screen(
        top = bar.Bar(
                    [
                        widget.GroupBox(this_screen_border=CHAM3,
                                        borderwidth=1,
                            font=FONT,fontsize=FONTSIZE,
                            padding=1, margin_x=1, margin_y=1),
                        widget.AGroupBox(),
                        widget.Prompt(),
                        widget.Sep(),
                        widget.WindowName(
                            font=FONT,fontsize=FONTSIZE, margin_x=6),
                        widget.Sep(),
                        widget.CPUGraph(**GRAPH_KW),
                        widget.MemoryGraph(**GRAPH_KW),
                        widget.SwapGraph(foreground='20C020', **GRAPH_KW),
                        #widget.IOWaitGraph(foreground='20C020', **GRAPH_KW),
                        widget.Sep(),
                        widget.Systray(),
                        widget.Sep(),
                        widget.Battery(font=FONT, fontsize=FONTSIZE),
                        widget.Sep(),
                        widget.Clock('%H:%M:%S %d.%m.%Y',
                            font=FONT, fontsize=FONTSIZE, padding=6),
                    ],
                    24,
                ),
    ),
    Screen(
        bottom = bar.Bar(
                    [
                        widget.GroupBox(),
                        widget.WindowName(),
                        widget.Clock()
                    ],
                    30,
                ),
    ),

]

@hook.subscribe.client_new
def dialogs(window):
    if window.window.get_wm_type() == 'dialog':
        window.floating = True
