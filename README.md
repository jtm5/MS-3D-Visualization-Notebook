# Meteor Scatter 3D Explorer: Jupyter notebook version

An interactive notebook for building intuition about **VHF forward meteor scatter**: where a meteor trail has to be, and how it has to be moving, to produce a given Doppler shift on a TV carrier received off-air.

Default setup: WDPN-TV (Philadelphia, ch 2, 54.309441 MHz pilot) to a receiver near Washington DC, about a 210 km baseline. You can type in your own sites in the form at the bottom of the notebook.

## Files

| File | Purpose |
|---|---|
| `meteor_scatter_3d_form.ipynb` | **Start here.** A short notebook: intro, a package check, and the input form. |
| `meteor_ui.py` | The form: fields, buttons and result tabs. Default field values are at the top. |
| `meteor_core.py` | The calculations: geometry and Doppler functions, the 3D page template, plots, tables and the page builder. |
| `meteor_scatter_3d.ipynb` | Simpler first version, with no form. You edit the settings cell by hand. It is self-contained and does not use the two `.py` files. |
| `meteor_3d_interactive_form.html` | Page written by the form notebook each time you click **Update and run**. It can also be opened on its own in a browser. |
| `meteor_3d_interactive.html` | Page written by the simpler notebook. |

Keep the notebook, `meteor_ui.py` and `meteor_core.py` in the same folder.

## What you need

- Python 3 with `numpy`, `matplotlib`, `plotly` and `ipywidgets`
- VS Code with the **Python** and **Jupyter** extensions (or any other Jupyter front end that supports widgets)

```bash
pip install numpy matplotlib plotly ipywidgets
```

## Using the notebook

1. Open `meteor_scatter_3d_form.ipynb` and choose a Python kernel when VS Code asks.
2. Choose **Run All** (toolbar at the top). There are three code cells: a package check, the form, and one that draws the first results into the form's tabs (scroll back up to see them).
3. Change the fields and click **Update and run**. Nothing else needs to be run again.

The results appear under the buttons in four tabs:

| Tab | Contents |
|---|---|
| Summary | The setup in plain language: baseline length and bearing, wavelength, the largest possible Doppler, and what share of random trail directions stay within the Doppler limit. |
| Static plots | Left: zero-Doppler line and ±limit band against heading and descent, for several reflection points. Right: Doppler map at the baseline midpoint. |
| Tables | Heading to descent angle tables for 0 Hz and for the ±limit window, at the midpoint and off the baseline. |
| 3D explorer | The interactive page, with a short how-to and glossary above it. |

### The form

While you type, a line under the fields shows the baseline length and bearing, or a red message if an input is not valid. After the first run it also tells you when the fields have changed and the results need refreshing.

| Field | Meaning |
|---|---|
| Name (TX and RX) | Labels for the markers and the page title. |
| Latitude | Decimal degrees. North is positive. |
| Longitude | Decimal degrees. East is positive, so US longitudes are negative. |
| Height (m) | Metres above the ellipsoid (ground elevation plus tower or antenna height). |
| Frequency (MHz) | Carrier frequency, for example `54.309441`. |
| Speed (km/s) | Meteor speed for the **static plots and tables only**. The 3D page has its own speed slider. |
| Altitude (km) | Reflection-point altitude for the **static plots and tables only**. The 3D page has its own altitude slider. |
| Doppler limit (Hz) | Width of the "near-zero Doppler" band. It sets the shaded bands, the table windows and the green/red threshold on the 3D page. |

Buttons: **Update and run**; **Reset to defaults** (puts the WDPN example values back in the fields); **Swap TX / RX**; **Open 3D page in browser** (opens the full-size page; available after the first run).

Bad input (a latitude over 90, a non-positive frequency, sites less than 5 km or more than 1500 km apart) gives a message instead of plots.

### What adjusts automatically for a new baseline

The interactive page was designed around a 210 km baseline. When you click **Update and run**, these are scaled to your baseline length:

- the **Reflection point along path** slider range, step and starting position
- the three preset buttons (¼ from RX, midpoint, ¼ from TX)
- the **Offset from path** slider range and step
- the size of the ground patch
- the page title, TX and RX markers, and the Doppler limit
- the offset label, which names the compass direction to the left when looking from RX toward TX (for example `+ = NW`)

## Using the interactive 3D page

- **3D view:** drag to rotate, scroll to zoom. It shows the ground, TX (red), RX (blue), the dashed baseline, the reflection point and the meteor trail as an arrow.
- **Blue shell:** the surface of constant TX to reflection point to RX path length. A meteor moving along it has zero Doppler.
- **Trail colour:** green when |f<sub>D</sub>| is within the Doppler limit at the reflection point, red when it is outside.
- **Sliders:** reflection point along the path, offset from the path, altitude, heading, descent angle and speed.
- **Set descent for 0 Hz:** solves for the descent angle that gives exactly 0 Hz at the current heading. If it reports no solution, the trail would have to climb, so try another heading.
- **Lower plot:** Doppler along the trail, with the limit band shaded.

Doppler model: f<sub>D</sub> = −(v/λ) · v̂ · (û<sub>T</sub> + û<sub>R</sub>), where û<sub>T</sub> and û<sub>R</sub> point from the transmitter and receiver to the reflection point. A positive shift means the path is shortening.

## Modifying the code

If you edit `meteor_core.py` or `meteor_ui.py`, restart the kernel and Run All again so the notebook picks up the change.

- **Default values in the form:** `DEFAULTS` at the top of `meteor_ui.py`.
- **Form layout, tabs, captions and messages:** `meteor_ui.py`.
- **Geometry and Doppler maths:** the "Geometry functions" section of `meteor_core.py`. `configure()` sets the site and signal values these functions read.
- **Static plots, tables and summary text:** `show_static_plots`, `print_tables` and `print_summary` in `meteor_core.py`.
- **The 3D page:** the `PAGE` template in `meteor_core.py`. Slider ranges, presets, labels and the Doppler limit are rewritten by `scale_page` using exact text replacements. If you edit the text in `PAGE`, update the matching `old` text in `scale_page` too. If a replacement cannot find its text, it raises an error naming it rather than silently doing nothing.

## Troubleshooting

- **The first cell stops with "Missing packages".** Run the `pip install` line it prints, restart the kernel, and Run All again.
- **`ModuleNotFoundError: meteor_ui` or `meteor_core`.** The notebook must be in the same folder as the two `.py` files, and the kernel must have started in that folder (VS Code does this when you open the notebook from the Explorer).
- **I changed a `.py` file and nothing changed.** Restart the kernel and Run All again.
- **The 3D page does not appear in its tab.** Some viewers block embedded pages. Click **Open 3D page in browser**, or open `meteor_3d_interactive_form.html` directly.
- **The 3D page is blank or looks wrong after you edited the template.** Open the browser console (F12) for a JavaScript error. A stray character in an edited line is the usual cause.
- **The notebook looks like an older version.** VS Code may still show a copy it opened earlier. Close the notebook tab and choose **Don't Save** (saving the stale copy would overwrite the new file), then reopen it from the Explorer.

## Model limits

- Straight-line propagation with no refraction.
- Straight trails at constant speed. There is no deceleration or ablation model.
- Specular reflection geometry only. Trail orientation and the Fresnel-zone and reflection-condition constraints are not enforced. The page shows what the Doppler would be at a point, not whether that point is a viable reflector.
- The form accepts baselines from 5 km to 1500 km.
