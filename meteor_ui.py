"""Input form for the Meteor Scatter 3D Explorer notebook.

show_form() displays the fields, the buttons and four result tabs (Summary, Static plots, Tables,
3D explorer), then draws the results once with the default values. The maths lives in meteor_core.py.
"""
import traceback
import webbrowser
from pathlib import Path

import ipywidgets as w
from IPython.display import HTML, clear_output, display

import meteor_core as mc

# Starting values for the form (WDPN, Philadelphia ch 2, to a receiver near Washington DC)
DEFAULTS = dict(
    tx_name="WDPN", tx_lat=40.04169, tx_lon=-75.23614, tx_h=378.9,
    rx_name="Washington DC", rx_lat=38.821708, rx_lon=-77.103720, rx_h=100.0,
    freq=54.309441, speed=20.0, alt=100.0, lim=100.0,
)

_DESC_W = {"description_width": "125px"}
_FIELD = w.Layout(width="300px")
_BOX = w.Layout(border="1px solid #8885", padding="6px 10px", margin="0 8px 8px 0")


def _num(label, key, tip):
    return w.FloatText(value=DEFAULTS[key], description=label, description_tooltip=tip, style=_DESC_W, layout=_FIELD)


def _text(label, key, tip):
    return w.Text(value=DEFAULTS[key], description=label, description_tooltip=tip, style=_DESC_W, layout=_FIELD)


def _box(title, *fields):
    return w.VBox([w.HTML(f"<b>{title}</b>"), *fields], layout=_BOX)


