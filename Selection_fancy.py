#!/usr/bin/env python
import argparse
import textwrap
import webbrowser
from pathlib import Path
from shutil import copy
from subprocess import run

import numpy as np


def buildHTMLDiv(imagepath, index, name):
    return f"""
    <img src="{imagepath}"/>
    <div>
    <h2>{index}: {name}</h2>
    <input type="checkbox" id="{index}" class="checkbox">
    </div>
    """


def buildHTML(folder, N, wavelengths, excitation):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <link rel="stylesheet" href="stylesheet.css">
    </head>
    <body>
    <div class="grid">
    """
    for i in range(1, N + 1):
        html += buildHTMLDiv(
            folder / f"target{i:03}.png", i, f"{wavelengths[i-1]} Fe {excitation[i-1]}"
        )
    html += """
    </div>
    <button id="button">Save to file</button>

    <script src="data.js"></script>
    <script src="script.js"></script>

    </body>
    </html>
    """
    return html


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Select lines from line file",
        epilog=textwrap.dedent(
            """
            run as "python3 Selection.py <file with all Fe lines>.list <pdf with images>.pdf"
            """
        ),
    )
    parser.add_argument("input", type=str, help="Name of line file")
    parser.add_argument("pdf", type=str, help="Path to pdf file")

    args = parser.parse_args()

    file = Path(args.input)
    pdf = Path(args.pdf)
    # file = Path("AllFe.txt")
    # pdf = Path("Fe-HD26_5000g2.50m1.0z-0.70_HD26.int_m-0.7_t2.00_c-4.pdf")

    folder = Path(pdf.stem)
    folder.mkdir()

    (folder / "images").mkdir()
    run(["pdftohtml", "-c", pdf, folder / "images" / "target.html"])



    lines = np.loadtxt(file, dtype=str)
    data = lines[:, 0].astype(float)
    Excitation = lines[:, -2].astype(str)
    N = len(data)

    with open(folder / "data.js", "w") as f:
        f.write("data = " + str(list([list(x) for x in zip(data, Excitation)])))

    html = buildHTML(Path("images"), N, data, Excitation)
    with open(folder / "index.html", "w") as f:
        f.write(html)

    copy("stylesheet.css", folder)
    copy("script.js", folder)
    s = str(folder.resolve() / "index.html")
    print(s)
    webbrowser.open("file://" + s)
