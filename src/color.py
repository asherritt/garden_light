from rpi_ws281x import Color
import pytweening
from model import PhaseColor, SegColor3, Step

phase_colors = [
    PhaseColor(
        name='midnight',
        lamps_on=True,
        fill_light=(0, 40, 0, 20),
        cyc=[
            SegColor3(red=81, green=85, blue=94),
            SegColor3(red=77, green=115, blue=255),
            SegColor3(red=92, green=79, blue=68),
            SegColor3(red=91, green=99, blue=115),
            SegColor3(red=37, green=37, blue=71),
        ],
    ),
    PhaseColor(
        name='first_light',
        lamps_on=True,
        fill_light=(0, 30, 0, 8),
        cyc=[
            SegColor3(red=191, green=201, blue=255),
            SegColor3(red=187, green=158, blue=255),
            SegColor3(red=77, green=115, blue=255),
            SegColor3(red=77, green=115, blue=255),
            SegColor3(red=77, green=115, blue=255),
        ],
    ),
    PhaseColor(
        name='dawn',
        lamps_on=False,
        fill_light=(90, 0, 15, 30),
        cyc=[
            SegColor3(red=255, green=206, blue=145),
            SegColor3(red=186, green=255, blue=218),
            SegColor3(red=158, green=161, blue=255),
            SegColor3(red=77, green=115, blue=255),
            SegColor3(red=173, green=184, blue=255),
        ],
    ),
    PhaseColor(
        name='sunrise',
        lamps_on=False,
        fill_light=(120, 0, 25, 45),
        cyc=[
            SegColor3(red=255, green=196, blue=87),
            SegColor3(red=255, green=176, blue=107),
            SegColor3(red=255, green=188, blue=112),
            SegColor3(red=255, green=184, blue=112),
            SegColor3(red=242, green=255, blue=251),
        ],
    ),
    PhaseColor(
        name='solar_noon',
        lamps_on=False,
        fill_light=(200, 255, 190, 255),
        cyc=[
            SegColor3(red=255, green=209, blue=171),
            SegColor3(red=255, green=216, blue=214),
            SegColor3(red=255, green=188, blue=112),
            SegColor3(red=255, green=228, blue=227),
            SegColor3(red=255, green=237, blue=199),
        ],
    ),
    PhaseColor(
        name='golden_hour',
        lamps_on=False,
        fill_light=(255, 0, 20, 90),
        cyc=[
            SegColor3(red=255, green=195, blue=166),
            SegColor3(red=255, green=222, blue=217),
            SegColor3(red=255, green=166, blue=115),
            SegColor3(red=255, green=156, blue=145),
            SegColor3(red=255, green=197, blue=158),
        ],
    ),
    PhaseColor(
        name='sunset',
        lamps_on=False,
        fill_light=(200, 0, 10, 125),
        cyc=[
            SegColor3(red=227, green=191, blue=255),
            SegColor3(red=255, green=223, blue=204),
            SegColor3(red=255, green=155, blue=97),
            SegColor3(red=255, green=137, blue=64),
            SegColor3(red=255, green=67, blue=20),
        ],
    ),
    PhaseColor(
        name='dusk',
        lamps_on=True,
        fill_light=(15, 40, 20, 10),
        cyc=[
            SegColor3(red=255, green=209, blue=253),
            SegColor3(red=184, green=198, blue=255),
            SegColor3(red=255, green=209, blue=253),
            SegColor3(red=255, green=209, blue=253),
            SegColor3(red=255, green=209, blue=253),
        ],
    ),
    PhaseColor(
        name='last_light',
        lamps_on=True,
        fill_light=(0, 10, 0, 0),
        cyc=[
            SegColor3(red=145, green=202, blue=255),
            SegColor3(red=145, green=202, blue=255),
            SegColor3(red=145, green=202, blue=255),
            SegColor3(red=145, green=202, blue=255),
            SegColor3(red=145, green=202, blue=255),
        ],
    ),
    PhaseColor(
        name='eod',
        lamps_on=True,
        fill_light=(0, 40, 0, 20),
        cyc=[
            SegColor3(red=81, green=85, blue=94),
            SegColor3(red=77, green=115, blue=255),
            SegColor3(red=92, green=79, blue=68),
            SegColor3(red=91, green=99, blue=115),
            SegColor3(red=37, green=37, blue=71),
        ],
    ),
]

def _interpolate_rgbw_colors(start_color, end_color, steps):
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

def _interpolate_rgb_colors(start_color, end_color, steps):
    # Unpack the start and end colors
    r1, b1, g1 = start_color
    r2, b2, g2 = end_color
    # Generate interpolated values for each color component
    r_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (r2 - r1) + r1) for i in range(steps)]
    g_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (g2 - g1) + g1) for i in range(steps)]
    b_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (b2 - b1) + b1) for i in range(steps)]
    # Create color objects for each step
    color_objects = [Color(int(r), int(b), int(g)) for r, b, g in zip(r_values, b_values, g_values)]
    return color_objects


def get_steps(phases):
    steps = []
    next_index = 1
    for phase in phases:
            # create interpolated fill colors
            fill_light_color = next((phase_color.fill_light for phase_color in phase_colors if phase_color.name ==  phase.name), None)
            assert fill_light_color is not None, f"No matching phase color found for phase name '{phase.name}'."
            
            next_fill_color =  next((phase_color.fill_light for phase_color in phase_colors if phase_color.name ==  phases[next_index].name), None)
            assert next_fill_color is not None, f"No matching phase color found for phase name '{phases[next_index].name}'."

            fill_colors_interpolated = _interpolate_rgbw_colors(fill_light_color, next_fill_color, phase.total_minutes)

           # Interpolating cyc segment colors
            cyc_colors = next((pc.cyc for pc in phase_colors if pc.name == phase.name), None)
            assert cyc_colors is not None, f"No matching phase color found for phase name '{phases[next_index].name}'."

            next_cyc_colors = next((pc.cyc for pc in phase_colors if pc.name == phases[next_index].name), None)
            assert next_cyc_colors is not None, f"No matching phase color found for phase name '{phases[next_index].name}'."

            cyc_colors_interpolated = [
                _interpolate_rgb_colors(cyc_colors[i].to_tuple(), next_cyc_colors[i].to_tuple(), phase.total_minutes)
                for i in range(len(cyc_colors))
            ]

            for m in range(phase.total_minutes):
                interpolated_cyc = [cyc_colors_interpolated[i][m] for i in range(len(cyc_colors))]
                steps.append(
                    Step(
                        time=phase.add_minutes(m),
                        lamps_on=phase.lamps_on,
                        phase_name=phase.name,
                        fill_light=fill_colors_interpolated[m],
                        cyc=interpolated_cyc,
                    )
                )
         
            # Wrap next index back to 0
            if next_index > len(phases) -1:
                next_index = 0
                
    return steps