def show_form():
    """Build and display the form, then draw the results once with the default values."""
    f = dict(
        tx_name=_text("Name", "tx_name", "Label used on the TX marker and the page title."),
        tx_lat=_num("Latitude (°)", "tx_lat", "Decimal degrees. North is positive."),
        tx_lon=_num("Longitude (°)", "tx_lon", "Decimal degrees. East is positive, so US longitudes are negative."),
        tx_h=_num("Height (m)", "tx_h", "Metres above the ellipsoid: ground elevation plus tower height."),
        rx_name=_text("Name", "rx_name", "Label used on the RX marker."),
        rx_lat=_num("Latitude (°)", "rx_lat", "Decimal degrees. North is positive."),
        rx_lon=_num("Longitude (°)", "rx_lon", "Decimal degrees. East is positive, so US longitudes are negative."),
        rx_h=_num("Height (m)", "rx_h", "Metres above the ellipsoid: ground elevation plus antenna height."),
        freq=_num("Frequency (MHz)", "freq", "Carrier frequency, for example the TV pilot carrier."),
        speed=_num("Speed (km/s)", "speed", "Meteor speed for the static plots and tables only. The 3D page has its own speed slider."),
        alt=_num("Altitude (km)", "alt", "Reflection-point altitude for the static plots and tables only. The 3D page has its own slider."),
        lim=_num("Doppler limit (Hz)", "lim", "Width of the 'near-zero Doppler' band (green on the 3D page, shaded on the plots)."),
    )
    numeric = [k for k in f if not k.endswith("name")]

    run = w.Button(description="Update and run", button_style="primary", icon="play",
                   tooltip="Recompute the plots, tables and 3D page with the values above.")
    reset = w.Button(description="Reset to defaults", icon="undo", tooltip="Put the WDPN to Washington DC values back in the fields.")
    swap = w.Button(description="Swap TX / RX", icon="exchange", tooltip="Exchange the transmitter and receiver fields.")
    browser = w.Button(description="Open 3D page in browser", icon="external-link", disabled=True,
                       tooltip="Open the interactive page in your web browser, full screen.")
    readout = w.HTML()
    outs = {name: w.Output() for name in ("Summary", "Static plots", "Tables", "3D explorer")}
    tabs = w.Tab(children=list(outs.values()))
    for i, name in enumerate(outs):
        tabs.set_title(i, name)

    state = {"dirty": False}

    def read_inputs():
        """Return the validated inputs as a dict, or raise ValueError with a message for the user."""
        v = {k: f[k].value for k in f}
        for k in numeric:
            if v[k] is None:
                raise ValueError("A field is empty.")
        if not (-90 <= v["tx_lat"] <= 90 and -90 <= v["rx_lat"] <= 90):
            raise ValueError("Latitudes must be between -90 and 90.")
        if not (-180 <= v["tx_lon"] <= 180 and -180 <= v["rx_lon"] <= 180):
            raise ValueError("Longitudes must be between -180 and 180 (US longitudes are negative).")
        if v["freq"] <= 0 or v["speed"] <= 0 or v["lim"] <= 0:
            raise ValueError("Frequency, speed and Doppler limit must be positive.")
        if not 30 <= v["alt"] <= 300:
            raise ValueError("Altitude should be between 30 and 300 km (meteor trails are typically 70 to 130 km).")
        d = mc.baseline_between((v["tx_lat"], v["tx_lon"]), (v["rx_lat"], v["rx_lon"]))
        if d < 5:
            raise ValueError(f"TX and RX are only {d:.1f} km apart; check the coordinates.")
        if d > 1500:
            raise ValueError(f"The baseline is {d:.0f} km, over the 1500 km this page is built for.")
        return v

    def update_readout(_=None):
        if _ is not None:                        # a field changed (not the call from on_run)
            state["dirty"] = True
        try:
            v = read_inputs()
        except ValueError as err:
            readout.value = f"<span style='color:#b42318'>&#9888; {err}</span>"
            return
        tx, rx = (v["tx_lat"], v["tx_lon"]), (v["rx_lat"], v["rx_lon"])
        brg = mc.bearing_deg(tx, rx)
        text = f"Baseline <b>{mc.baseline_between(tx, rx):.1f} km</b>, receiver is at bearing {brg:.0f}° ({mc.compass(brg)}) from the transmitter."
        if state["dirty"]:
            text += " <b>Fields changed: click Update and run to refresh the results below.</b>"
        readout.value = f"<span style='opacity:.8'>{text}</span>"

    def fill(out, caption, fn, *args):
        """Run fn inside an output area, with an optional HTML caption first; show any error there."""
        with out:
            clear_output(wait=True)
            if caption:
                display(HTML(f"<p style='max-width:900px'>{caption}</p>"))
            try:
                fn(*args)
            except Exception:
                traceback.print_exc()

    def show_3d(v):
        display(HTML(
            "<div style='max-width:900px'><b>How to use the 3D page:</b> drag to rotate and scroll to zoom. "
            "The sliders move the reflection point, the trail direction (heading and descent) and the meteor speed. "
            f"A <span style='color:#1a7f37'><b>green</b></span> trail gives |Doppler| &le; {v['lim']:g} Hz at the reflection point; "
            "<span style='color:#d62728'><b>red</b></span> is outside that. "
            "<i>Set descent for 0 Hz</i> finds the descent angle that gives exactly 0 Hz at the current heading."
            "<details><summary>Glossary</summary>"
            "<b>Heading</b>: compass direction the meteor travels, from north. "
            "<b>Descent</b>: angle of the trail below horizontal. "
            "<b>Reflection point</b>: the spot on the trail that scatters the signal from TX to RX. "
            "<b>Blue shell</b>: the surface of equal TX&rarr;point&rarr;RX path length. A meteor moving along it has zero Doppler. "
            "<b>Offset from path</b>: sideways distance of the reflection point from the TX&ndash;RX line."
            "</details></div>"))
        display(mc.build_interactive(v["tx_name"], v["rx_name"]))

    def on_run(_=None):
        run.disabled, run.description = True, "Working…"
        try:
            try:
                v = read_inputs()
            except ValueError as err:
                update_readout()
                with outs["Summary"]:
                    clear_output(wait=True)
                    print("Check the inputs:", err)
                return
            state["dirty"] = False
            update_readout()
            mc.configure((v["tx_lat"], v["tx_lon"], v["tx_h"]), (v["rx_lat"], v["rx_lon"], v["rx_h"]),
                         v["freq"], v["speed"], v["alt"], v["lim"])
            fill(outs["Summary"], None, mc.print_summary, v["tx_name"], v["rx_name"])
            fill(outs["Static plots"],
                 f"<b>Left:</b> for each heading, the line is the descent angle that gives exactly 0 Hz and the shading is the range "
                 f"within &plusmn;{v['lim']:g} Hz, for several reflection points. <b>Right:</b> Doppler for every heading and descent at the "
                 f"baseline midpoint (black lines are &plusmn;{v['lim']:g} Hz; dashed is 0 Hz). Speed {v['speed']:g} km/s, "
                 f"altitude {v['alt']:g} km.", mc.show_static_plots)
            fill(outs["Tables"],
                 "Read each row as: <i>if the meteor travels in this heading, it must descend at this angle to give 0 Hz</i>, "
                 "plus the range of angles that stay within the Doppler limit. The second table moves the reflection point "
                 "off the TX&ndash;RX line and lists the headings that work for a few descent angles.", mc.print_tables)
            fill(outs["3D explorer"], None, show_3d, v)
            browser.disabled = False
        except Exception:
            with outs["Summary"]:
                traceback.print_exc()
        finally:
            run.disabled, run.description = False, "Update and run"

    def on_reset(_):
        for k, widget in f.items():
            widget.value = DEFAULTS[k]

    def on_swap(_):
        for a, b in (("tx_name", "rx_name"), ("tx_lat", "rx_lat"), ("tx_lon", "rx_lon"), ("tx_h", "rx_h")):
            f[a].value, f[b].value = f[b].value, f[a].value

    def on_browser(_):
        webbrowser.open(Path(mc.PAGE_FILE).resolve().as_uri())

    for k in numeric:
        f[k].observe(update_readout, names="value")
    run.on_click(on_run)
    reset.on_click(on_reset)
    swap.on_click(on_swap)
    browser.on_click(on_browser)

    display(w.VBox([
        w.HBox([
            _box("Transmitter (TX)", f["tx_name"], f["tx_lat"], f["tx_lon"], f["tx_h"]),
            _box("Receiver (RX)", f["rx_name"], f["rx_lat"], f["rx_lon"], f["rx_h"]),
            _box("Signal and static plots", f["freq"], f["speed"], f["alt"], f["lim"]),
        ], layout=w.Layout(flex_flow="row wrap")),
        readout,
        w.HBox([run, reset, swap, browser]),
        tabs,
    ]))
    on_run()
