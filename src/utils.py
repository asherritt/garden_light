def convert_rgb_int_to_rgb(rgb_int):
    red = (rgb_int >> 16) & 0xFF
    green = (rgb_int >> 8) & 0xFF
    blue = rgb_int & 0xFF

    # Return the formatted string
    return f"{red}, {green}, {blue}"