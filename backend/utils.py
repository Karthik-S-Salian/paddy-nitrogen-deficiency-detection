def rgb_to_hsv(rgb):
    # Normalize RGB values to the range [0, 1]
    r, g, b = [x / 255.0 for x in rgb]

    # Find the minimum and maximum values
    min_val = min(r, g, b)
    max_val = max(r, g, b)
    delta = max_val - min_val

    # Calculate Hue
    if delta == 0:
        hue = 0
    elif max_val == r:
        hue = 60 * (((g - b) / delta) % 6)
    elif max_val == g:
        hue = 60 * (((b - r) / delta) + 2)
    elif max_val == b:
        hue = 60 * (((r - g) / delta) + 4)

    # Calculate Saturation
    saturation = 0 if max_val == 0 else delta / max_val

    # Calculate Value
    value = max_val

    # Adjust hue to be in the range [0, 360]
    hue = (hue + 360) % 360

    return (hue, saturation, value)

