# garden_light

Python scripts to run Ratington Manor Garden Lights on a Raspberry Pi. The system simulates a natural day/night lighting cycle across multiple light sources, with colors interpolated minute-by-minute based on real sunrise/sunset data for the location.

## Hardware

- **Raspberry Pi** — runs the control scripts, manages GPIO
- **SK6812 RGBW LED strip** — 144-pixel fill light driven via GPIO pin 18
- **WLED controller** (`192.168.1.168`) — controls a cyclorama/backdrop light split into 5 segments
- **GPIO relay** (pin 12) — switches physical lamps on/off based on time of day

## Architecture

### `main.py`
Entry point. Fetches sun phase times for the day, generates a list of per-minute color steps, and processes them in order — sleeping 60 seconds between each step (scaled by `DAY_CYCLES` for a compressed day simulation). Loops continuously, re-fetching phases each cycle. Registers GPIO cleanup on exit.

### `sunrisesunset_api.py`
Calls [api.sunrisesunset.io](https://sunrisesunset.io/api/) with a fixed lat/lng (Los Angeles area) to retrieve the following phase times each day:

`midnight` → `first_light` → `dawn` → `sunrise` → `solar_noon` → `golden_hour` → `sunset` → `dusk` → `last_light` → `eod`

### `color.py`
Defines target RGB/RGBW colors for each phase (`PhaseColor`). At runtime, colors are linearly interpolated between consecutive phases minute-by-minute, producing a smooth transition. Each minute becomes a `Step` with a timestamp, fill light colors, cyc colors, and lamp state.

### `garden_fill_light.py`
Drives the 144-pixel SK6812 RGBW NeoPixel strip. The strip cycles through a list of 3 colors, repeating the pattern across all pixels.

### `wled_api.py`
Sends HTTP POST requests to the WLED JSON API to set 5 independent LED segments. Each step applies a 55-second crossfade transition (`tt: 55000`) so changes blend smoothly into the next minute's colors.

### `realys.py`
Controls GPIO relay(s) to switch physical lamps. Lamps are on during nighttime phases (`midnight`, `first_light`, `dusk`, `last_light`, `eod`) and off during daylight phases.

### `model.py`
Pydantic models: `Phase` (a named time window with duration), `PhaseColor` (target colors per phase), and `Step` (a resolved per-minute lighting state).

## Day Cycle Compression

`DAY_CYCLES` in `main.py` controls how many full day/night cycles run in 24 hours. At `DAY_CYCLES = 4`, the sleep between steps is `60 / 4 = 15` seconds, compressing a full day into 6 hours.

## Running

```bash
sudo python3 ~/Desktop/garden_light/src/main.py
```

Use `-c` to clear the LED strip on exit:

```bash
sudo python3 ~/Desktop/garden_light/src/main.py -c
```

## Testing

```bash
sudo python3 ~/Desktop/garden_light/src/test/test_relay.py
```

## Dependencies

See `requirements.txt`. Key packages:

- `rpi_ws281x` — NeoPixel LED strip control
- `RPi.GPIO` — GPIO relay control
- `requests` — HTTP calls to sunrise/sunset API and WLED
- `pydantic` — data models and validation