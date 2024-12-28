from rpi_ws281x import Color
import pytweening
from model import PhaseColor, Step

phase_colors = [
    PhaseColor(
        name='midnight',
        lamps_on=True,
        fill_light=[(0, 40, 0, 20), (0, 40, 0, 20), (0, 40, 0, 20)],
        cyc=[
            (81, 85, 94),
            (77, 115, 255),
            (92, 79, 68),
            (91, 99, 115),
            (37, 37, 71),
        ],
    ),
    PhaseColor(
        name='first_light',
        lamps_on=True,
        fill_light=[(0, 30, 0, 8), (0, 30, 0, 8), (0, 30, 0, 8)],
        cyc=[
            (191, 201, 255),
            (187, 158, 255),
            (77, 115, 255),
            (77, 115, 255),
            (77, 115, 255),
        ],
    ),
    PhaseColor(
        name='dawn',
        lamps_on=False,
        fill_light=[(90, 0, 15, 30), (90, 0, 15, 30), (90, 0, 15, 30)],
        cyc=[
            (255, 206, 145),
            (186, 255, 218),
            (158, 161, 255),
            (77, 115, 255),
            (173, 184, 255),
        ],
    ),
    PhaseColor(
        name='mid_morning',
        lamps_on=False,
        fill_light=[(175, 0, 25, 200), (175, 0, 25, 200), (175, 0, 25, 200)],
        cyc=[
            (255, 87, 87),
            (255, 90, 107),
            (255, 100, 112),
            (255, 100, 112),
            (242, 200, 251),
        ],
    ),
    PhaseColor(
        name='solar_noon',
        lamps_on=False,
        fill_light=[(200, 220, 190, 255), (200, 220, 190, 255), (200, 220, 190, 255)],
        cyc=[
            (255, 209, 171),
            (255, 216, 214),
            (255, 188, 112),
            (255, 228, 227),
            (255, 237, 199),
        ],
    ),
    PhaseColor(
        name='golden_hour',
        lamps_on=False,
        fill_light=[(255, 0, 20, 90), (255, 0, 20, 90), (255, 0, 20, 90)],
        cyc=[
            (255, 195, 166),
            (255, 222, 217),
            (255, 166, 115),
            (255, 156, 145),
            (255, 197, 158),
        ],
    ),
    PhaseColor(
        name='sunset',
        lamps_on=False,
        fill_light=[(200, 0, 10, 125), (200, 0, 10, 125), (200, 0, 10, 125)],
        cyc=[
            (227, 191, 255),
            (255, 223, 204),
            (255, 155, 97),
            (255, 137, 64),
            (255, 67, 20),
        ],
    ),
    PhaseColor(
        name='dusk',
        lamps_on=True,
        fill_light=[(15, 40, 20, 10) (15, 40, 20, 10), (15, 40, 20, 10)],
        cyc=[
            (255, 209, 253),
            (184, 198, 255),
            (255, 209, 253),
            (255, 209, 253),
            (255, 209, 253),
        ],
    ),
    PhaseColor(
        name='last_light',
        lamps_on=True,
        fill_light=[(0, 10, 0, 0), (0, 10, 0, 0), (0, 10, 0, 0)],
        cyc=[
            (145, 202, 255),
            (145, 202, 255),
            (145, 202, 255),
            (145, 202, 255),
            (145, 202, 255),
        ],
    ),
    PhaseColor(
        name='eod',
        lamps_on=True,
        fill_light=[(0, 40, 0, 20), (0, 40, 0, 20), (0, 40, 0, 20)],
        cyc=[
            (81, 85, 94),
            (77, 115, 255),
            (92, 79, 68),
            (91, 99, 115),
            (37, 37, 71),
        ],
    ),
]

def _interpolate_colors(start_color, end_color, steps):
    """
    Interpolates between two RGB or RGBW colors over a specified number of steps.

    :param start_color: Tuple representing the starting color (R, G, B) or (R, G, B, W).
    :param end_color: Tuple representing the ending color (R, G, B) or (R, G, B, W).
    :param steps: Number of interpolation steps.
    :return: List of tuples representing the interpolated colors.
    """
    # Check if the input colors are the same length
    if len(start_color) != len(end_color):
        raise ValueError("Start color and end color must have the same number of components")

    # Perform interpolation for each color component
    interpolated_values = [
        [
            round((i / (steps - 1)) * (end - start) + start)
            for i in range(steps)
        ]
        for start, end in zip(start_color, end_color)
    ]

    # Zip the interpolated values into tuples
    return list(zip(*interpolated_values))


def get_steps(phases):
    steps = []
    next_index = 1

    for phase in phases:
        # Get fill_light and next_fill_light
        fill_light_colors = next((pc.fill_light for pc in phase_colors if pc.name == phase.name), None)
        assert fill_light_colors is not None, f"No matching phase color found for phase name '{phase.name}'."

        next_fill_light_colors = next((pc.fill_light for pc in phase_colors if pc.name == phases[next_index].name), None)
        assert next_fill_light_colors is not None, f"No matching phase color found for phase name '{phases[next_index].name}'."

        # Interpolate fill_light
        fill_light_interpolated = [
            _interpolate_colors(fill_light_colors[i], next_fill_light_colors[i], phase.total_minutes)
            for i in range(len(fill_light_colors))
        ]

        # Get cyc colors and next_cyc colors
        cyc_colors = next((pc.cyc for pc in phase_colors if pc.name == phase.name), None)
        assert cyc_colors is not None, f"No matching phase color found for phase name '{phase.name}'."

        next_cyc_colors = next((pc.cyc for pc in phase_colors if pc.name == phases[next_index].name), None)
        assert next_cyc_colors is not None, f"No matching phase color found for phase name '{phases[next_index].name}'."

        # Interpolate cyc colors
        cyc_colors_interpolated = [
            _interpolate_colors(cyc_colors[i], next_cyc_colors[i], phase.total_minutes)
            for i in range(len(cyc_colors))
        ]

        for m in range(phase.total_minutes):
            # Combine interpolated values for fill_light and cyc
            interpolated_fill_light = [fill_light_interpolated[i][m] for i in range(len(fill_light_interpolated))]
            interpolated_cyc = [cyc_colors_interpolated[i][m] for i in range(len(cyc_colors_interpolated))]

            steps.append(
                Step(
                    time=phase.add_minutes(m),
                    lamps_on=phase.lamps_on,
                    phase_name=phase.name,
                    fill_light=interpolated_fill_light,
                    cyc=interpolated_cyc,
                )
            )

        # Wrap next index back to 0
        next_index += 1
        if next_index > len(phases) - 1:
            next_index = 0

    return steps
