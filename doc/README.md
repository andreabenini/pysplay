# Documentation
YAML file documentation with widgets, properties and actions associated to **pysplay** _library_

## Structure
**pysplay** YAML structure is short and easy to understand, sections and variables are case insensitive but
assigned values are not. here's a skeleton overview:
```yaml
Screen:
    <screenName>:               # ScreenID   [required] (main: first displayed screen)
        display:                # display    [required] Collection of screen widgets
            - <widgetItem_1>    # Widget description, see [Widgets] below
            - <widgetItem_2>
            - ...
            - <widgetItem_N>
        events:
            show: eventName     # Event function to execute before the page show event
```

## Widgets
### Common properties
These properties are available to each single widget, they're defaulted to a common value
when aren't declared
```yaml
# COMMON properties
- Type: <OneOfThese>   # widgetType [required] Your favorite widget
        box            #   - Draw a box
        button         #   - Draw a button (just like a box but pretty with a text caption)
        text           #   - Print some text on the screen (centered on X,Y)
        windowdialog   #   - Draw a modal window like box (confirm, info, errors, ...)
        dot            #   - Draw a single dot on the screen
        circle         #   - Draw a circle
        crosshair      #   - Draw a crosshair (useful for calibration stuff)
        hidden         #   - Nothing displayed but touchscreen action available like a button
        image          #   - Display an image
  id: widgetID         # widgetID   [optional] Widget ID
  x: 10                # Integer    [optional] X Position for the widget
  y: 10                # Integer    [optional] Y Position for the widget
  color: 255,255,255   # Tuple      [optional] Widget color
  action: None         # String     [optional] Action associated to this widget
  t_x1: <calc>         # Touch Xmin [optional] Touchscreen X min (calculated or manually set)
  t_y1: <calc>         # Touch Ymin [optional] Touchscreen Y min (calculated or manually set)
  t_x2: <calc>         # Touch Xmax [optional] Touchscreen X max (calculated or manually set)
  t_y2: <calc>         # Touch Ymax [optional] Touchscreen Y max (calculated or manually set)
                       #            t_x1 < t_x2,   t_y1 < t_y2     [[ !ALWAYS! ]]
```

### Widgets
Each single widget always has all common properties described above and adds its own special features
```yaml
# [BOX] extra properties
- type: box
  width: 100                    Integer    [optional] Widget width
  height: 50                    Integer    [optional] Widget height
  border: 0                     Integer    [optional] Widget border
  bordercolor: 255,255,255      Tuple      [optional] Widget default color (RGB)

# [BUTTON] extra properties     Inherits properties from [BOX]
- type: button
  border: 2                     Integer    [optional] Button border
  text: 'button'                Text       [optional] Text caption
  textsize: 24                  Integer    [optional] Text caption font size
  textcolor: 255,255,255        Tuple      [optional] Text color (also TopLeft border)
  textalign: left|center|right  Enum       [optional] Window message alignment, Default [center]
  textspacing: 10               Integer    [optional] Spacing from border [alignment=left|right]
  bordercolor: 255,255,255      Tuple      [optional] BottomRight border color

# [TEXT] extra properties
#        Font: 'dejavuserif','dejavusansmono','freesans','dejavusans','freeserif','freemono'
#        Font Variants: <fontName>+'bold'
- type: text
  text: 'TEXT'                  Text       [optional] Text label
  textfont: freesans            Text       [optional] Font type [Default:freesans]
  textsize: 24                  Integer    [optional] Text font size
  textalign: left|center|right  Enum       [optional] Text alignment (default [center])
  textcolor: 255,255,255        Tuple      [optional] Text color [color]=[textcolor]

# [WINDOWDIALOG] extra properties
- type: windowdialog
  width:  250                   Integer    [optional] Widget width
  height: 100                   Integer    [optional] Widget height
  title: 'window title'         Text       [optional] Window title
  titlebackground: 20,50,70     Tuple      [optional] Window title background color
  color: 50,188,228             Tuple      [optional] Widget color (window color)
  bordercolor: 120,120,120      Tuple      [optional] Border color (buttons and window)
  text: 'info message'          Text       [optional] Text message
  textsize: 18                  Integer    [optional] Window message text size
  textcolor: 255,255,255        Tuple      [optional] Text color
  textalign: left|center|right  Enum       [optional] Window message alignment, default [left]
  button1: '  OK  '             Text       [optional] Button1 text, if [None] is not shown
  button2:  CANCEL              Text       [optional] Button2 text, if [None] is not shown
  buttonwidth: 64               Integer    [optional] Buttons width
  buttonheight: 18              Integer    [optional] Buttons height
  buttontextcolor: 0,0,0        Tuple      [optional] Buttons text color
  buttoncolor: 50,188,228       Tuple      [optional] Buttons background color
  action:  None                 String     [optional] Action associated to button1
  action2: None                 String     [optional] Action associated to button2

# [HIDDEN] extra properties. [color] property not used
- type: hidden
  width: 64                     Integer    [optional] Widget area width
  height: 18                    Integer    [optional] Widget area height

# [IMAGE] Display an image
- type: image
  src: <imageName.jpg>          String     [mandatory] Image to display

# [DOT] extra properties (none)
- type: dot

# [CIRCLE]    properties ..and.. [CROSSHAIR] properties
- type: circle|crosshair
  fill: true|false              Boolean    [optional] Fill the crosshair (with [color])
  radius: 10                    Integer    [optional] Crosshair radius
```

## Example
Here's a sample configuration file
```yaml
screen:
  main:
    Display:
      - Type: box
        id: box1
        x: 5
        y: 10
        width: 20
        height: 30
        color: 100,50,191
        action: exit
      - type: box
        id: box2
        x: 50
        y: 100
        width: 70
        height: 30
        border: 1
      - type: dot
        x: 160
        y: 120
        color: 255,255,255
      - type: dot
        x: 00
        y: 120
        color: 255,255,255
      - type: dot
        x: 319
        y: 120
        color: 255,255,255
      - type: button
        id: button1
        x: 100
        y: 30
        width: 100
        height: 30
        text: Hello World
        action: exit
```