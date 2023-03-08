def get_all_children(widget, inclusive=False, recursive=False):
    # Get all children of a widget
    # Incomplete
    widget_list = widget.winfo_children()
    if recursive:
        for item in widget_list:
            if item.winfo_children():
                widget_list.extend(item.winfo_children())
    if inclusive:
        widget_list.append(widget)
    return widget_list