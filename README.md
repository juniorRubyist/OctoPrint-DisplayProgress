# OctoPrint-DisplayProgressNeue

A fork of [OctoPrint/OctoPrint-DisplayProgress](https://github.com/OctoPrint/OctoPrint-DisplayProgress) with some additions.

Displays the print progress on the printer's display using M117 and M73 G-code commands.

![Example](http://i.imgur.com/F4m2QlB.jpg)

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OctoPrint/OctoPrint-DisplayProgressNeue/archive/master.zip

## Configuration

```yaml
plugins:
  displayprogress_neue:
    # The message to display. Placeholders:
    # - bar: a progress bar, e.g. [######    ]
    # - progress: the current progress as an integer between 1 and 100
    message: "{bar} {progress:>3}%%"
    # marlin_bar: whether to use the M73 command (Marlin).
    marlin_bar: True
```
