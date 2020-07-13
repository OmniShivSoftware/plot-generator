import os
import io
import logging
import boto3
import base64
import matplotlib.pyplot as plt

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    (fig, subplots) = initialize_figure()
    populate_subplots(event, subplots)
    return figure_to_base64(fig)


def initialize_figure():
    fig = plt.figure(constrained_layout=False, figsize=(
        20.03, 13.46), frameon=False, dpi=144)
    img = plt.imread("report.png")
    plt.box(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img)
    fig.set_tight_layout({"pad": .0})
    gspec = fig.add_gridspec(nrows=2, ncols=3, figure=fig,
                             left=0.187, right=0.983, top=0.845, bottom=0.057,
                             hspace=0.40, wspace=0.28)

    subplots = [
        fig.add_subplot(gspec[0, 0], xlim=(0, 100), ylim=(0, 100)),
        fig.add_subplot(gspec[0, 1], xlim=(0, 100), ylim=(0, 100)),
        fig.add_subplot(gspec[0, 2], xlim=(0, 100), ylim=(0, 100)),
        fig.add_subplot(gspec[1, 0], xlim=(0, 100), ylim=(0, 100)),
        fig.add_subplot(gspec[1, 1], xlim=(0, 100), ylim=(0, 100)),
        fig.add_subplot(gspec[1, 2], xlim=(0, 100), ylim=(0, 100))
    ]

    for subplot in subplots:
        subplot.axis('off')
        subplot.patch.set_alpha(0)

    return (fig, subplots)


def populate_subplots(event, subplots):
    for idx in range(1, 7):
        points = event[str(idx)]
        x_list = list(map(lambda p: p["x"], points))
        y_list = list(map(lambda p: p["y"], points))
        label_list = list(map(lambda p: p["label"], points))
        subplot = subplots[idx - 1]
        subplot.scatter(x_list, y_list, c="black")
        for lidx, label in enumerate(label_list):
            x, y = x_list[lidx], y_list[lidx]
            x_text, ha_align = x_axis_position(x)
            y_text, va_align = y_axis_position(y)
            subplot.annotate(label, (x_text, y_text), va=va_align,
                             ha=ha_align, fontsize=16, family="Helvetica Neue")


def x_axis_position(x):
    if x < 30:
        return (x, "left")
    else:
        return (x + 1, "right")


def y_axis_position(y):
    if y < 30:
        return (y + 1, "bottom")
    else:
        return (y - 3, "top")


def figure_to_base64(fig):
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=fig.dpi)
    image_base64 = base64.b64encode(
        buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return image_base64
