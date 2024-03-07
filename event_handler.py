
def on_menu_option_1_click():
    """
    Handler for option 1 menu click
    """
    print("Option 1") 

def on_menu_option_2_click():
    """
    Handler for option 2 menu click
    """
    print("Option 2") 

def on_menu_option_3_click():
    """
    Handler for option 3 menu click
    """
    print("Option 3") 

def on_canvas_click(event):
    """
    Handler for canvas click
    """
    x, y = event.x, event.y
    print(f"Mouse clicked at coordinates: ({x}, {y})")
