import pandas as pd
import numpy as np
import datetime
from covid19_inference import data_collection
import matplotlib.pyplot as plt
import os


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


def boxplots_around_lockdown_one_country(country, distance=5):
    other_vars = data_collection.read_variable_country(country, "other_vars")
    lambda_t = data_collection.read_variable_country(country, "lambda_t")
    mu_all = data_collection.read_variable_country(country, "mu")

    datasets = list(other_vars.keys())

    height = int(np.ceil(len(datasets) / 2))
    fig, axes = plt.subplots(ncols=2, nrows=height, figsize=(14, 7 * height))

    y_low_lim = []
    y_up_lim = []

    for i in range(0, len(datasets)):
        bd = other_vars[datasets[i]]["bd"].to_numpy()[0]
        diff_data_sim = other_vars[datasets[i]]["diff_data_sim"].to_numpy()[0]
        lddate = other_vars[datasets[i]]["lockdown_date"].to_numpy()[0]
        ld_num = (
            datetime.datetime.strptime(lddate, "%Y-%m-%d")
            - datetime.datetime.strptime(bd, "%Y-%m-%d")
        ).days + diff_data_sim
        diff = [0, 0]
        diff[0] = ld_num - distance
        diff[1] = ld_num + distance
        if len(datasets) <= 2:
            ax = axes[i]
        else:
            ax = axes[int(np.floor(i / 2))][i % 2]
        ax.boxplot(lambda_t[datasets[i]].to_numpy()[:, diff])

        datetime.datetime.strptime(lddate, "%Y-%m-%d") + datetime.timedelta
        mu = mu_all[datasets[i]].to_numpy()
        xlims = ax.get_xlim()
        ax.hlines(np.median(mu), xlims[0], xlims[1], linestyle="-")
        y_low_lim.append(ax.get_ylim()[0])
        y_up_lim.append(ax.get_ylim()[1])

    for i in range(0, len(datasets)):
        if len(datasets) <= 2:
            ax = axes[i]
        else:
            ax = axes[int(np.floor(i / 2))][i % 2]
        ax.set_ylim((min(y_low_lim), max(y_up_lim)))
    return axes
