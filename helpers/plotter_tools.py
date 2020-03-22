"""Functions to assist in plotting images."""

import os as os
import subprocess
from collections import defaultdict
from operator import itemgetter
from itertools import zip_longest, groupby
import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib import rcParams
from pylab import figure

rcParams["axes.labelsize"] = 14
rcParams["xtick.labelsize"] = 14
rcParams["ytick.labelsize"] = 14
rcParams["legend.fontsize"] = 12

rcParams["font.family"] = "Dejavu Sans"
rcParams["font.serif"] = ["Computer Modern Roman"]

rcParams["xtick.major.pad"] = 12
rcParams["ytick.major.pad"] = 12


def image_pager(img_list, horiz_n, vert_n, path_str, fin_prefix):
    """Concats a list of images into an NxN page using imagemagick ."""
    horiz_paste = grouper(img_list, horiz_n)
    vert_img_li = []
    for idx, row in enumerate(horiz_paste):
        img_name_li = [
            path_str + "/" + img_name for img_name in row if img_name is not None
        ]
        out_img_name = path_str + "/row_" + str(idx) + ".png"

        concat_images(file_li=img_name_li, outname=out_img_name, mode="horiz")
        vert_img_li.append(out_img_name)

    ###
    vert_paste = grouper(vert_img_li, vert_n)
    for idx, col in enumerate(vert_paste):
        img_name_li = [row for row in col if row is not None]
        out_img_name = path_str + fin_prefix + "_page_" + str(idx) + ".png"

        concat_images(file_li=img_name_li, outname=out_img_name, mode="vert")
    return None


def grouper(mylist, subli_size):
    """Collect data into fixed-length chunks or blocks
    grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"""

    args = [iter(mylist)] * subli_size

    return zip_longest(*args, fillvalue=None)


def concat_images(file_li, outname, mode="horiz", del_input=True):
    """Pastes inages into horizontal rows or vertical columns."""

    if mode == "horiz":
        append = "+append"
    elif mode == "vert":
        append = "-append"

    formated_cmd = ["convert", append]

    for file_name in file_li:
        formated_cmd.append(file_name)

    formated_cmd.append(outname)
    subprocess.call(formated_cmd)

    if del_input:
        for file_name in file_li:
            os.remove(file_name)

    return


def nested_line_plot(
    x_data=None,
    y_data=None,
    ls_var="--",
    col_var="RAND",
    lw_var=1.0,
    alpha1_var=0.5,
    title_var="null",
    fig_name="null.png",
    ylim_var=False,
    xlim_var=False,
    main_label=None,
    **kwargs
):
    """
       Multi-line function call. kwargs are dictionaries.
    """

    fig = figure()
    plt.xticks(rotation=15)
    plt.title(title_var)

    axhell = plt.subplot(1, 1, 1)

    axhell.grid(True)
    axhell.set_title(title_var)
    axhell.axhline(y=2.0, color="grey", linestyle="dashed", lw=1.5)

    if ylim_var:
        axhell.set_ylim(ylim_var)

    if xlim_var:
        axhell.set_xlim(x_data[0], x_data[-1])

    if col_var == "RAND":
        axhell.plot(
            x_data, y_data, ls=ls_var, lw=lw_var, alpha=alpha1_var, label=main_label
        )
    else:
        axhell.plot(
            x_data,
            y_data,
            ls=ls_var,
            color=col_var,
            lw=lw_var,
            alpha=alpha1_var,
            label=main_label,
        )

    # print additional lines if present
    if kwargs:
        for key, value in kwargs.items():
            aux_plot = {
                "xdat": None,
                "ydat": None,
                "ls": "-",
                "col": "k",
                "lw": 1.5,
                "alph": 1.0,
                "aux_lab": None,
                "mode": "line",
            }

            for subkey, subval in value.items():
                aux_plot[subkey] = subval

            if aux_plot["mode"] == "line":
                axhell.plot(
                    aux_plot["xdat"],
                    aux_plot["ydat"],
                    ls=aux_plot["ls"],
                    color=aux_plot["col"],
                    lw=aux_plot["lw"],
                    alpha=aux_plot["alph"],
                    label=aux_plot["aux_lab"],
                )
            elif aux_plot["mode"] == "scatter":
                axhell.scatter(
                    aux_plot["xdat"],
                    aux_plot["ydat"],
                    marker=aux_plot["ls"],
                    color=aux_plot["col"],
                    s=aux_plot["lw"],
                    alpha=aux_plot["alph"],
                )
            else:
                raise Exception("Extra line plotting mode not found")

    if main_label:
        axhell.set_leg = axhell.legend(loc="best", fancybox=True)
        axhell.set_leg.get_frame().set_alpha(0.5)

    plt.tight_layout(pad=0.9, w_pad=0.5, h_pad=1.0)
    plt.savefig(fig_name)
    plt.cla()
    plt.close(fig)

    return


def list_duplicates(seq):
    """Uses default dict to find index numbers of repeated
       elements in a sequence.
    """

    tally = defaultdict(list)
    for idx, item in enumerate(seq):
        tally[str(item)].append(idx)

    return tally


def split_list_on_missing_elem(in_list):
    """
    in: [1, 2, 3, 4, 6, 7, 8, 9, 10]
    out: [[1, 2, 3, 4], [6, 7, 8, 9, 10]]
    https://stackoverflow.com/questions/3149440/python-splitting-list-based-on-missing-numbers-in-a-sequence
    """

    idx_holder = []
    for k, g in groupby(enumerate(in_list), lambda i: i[0] - i[1]):
        subli = list(map(itemgetter(1), g))
        idx_holder.append(subli)
    return idx_holder


