import pandas as pd
import numpy as np
import datetime
from covid19_inference import data_collection
import matplotlib.pyplot as plt
import os
import plotly.graph_objs as go
from IPython.display import display, Markdown


def boxplot_lambda(country, dataset, date, ax):
    other_vars = data_collection.read_variable(country, dataset, "other_vars")
    bd = other_vars["bd"].to_numpy()[0]
    diff_data_sim = other_vars["diff_data_sim"].to_numpy()[0]

    diff = (date - datetime.datetime.strptime(bd, "%Y-%m-%d")).days + diff_data_sim
    lambda_t = data_collection.read_variable(country, dataset, "lambda_t").to_numpy()
    fig, ax = plt.axes()
    ax.boxplot(lambda_t[:, diff])

    return ax


def boxplots_lambda(country, dataset, dates):

    other_vars = data_collection.read_variable(country, dataset, "other_vars")
    bd = other_vars["bd"].to_numpy()[0]
    diff_data_sim = other_vars["diff_data_sim"].to_numpy()[0]
    diff = []
    for date in dates:
        diff.append(
            (date - datetime.datetime.strptime(bd, "%Y-%m-%d")).days + diff_data_sim
        )
    lambda_t = data_collection.read_variable(country, dataset, "lambda_t").to_numpy()
    ax = plt.axes()
    ax.boxplot(lambda_t[:, diff])
    mu = data_collection.read_variable(country, dataset, "mu").to_numpy()
    xlims = ax.get_xlim()
    ax.hlines(np.median(mu), xlims[0], xlims[1], linestyle="-")
    return ax


