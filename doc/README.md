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
        properties:
            ...                 # See ScreenProperties below
        events:
            open: eventName()   # Event function to execute before the page is shown
            close: eventName()  # Event function to execute when this page is closed
```

## Widgets
### Common properties
These properties are available for each single widget, they're defaulted to a common value
when are not declared.
```yaml
# COMMON properties
- Type: <OneOfThese>    # widgetType [required] Your favorite widget
        box             #   - Draw a box
        button          #   - Draw a button (just like a box but pretty with a text caption)
        text            #   - Print some text on the screen (centered on X,Y)
        listbox         #   - Draw a listbox for list contents
        windowdialog    #   - Draw a modal window like box (confirm, info, errors, ...)
        dot             #   - Draw a single dot on the screen
        circle          #   - Draw a circle
        crosshair       #   - Draw a crosshair (useful for calibration stuff)
        hidden          #   - Nothing displayed but touchscreen action available like a button
        image           #   - Display an image
  id: widgetID          # widgetID   [optional] Widget ID
  x:  10                # Integer    [optional] X Position for the widget
  y:  10                # Integer    [optional] Y Position for the widget
  color:  255,255,255   # Tuple      [optional] Widget color (RGB, 3 bytes)
  action: None          # String     [optional] Action associated to this widget
  t_x1: <calc>          # Touch Xmin [optional] Touchscreen X min (calculated or manually set)
  t_y1: <calc>          # Touch Ymin [optional] Touchscreen Y min (calculated or manually set)
  t_x2: <calc>          # Touch Xmax [optional] Touchscreen X max (calculated or manually set)
  t_y2: <calc>          # Touch Ymax [optional] Touchscreen Y max (calculated or manually set)
                        #            t_x1 < t_x2,   t_y1 < t_y2     [[ !ALWAYS! ]]
```

### Widgets
Each single widget always has all common properties described above and adds its own special features
```yaml
# [BOX] extra properties
- type: box
  width: 100                    Integer  [optional] Widget width
  height: 50                    Integer  [optional] Widget height
  border: 0                     Integer  [optional] Widget border
  bordercolor: 255,255,255      Tuple    [optional] Widget default color (RGB)

# [BUTTON] extra properties     Inherits properties from [BOX]
- type: button
  border: 2                     Integer  [optional] Button border
  text: 'button'                Text     [optional] Text caption
  textsize: 24                  Integer  [optional] Text caption font size
  textcolor: 255,255,255        Tuple    [optional] Text color (also TopLeft border)
  textalign: left|center|right  Enum     [optional] Window message alignment [Default:center]
  textspacing: 10               Integer  [optional] Spacing from border [alignment=left|right]
  bordercolor: 255,255,255      Tuple    [optional] BottomRight border color

# [TEXT] extra properties
#        Font: 'dejavuserif','dejavusansmono','freesans','dejavusans','freeserif','freemono'
#        Font Variants: <fontName>+'bold'
- type: text
  text: 'TEXT'                  String   [optional] Text label
  textfont: freesans            String   [optional] Font type [Default:freesans]
  textsize: 24                  Integer  [optional] Text font size
  textalign: left|center|right  Enum     [optional] Text alignment [default:center]
  textcolor: 255,255,255        Tuple    [optional] Text color [color]=[textcolor]

# [WINDOWDIALOG] extra properties
- type: windowdialog
  width:  250                   Integer  [optional] Widget width
  height: 100                   Integer  [optional] Widget height
  title: 'window title'         Text     [optional] Window title
  titlebackground: 20,50,70     Tuple    [optional] Window title background color
  color: 50,188,228             Tuple    [optional] Widget color (window color)
  bordercolor: 120,120,120      Tuple    [optional] Border color (buttons and window)
  text: 'info message'          Text     [optional] Text message
  textsize: 18                  Integer  [optional] Window message text size
  textcolor: 255,255,255        Tuple    [optional] Text color
  textalign: left|center|right  Enum     [optional] Window message alignment, [default:left]
  button1: '  OK  '             Text     [optional] Button1 text, if [None] is not shown
  button2:  CANCEL              Text     [optional] Button2 text, if [None] is not shown
  buttonwidth: 64               Integer  [optional] Buttons width
  buttonheight: 18              Integer  [optional] Buttons height
  buttontextcolor: 0,0,0        Tuple    [optional] Buttons text color
  buttoncolor: 50,188,228       Tuple    [optional] Buttons background color
  action:  None                 String   [optional] Action associated to button1
  action2: None                 String   [optional] Action associated to button2

# [LISTBOX] extra properties
- type: listbox
  width: 200                    Integer  [optional] Widget width
  height: 150                   Integer  [optional] Widget height
  color: 0,0,0                  Tuple    [optional] Widget color (inner box color)
  border: 1                     Integer  [optional] Widget border
  bordercolor: 128,128,128      Tuple    [optional] Border and scrollbar color
  textsize: 18                  Integer  [optional] Text list size
  textfont: freesans            String   [optional] Font type [default:freesans]
  textcolor: 255,255,255        Tuple    [optional] Text list color [default]
  textalign: left|center|right  String   [optional] Text alignment, [default:left]
  textspacing: 10               Integer  [optional] Spacing from border
  scrollbarwidth: 40            Integer  [optional] Scrollbar width
  list:                         Array    [mandatory] Items list
    - item1                     #<-- These two items contains the same value
    - text: item1               #<--        (but have different index [0,1])
    - item2
    - text: item3               # Item with text: 'item3' and color '127,0,0'
      color: 127,0,0            #
    - itemN
  action: None                  String   [optional] Action when item selected
  # Action example.             Here's a YAML definition and a programming sample
  #  YAML FILE                  # Inside .yaml file
  #     action: myFunc()        
  #  PYTHON                     # Function definition, in your code
  #     def myFunc(self, listbox, index):
  #         print('Widget ID={}  '.format(listbox['id']))
  #         print('       Item={}'.format(listbox['list'][index]['text']))
  # @see [userobject.testListbox()] for further details
  selected: N                   Integer  [property] Returns currently selected item

# [HIDDEN] extra properties.    [color] property NOT used
- type: hidden
  width: 64                     Integer  [optional] Widget area width
  height: 18                    Integer  [optional] Widget area height

# [IMAGE] Display an image
- type: image
  src: <imageName.jpg>          String   [mandatory] Image to display

# [DOT] extra properties (none)
- type: dot

# [CIRCLE]    properties ..and.. [CROSSHAIR] properties
- type: circle|crosshair
  fill: true|false              Boolean  [optional] Fill the crosshair (with [color])
  radius: 10                    Integer  [optional] Crosshair radius
```




## ScreenProperties
global properties related to the selected [screenName]
```yaml
Screen:
    <screenName>:               # ScreenID   [required] (main: first displayed screen)
        properties:             # [optional]
            color: 0,0,0        # Screen background color
```




## Events
Here's a sample with events
```yaml
Screen:
    <screenName>:               # ScreenID   [required] (main: first displayed screen)
        events:                 # [optional]
            open: eventOpen()   # Event function to execute before the page is shown
            close: eventClose() # Event function to execute when this page is closed
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
      - type: text
        id: status
        x: 100
        y: 8
        text: Text Message
        textsize: 28
        textfont: freesansbold
        textcolor: 0,150,255
        textalign: left
      - type: listbox
        id: joblist
        x: 50
        y: 40
        width: 250
        height: 140
        color: 50,50,50
        action: jobSelect()
        list:
            - Item 1
            - text: Item 2
            - text: item 3
              color: 255,0,0
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