def viz_anamoly_plot(
    col_date, residuals, residual_mad, norm_counts, normc_median, img_path, myrigidity
):
    """Visualise the identified anomaly. Plots normalised counts and
       euclidian distances with anomaly highlighted in red.
    """

    # get indexes of anomalous points & corresponding y-axis valuesA
    anomalous_truth_mask = residuals["trig_anom"].tolist()
    anomalous_times = residuals.index.tolist()
    anomalous_nc_y = norm_counts[col_date].tolist()
    anomalous_ncres_y = residuals[col_date].tolist()

    # print("\nanomalous_truth_mask:", anomalous_truth_mask)
    # print("\nanomalous_times:", anomalous_times)
    # print("\nanomalous_nc_y:", anomalous_nc_y)
    # print("\nanomalous_ncres_y:", anomalous_ncres_y)
    # print("\n")

    # split anomalus lists into nested lists - to plot properly
    truth_idxes = list_duplicates(anomalous_truth_mask)
    split_idxes = split_list_on_missing_elem(truth_idxes["True"])

    # plot figure
    figx = figure()

    ax1 = figx.add_subplot(2, 1, 1)

    ax1.set_title("Anomaly Standardised Counts")
    ax1.grid(True)
    ax1.set_ylim(-1.75, 1.75)
    ax1.set_ylabel("Norm counts")
    ax1.set_xlabel("")
    ax1.set_xticklabels([])

    for sub_list in split_idxes:
        anom_time_sub = [anomalous_times[idx] for idx in sub_list]
        anom_ncy_sub = [anomalous_nc_y[idx] for idx in sub_list]

        ax1.plot(
            anom_time_sub,
            anom_ncy_sub,
            color="orangered",
            ls="-",
            lw=4.4,
            path_effects=[pe.Stroke(linewidth=4.6, foreground="black"), pe.Normal()],
            alpha=1.0,
        )

    ax1.plot(
        residuals[col_date].index,
        norm_counts[col_date],
        color="chartreuse",
        ls="-",
        lw=1.5,
        path_effects=[pe.Stroke(linewidth=2.0, foreground="black"), pe.Normal()],
        label="Event",
    )

    ax1.plot(
        residuals[col_date].index,
        normc_median["median_of_cols"],
        color="dodgerblue",
        ls="--",
        lw=1.5,
        label="Median",
    )

    ax1.set_leg = ax1.legend(loc="best", fancybox=True)
    ax1.set_leg.get_frame().set_alpha(0.5)

    ###
    ax2 = figx.add_subplot(2, 1, 2)
    ax2.set_title("Euclidian distances - myRig: " + str(myrigidity))
    ax2.grid(True)
    ax2.set_ylim(-0.05, 1.5)
    ax2.set_ylabel("Norm Abs counts")
    ax2.set_xlabel("Time")

    for sub_list in split_idxes:
        anom_time_sub = [anomalous_times[idx] for idx in sub_list]
        anom_ncresy_sub = [anomalous_ncres_y[idx] for idx in sub_list]
        ax2.plot(
            anom_time_sub,
            anom_ncresy_sub,
            color="orangered",
            ls="-",
            lw=4.4,
            path_effects=[pe.Stroke(linewidth=4.6, foreground="black"), pe.Normal()],
            alpha=1.0,
        )

    ax2.plot(
        residuals[col_date].index,
        residuals[col_date],
        color="chartreuse",
        ls="-",
        lw=1.5,
        path_effects=[pe.Stroke(linewidth=2.0, foreground="black"), pe.Normal()],
        label="Event residual",
    )

    ax2.plot(
        residuals[col_date].index,
        residual_mad["mad_of_myrig"],
        color="dodgerblue",
        ls="--",
        lw=1.5,
        label="Residual median",
    )

    ax2.set_leg = ax2.legend(loc="best", fancybox=True)
    ax2.set_leg.get_frame().set_alpha(0.5)

    for myax in figx.axes:
        matplotlib.pyplot.sca(myax)
        plt.xticks(rotation=15)

    plt.tight_layout(pad=0.9, w_pad=0.5, h_pad=1.0)
    plt.savefig(img_path + "anomalies_" + str(col_date) + ".png")
    plt.cla()
    plt.close(figx)

    return


def plot_err_bar_graphs(graph_data_dic):
    """Plot bar graphs with error bars."""

    y_vals_keys = ["median_li", "mean_li"]

    for y_key in y_vals_keys:
        fig_name = y_key + ".png"
        title_var = y_key

        y_vals = graph_data_dic[y_key]
        x_pos = list(range(0, len(y_vals), 1))
        print("\nCC", y_key, y_vals)

        fig = figure()
        plt.xticks(rotation=90)
        plt.title(title_var)

        ax1 = plt.subplot(1, 1, 1)

        ax1.grid(True)
        ax1.set_title(title_var)
        # ax1.axhline(y=2.0, color="grey", linestyle='dashed', lw=1.5)
        ax1.bar(
            x_pos,
            y_vals,
            width=0.8,
            color="g",
            ecolor="k",
            yerr=graph_data_dic["stddev_li"],
            tick_label=graph_data_dic["fn_li"],
            capsize=0.2,
            alpha=0.55,
        )

        # ax1.plot(x_axis, value)

        # xxxxxxxxxxxxxx

        plt.tight_layout(pad=0.9, w_pad=0.5, h_pad=1.0)
        # plt.show()
        plt.savefig(fig_name)
        plt.cla()
        plt.close(fig)
