from rpi_ws281x import Color
import pytweening


def interpolate_colors(start_color, end_color, steps):
    # Unpack the start and end colors
    r1, b1, g1, w1 = start_color
    r2, b2, g2, w2 = end_color
    # Generate interpolated values for each color component
    r_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (r2 - r1) + r1) for i in range(steps)]
    g_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (g2 - g1) + g1) for i in range(steps)]
    b_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (b2 - b1) + b1) for i in range(steps)]
    w_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (w2 - w1) + w1) for i in range(steps)]
    # Create color objects for each step
    color_objects = [Color(int(r), int(b), int(g), int(w)) for r, b, g, w in zip(r_values, b_values, g_values, w_values)]
    return color_objects

def init_color_steps(day_phases):
    print("init_color_steps")
    color_steps = []
    next_index = 1
    for d in day_phases:
        next_color = day_phases[next_index].color
        color_steps.extend(interpolate_colors(d.color, next_color, d.steps))
        next_index += 1
        print(f'name: {d.name} time: {d.time} steps: {d.steps}')
        if next_index > len(day_phases) -1:
            next_index = 0

    print("color_steps")
    print(color_steps)
         
    return color_steps
