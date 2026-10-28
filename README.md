# Meteor Scatter 3D Explorer: Jupyter notebook version

An interactive notebook for building intuition about **VHF forward meteor scatter**: where a meteor trail has to be, and how it has to be moving, to produce a given Doppler shift on a TV carrier received off-air.

Default setup: WDPN-TV (Philadelphia, ch 2, 54.309441 MHz pilot) to a receiver near Washington DC, about a 210 km baseline. You can type in your own sites with the input form at the top of the notebook.

This folder is a notebook copy of the scripts in the `MS 3D Visualization` folder (`meteor_doppler_wdpn.py` and `meteor_3d_interactive.py`). The original scripts are unchanged.

## Files

| File | Purpose |
|---|---|
| `meteor_scatter_3d_form.ipynb` | **Start here.** Notebook with an input form: type your TX and RX sites, frequency and speed, and click a button. |
| `meteor_scatter_3d.ipynb` | Simpler first version. No form: you edit the settings cell by hand. |
| `meteor_3d_interactive.html` | Page written by the simpler notebook. It is rewritten each time that notebook runs. |
| `meteor_3d_interactive_form.html` | Page written by the form notebook (created the first time you run it). It can also be opened on its own in a browser. |

## What you need

- Python 3 with `numpy`, `matplotlib`, `plotly` and `ipywidgets`
- VS Code with the **Python** and **Jupyter** extensions (or any other Jupyter front end that supports widgets)

```bash
pip install numpy matplotlib plotly ipywidgets
```

## Running the form notebook

Open `meteor_scatter_3d_form.ipynb` and choose a Python kernel when VS Code asks.

1. **Choose Run All** (the toolbar button at the top of the notebook) the first time. The cells below the form define the constants, geometry functions, page template and helpers that the form needs, so they must run before the form can draw anything.
2. **Scroll back up to the Input form at the top of the notebook.** After Run All, VS Code jumps to the last cell, which is at the bottom. The results do not appear there; they appear **under the Update and run button** in the form. The last cell prints a reminder to scroll up.
3. Look under the button. You will find a summary, the two static plots, the tables and the interactive 3D explorer.
4. To try other values, change the fields in the form and click **Update and run**. You do not need to run anything else.

If you click **Update and run** before the cells below have run, the form says "Run the cells below this form first (Run All), then click again." Do that and click again.

### The form fields

| Field | Meaning |
|---|---|
| TX name | A label used in the page title and on the TX marker. |
| TX / RX latitude | Decimal degrees. North is positive. |
| TX / RX longitude | Decimal degrees. East is positive, so US longitudes are negative. |
| TX / RX height | Metres above the ellipsoid (antenna height above sea level, plus tower height for a real emitter). |
| Frequency (MHz) | Carrier frequency, for example `54.309441`. |
| Speed (km/s) | Meteor speed for the static plots. The interactive page has its own speed slider. |

Bad input (a latitude over 90, a non-positive frequency, sites less than 5 km apart or more than 1500 km apart) gives a one-line message instead of a plot.

### What adjusts automatically for a new baseline

The interactive page was designed around a 210 km baseline. When you click **Update and run**, these are scaled to your baseline length:

- the **Reflection point along path** slider range, step and starting position
- the three preset buttons (¼ from RX, midpoint, ¼ from TX)
- the **Offset from path** slider range and step
- the size of the ground patch
- the page title and TX marker, which use your TX name and frequency
- the offset label, which names the compass direction to the left when looking from RX toward TX (for example `+ = NW`)

The summary line below the form's output shows what was chosen, for example: `page scaled for a 824 km baseline: along-path +-412 km (presets +-206), offset +-990 km (+ = SE), ground patch +-1295 km`.

## Using the interactive 3D page

The page is the same explorer as in the main project:

- **3D view:** drag to rotate, scroll to zoom. It shows the ground, TX (red), RX (blue), the dashed baseline, the reflection point and the meteor trail as an arrow.
- **Blue shell:** the surface of constant TX to reflection point to RX path length. A meteor moving along it has zero Doppler.
- **Trail colour:** green when |f<sub>D</sub>| is 100 Hz or less at the reflection point, red when it is outside.
- **Sliders:** reflection point along the path, offset from the path, altitude, heading, descent angle and speed.
- **Set descent for 0 Hz:** solves for the descent angle that gives exactly 0 Hz at the current heading. If it reports no solution, the trail would have to climb, so try another heading.
- **Lower plot:** Doppler along the trail, with the ±100 Hz band shaded.

Doppler model: f<sub>D</sub> = −(v/λ) · v̂ · (û<sub>T</sub> + û<sub>R</sub>), where û<sub>T</sub> and û<sub>R</sub> point from the transmitter and receiver to the reflection point. A positive shift means the path is shortening.

## Notebook layout

| Cell | What it does |
|---|---|
| Input form (top) | The fields, the **Update and run** button and the results. |
| 1. Constants | WGS-84 constants, the speed of light, the ±100 Hz limit. |
| 2. Geometry functions | ECEF and East/North/Up conversions, bisector, Doppler, zero-Doppler descent, band width, heading windows (from `meteor_doppler_wdpn.py`). |
| 3. Page template | The HTML and JavaScript of the explorer (from `meteor_3d_interactive.py`). |
| 4. Helpers | The plot and table functions, `scale_page` (slider scaling), and `build_interactive` (writes the HTML page). |
| 5. Draw | Runs the form once, then prints the reminder to scroll up. |

## Modifying the code

- **Different sites or frequency:** use the form. No code changes are needed.
- **Default values in the form:** edit the numbers in the `num(...)` lines of the form cell.
- **The ±100 Hz threshold:** change `LIM` in the Constants cell. The interactive page has its own copy of this number, hard-coded in its JavaScript (search for `100` in the template).
- **Slider ranges, presets, labels:** these are rewritten by `scale_page` in the Helpers cell, using exact text replacements. If you edit the text in the page template (cell 3), update the matching `old` text in `scale_page` too. If a replacement cannot find its text, it raises an error naming it, rather than silently doing nothing.
- **Static plots and tables:** `show_static_plots` and `print_tables` in the Helpers cell.

## Troubleshooting

- **The notebook looks like an older version after I regenerated or updated it.** VS Code may still show a copy it opened earlier. Close the notebook tab and choose **Don't Save** (saving the stale copy would overwrite the new file), then reopen it from the Explorer.
- **The form is not visible after Run All.** It is at the top. Scroll up.
- **Clicking the button does nothing useful or shows the "Run the cells below" message.** Run All first.
- **The interactive page does not appear in the form output.** Some viewers block embedded pages. Open `meteor_3d_interactive_form.html` directly in a browser instead.
- **The page is blank or looks wrong after you edited the template.** Open the browser console (F12) for a JavaScript error. A stray character in an edited line is the usual cause.
- **A cell raises `ModuleNotFoundError`.** Install the missing package with the `pip` command above, then restart the kernel.

## Model limits

- Straight-line propagation with no refraction.
- Straight trails at constant speed. There is no deceleration or ablation model.
- Specular reflection geometry only. Trail orientation and the Fresnel-zone and reflection-condition constraints are not enforced. The page shows what the Doppler would be at a point, not whether that point is a viable reflector.
- The form accepts baselines from 5 km to 1500 km.