def boxplots_around_lockdown_one_country(country, distance=5, outliers=False):
    if outliers:
        print("The whiskers show 0.05 and 0.95 quantiles, outliers enabled")
    else:
        print("The whiskers show 0.05 and 0.95 quantiles, outliers disabled")
    other_vars = data_collection.read_variable_country(country, "other_vars")
    lambda_t = data_collection.read_variable_country(country, "lambda_t")
    mu_all = data_collection.read_variable_country(country, "mu")

    datasets = list(other_vars.keys())

    height = int(np.ceil(len(datasets) / 2))
    fig, axes = plt.subplots(
        ncols=4,
        nrows=height,
        figsize=(18, 7 * height),
        gridspec_kw={"width_ratios": [2, 1, 2, 1]},
    )
    plt.suptitle(
        "lambda " + str(distance) + " days before and after the lockdown and ratio"
    )
    y_low_lim = []
    y_up_lim = []

    for i in range(0, len(datasets)):
        lddate = other_vars[datasets[i]]["lockdown_date"].to_numpy()[0]
        lddate_normalstring = datetime.datetime.strptime(lddate, "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        )
        bd = other_vars[datasets[i]]["bd"].to_numpy()[0]
        diff_data_sim = other_vars[datasets[i]]["diff_data_sim"].to_numpy()[0]

        ld_num = (
            datetime.datetime.strptime(lddate, "%Y-%m-%d")
            - datetime.datetime.strptime(bd, "%Y-%m-%d")
        ).days + diff_data_sim
        diff = [0, 0]
        diff[0] = ld_num - distance
        diff[1] = ld_num + distance
        if len(datasets) <= 2:
            ax = axes[2 * i]
            plt.sca(ax)
        else:
            ax = axes[int(np.floor(i / 2))][2 * (i % 2)]
            plt.sca(ax)
        if outliers:
            ax.boxplot(lambda_t[datasets[i]].to_numpy()[:, diff], whis=(5, 95))
        else:
            ax.boxplot(lambda_t[datasets[i]].to_numpy()[:, diff], sym="", whis=(5, 95))

        first_date = (
            datetime.datetime.strptime(lddate, "%Y-%m-%d")
            - datetime.timedelta(days=distance)
        ).strftime("%d/%m/%Y")
        second_date = (
            datetime.datetime.strptime(lddate, "%Y-%m-%d")
            + datetime.timedelta(days=distance)
        ).strftime("%d/%m/%Y")
        plt.xticks([1, 2], [first_date, second_date])
        plt.title(datasets[i] + " dataset, lockdown: " + lddate_normalstring)
        plt.xlabel("date")
        plt.ylabel("boxplot of lambda, black line for mu")

        mu = mu_all[datasets[i]].to_numpy()
        xlims = ax.get_xlim()
        ax.hlines(np.median(mu), xlims[0], xlims[1], linestyle="-")
        y_low_lim.append(ax.get_ylim()[0])
        y_up_lim.append(ax.get_ylim()[1])

    y_low_lim_2 = []
    y_up_lim_2 = []
    for i in range(0, len(datasets)):
        if len(datasets) <= 2:
            ax = axes[2 * i + 1]
            plt.sca(ax)
        else:
            ax = axes[int(np.floor(i / 2))][2 * (i % 2) + 1]
            plt.sca(ax)

        ratio = (
            lambda_t[datasets[i]].to_numpy()[:, diff[0]]
            / lambda_t[datasets[i]].to_numpy()[:, diff[1]]
        )
        if outliers:
            ax.boxplot(np.log(ratio), whis=(5, 95))
        else:
            ax.boxplot(np.log(ratio), whis=(5, 95), sym="")
        plt.ylabel("log ratio " + datasets[i])
        plt.title("log ratio\nbefore/after boxplot")
        y_low_lim_2.append(ax.get_ylim()[0])
        y_up_lim_2.append(ax.get_ylim()[1])

    # finally adjust the limits
    for i in range(0, len(datasets)):
        if len(datasets) <= 2:
            ax = axes[2 * i]
        else:
            ax = axes[int(np.floor(i / 2))][2 * (i % 2)]
        ax.set_ylim((min(y_low_lim), max(y_up_lim)))
        if len(datasets) <= 2:
            ax = axes[2 * i + 1]
        else:
            ax = axes[int(np.floor(i / 2))][2 * (i % 2) + 1]
        ax.set_ylim((min(y_low_lim_2), max(y_up_lim_2)))

    return


def plotly_violins_all_available_lambda(distances=5, around="lockdown", refdate=None):
    # if distances is an integer, make a tuple.
    if isinstance(distances, int):
        distances = (distances, distances)

    # tell what's going on
    display(
        Markdown(
            "# Violin plots of $\lambda -\mu$ for each of the countries / datasets found \n"
            + str(distances[0])
            + " days before and "
            + str(distances[1])
            + " days after lockdown\n"
        )
    )

    # get country names in results_collection folder
    countries = data_collection.get_countries()

    traces = []
    current = 0
    # we assume generally mu=0.125
    mu = 0.125
    printhosp = False
    printnew_gvt = False
    printJHU = False

    md_table = "|Country|Dataset|lockdown date |lockdown type|data retrieved|\n|:---|:---|:---|:---|:---|\n"
    for country in countries:
        other_vars = data_collection.read_variable_country(country, "other_vars")
        lambda_t = data_collection.read_variable_country(country, "lambda_t")

        # get dataset names
        datasets = list(other_vars.keys())

        for i in range(0, len(datasets)):
            bd = other_vars[datasets[i]]["bd"].to_numpy()[0]
            diff_data_sim = other_vars[datasets[i]]["diff_data_sim"].to_numpy()[0]

            if around == "lockdown":
                lddate = other_vars[datasets[i]]["lockdown_date"].to_numpy()[0]
                ldtype = other_vars[datasets[i]]["lockdown_type"].to_numpy()[0]
                lddate_normalstring = datetime.datetime.strptime(
                    lddate, "%Y-%m-%d"
                ).strftime("%d/%m/%Y")

                ld_num = (
                    datetime.datetime.strptime(lddate, "%Y-%m-%d")
                    - datetime.datetime.strptime(bd, "%Y-%m-%d")
                ).days + diff_data_sim

                diff_0 = ld_num - distances[0]
                diff_1 = ld_num + distances[1]

                date_0_string = (
                    datetime.datetime.strptime(lddate, "%Y-%m-%d")
                    - datetime.timedelta(days=distances[0])
                ).strftime("%d/%m/%Y")
                date_1_string = (
                    datetime.datetime.strptime(lddate, "%Y-%m-%d")
                    + datetime.timedelta(days=distances[1])
                ).strftime("%d/%m/%Y")

            if datasets[i] == "hospitalisations":
                name_0 = country + " hosp " + date_0_string
                name_1 = country + " hosp " + date_1_string
                md_table = (
                    md_table
                    + "|"
                    + country
                    + "|hosp|"
                    + lddate_normalstring
                    + "|"
                    + ldtype
                )
                printhosp = True
            elif datasets[i] == "new_cases_government_data":
                name_0 = country + " new_gvt " + date_0_string
                name_1 = country + " new_gvt " + date_1_string
                md_table = (
                    md_table
                    + "|"
                    + country
                    + "|new_gvt|"
                    + lddate_normalstring
                    + "|"
                    + ldtype
                )
                printnew_gvt = True
            elif datasets[i] == "new_lab":
                name_0 = country + " new_lab " + date_0_string
                name_1 = country + " new_lab " + date_1_string
                md_table = (
                    md_table
                    + "|"
                    + country
                    + "|new_lab|"
                    + lddate_normalstring
                    + "|"
                    + ldtype
                )
                printnew_lab = True
            else:
                if datasets[i] == "JHU":
                    printJHU = True
                name_0 = country + " " + datasets[i] + " " + date_0_string
                name_1 = country + " " + datasets[i] + " " + date_1_string
                md_table = (
                    md_table
                    + "|"
                    + country
                    + "|"
                    + datasets[i]
                    + "|"
                    + lddate_normalstring
                    + "|"
                    + ldtype
                )

            if "data_retrieval" in list(other_vars[datasets[i]].keys()):
                md_table = (
                    md_table
                    + "|"
                    + other_vars[datasets[i]]["data_retrieval"].to_numpy()[0]
                    + "|\n"
                )
            else:
                md_table = md_table + "| |\n"

            # x_0 = [date_0_string for i in range(0, len(lambda_t[datasets[i]].to_numpy()[:,diff_0]))]
            # x_1 = [date_1_string for i in range(0, len(lambda_t[datasets[i]].to_numpy()[:,diff_1]))]

            raw_data = lambda_t[datasets[i]].to_numpy()[:, diff_0]
            processed_data = raw_data[
                np.logical_and(
                    np.quantile(raw_data, 0.05) < raw_data,
                    raw_data < np.quantile(raw_data, 0.95),
                )
            ]
            traces.append(
                go.Violin(
                    y=processed_data - mu,
                    name=name_0,
                    legendgroup=name_0,
                    meanline_visible=True,
                    box={"visible": False},
                    points=False,
                )
            )
            raw_data = lambda_t[datasets[i]].to_numpy()[:, diff_1]
            processed_data = raw_data[
                np.logical_and(
                    np.quantile(raw_data, 0.05) < raw_data,
                    raw_data < np.quantile(raw_data, 0.95),
                )
            ]
            traces.append(
                go.Violin(
                    y=processed_data - mu,
                    name=name_1,
                    legendgroup=name_1,
                    meanline_visible=True,
                    box={"visible": False},
                    points=False,
                )
            )
            # traces.append(go.Scatter(x=[current, current + 1], y=[mu, mu], legendgroup = name_1, mode="lines", line=dict(color="black")))
    display(Markdown(md_table))
    md_table = ""
    if printJHU or printnew_gvt or printhosp or printnew_lab:
        md_table = "|Abbreviation|Meaning| \n|:---|:---|\n"
        if printJHU:
            md_table = md_table + "|JHU|Data from Johns Hopkins university|\n"
        if printnew_gvt:
            md_table = (
                md_table
                + "|new_gvt|New cases according to government data of the respective country|\n"
            )
        if printhosp:
            md_table = (
                md_table
                + "|hosp|New hospitalisations according to government data of the respective country|\n"
            )
        if printnew_lab:
            md_table = (
                md_table
                + "|new_lab|France-specific, positive tests of a part of the laboratories (*laboratoires de ville*)|\n"
            )

    md_table = (
        md_table
        + "\n For the links to the sources, see the readme of the repository.\n\n"
    )
    md_table = (
        md_table
        + "__Data has been pre-processed to include only data between 0.05 and 0.95 quantiles. The following plots are interactive, by clicking on a legend item, the corresponding plot will disappear. Double-click to isolate.__\n\n"
    )
    display(Markdown(md_table))
    figure = go.Figure(
        data=traces,
        layout={
            "title": {"text": r"$\lambda - \mu\text{, violin plots, with }\mu=0.125$"},
            "height": 700,
        },
    )

    # figure.add_shape(
    #        type="line",
    #        x0=-1,
    #        y0=mu,
    #        x1=len(traces),
    #        y1=mu,
    #        line=dict(
    #            color="Black",
    #            width=2,
    #        ),
    #        name ="mu"
    # )
    return figure


def plotly_violins_all_available_ratio(distances=5, around="lockdown", refdate=None):
    # if distances is an integer, make a tuple.
    if isinstance(distances, int):
        distances = (distances, distances)

    # tell what's going on
    display(
        Markdown(
            "# Violin plots of the ratio of $\lambda$ for each of the countries / datasets found \n"
            + str(distances[1])
            + " days after and "
            + str(distances[0])
            + " days before lockdown\n"
        )
    )

    # get country names in results_collection folder
    countries = data_collection.get_countries()

    traces = []
    current = 0
    # we assume generally mu=0.125
    mu = 0.125
    printhosp = False
    printnew_gvt = False
    printJHU = False

    md_table = "|Country|Dataset|lockdown date |lockdown type|data retrieved|\n|:---|:---|:---|:---|:---|\n"
    for country in countries:
        other_vars = data_collection.read_variable_country(country, "other_vars")
        lambda_t = data_collection.read_variable_country(country, "lambda_t")

        # get dataset names
        datasets = list(other_vars.keys())

        for i in range(0, len(datasets)):
            bd = other_vars[datasets[i]]["bd"].to_numpy()[0]
            diff_data_sim = other_vars[datasets[i]]["diff_data_sim"].to_numpy()[0]

            if around == "lockdown":
                lddate = other_vars[datasets[i]]["lockdown_date"].to_numpy()[0]
                ldtype = other_vars[datasets[i]]["lockdown_type"].to_numpy()[0]
                lddate_normalstring = datetime.datetime.strptime(
                    lddate, "%Y-%m-%d"
                ).strftime("%d/%m/%Y")

                ld_num = (
                    datetime.datetime.strptime(lddate, "%Y-%m-%d")
                    - datetime.datetime.strptime(bd, "%Y-%m-%d")
                ).days + diff_data_sim

                diff_0 = ld_num - distances[0]
                diff_1 = ld_num + distances[1]

            if datasets[i] == "hospitalisations":
                name = country + " " + "hosp" + " around " + lddate_normalstring
                md_table = (
                    md_table
                    + "|"
                    + country
                    + "|hosp|"
                    + lddate_normalstring
                    + "|"
                    + ldtype
                )
                printhosp = True
            elif datasets[i] == "new_cases_government_data":
                name = country + " " + "new_gvt" + " around " + lddate_normalstring
                md_table = (
                    md_table
                    + "|"
                    + country
                    + "|new_gvt|"
                    + lddate_normalstring
                    + "|"
                    + ldtype
                )
                printnew_gvt = True
            elif datasets[i] == "new_lab":
                name = country + " " + "new_lab" + " around " + lddate_normalstring
                md_table = (
                    md_table
                    + "|"
                    + country
                    + "|new_lab|"
                    + lddate_normalstring
                    + "|"
                    + ldtype
                )
                printnew_lab = True
            else:
                if datasets[i] == "JHU":
                    printJHU = True
                name = country + " " + datasets[i] + " around " + lddate_normalstring
                md_table = (
                    md_table
                    + "|"
                    + country
                    + "|"
                    + datasets[i]
                    + "|"
                    + lddate_normalstring
                    + "|"
                    + ldtype
                )

            if "data_retrieval" in list(other_vars[datasets[i]].keys()):
                md_table = (
                    md_table
                    + "|"
                    + other_vars[datasets[i]]["data_retrieval"].to_numpy()[0]
                    + "|\n"
                )
            else:
                md_table = md_table + "| |\n"

            # x_0 = [date_0_string for i in range(0, len(lambda_t[datasets[i]].to_numpy()[:,diff_0]))]
            # x_1 = [date_1_string for i in range(0, len(lambda_t[datasets[i]].to_numpy()[:,diff_1]))]

            raw_data = lambda_t[datasets[i]].to_numpy()[:, diff_0]
            raw_data_2 = lambda_t[datasets[i]].to_numpy()[:, diff_1]
            quotient = np.divide(raw_data, raw_data_2)
            processed_quotient = quotient[
                np.logical_and(
                    np.quantile(quotient, 0.05) < quotient,
                    quotient < np.quantile(quotient, 0.95),
                )
            ]
            traces.append(
                go.Violin(
                    y=processed_quotient,
                    name=name,
                    legendgroup=name,
                    meanline_visible=True,
                    box={"visible": False},
                    points=False,
                )
            )
            # traces.append(go.Scatter(x=[current, current + 1], y=[mu, mu], legendgroup = name_1, mode="lines", line=dict(color="black")))
    display(Markdown(md_table))
    md_table = ""
    if printJHU or printnew_gvt or printhosp or printnew_lab:
        md_table = "|Abbreviation|Meaning| \n|:---|:---|\n"
        if printJHU:
            md_table = md_table + "|JHU|Data from Johns Hopkins university|\n"
        if printnew_gvt:
            md_table = (
                md_table
                + "|new_gvt|New cases according to government data of the respective country|\n"
            )
        if printhosp:
            md_table = (
                md_table
                + "|hosp|New hospitalisations according to government data of the respective country|\n"
            )
        if printnew_lab:
            md_table = (
                md_table
                + "|new_lab|France-specific, positive tests of a part of the laboratories (*laboratoires de ville*)|\n"
            )

    md_table = (
        md_table
        + "\n For the links to the sources, see the readme of the repository.\n\n"
    )
    md_table = (
        md_table
        + "__After calculating the ratio, only the ratios between the 0.05 and 0.95 quantiles are plotted. The following plots are interactive, by clicking on a legend item, the corresponding plot will disappear. Double-click to isolate.__\n\n"
    )
    display(Markdown(md_table))
    figure = go.Figure(data=traces, layout={"title": {"text": r""}, "height": 700,},)
    return figure
