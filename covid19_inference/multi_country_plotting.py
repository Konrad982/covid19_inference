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


def boxplots_around_lockdown_one_country(country, distance=5, outliers=False):
    other_vars = data_collection.read_variable_country(country, "other_vars")
    lambda_t = data_collection.read_variable_country(country, "lambda_t")
    mu_all = data_collection.read_variable_country(country, "mu")

    datasets = list(other_vars.keys())

    height = int(np.ceil(len(datasets) / 2))
    fig, axes = plt.subplots(ncols=4, nrows=height, figsize=(18, 7 * height), gridspec_kw={"width_ratios": [2, 1, 2, 1]})
    plt.suptitle("lambda " + str(distance) + " days before and after the lockdown and ratio")
    y_low_lim = []
    y_up_lim = []

    for i in range(0, len(datasets)):
        lddate = other_vars[datasets[i]]["lockdown_date"].to_numpy()[0]
        lddate_normalstring = datetime.datetime.strptime(lddate, "%Y-%m-%d").strftime("%d/%m/%Y")
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
            ax = axes[2*i]
            plt.sca(ax)
        else:
            ax = axes[int(np.floor(i / 2))][2*(i % 2)]
            plt.sca(ax)
        ax.boxplot(lambda_t[datasets[i]].to_numpy()[:, diff])

        first_date = (datetime.datetime.strptime(lddate, "%Y-%m-%d") - datetime.timedelta(days=distance)).strftime("%d/%m/%Y")
        second_date = (datetime.datetime.strptime(lddate, "%Y-%m-%d") + datetime.timedelta(days=distance)).strftime("%d/%m/%Y")
        plt.xticks([1,2], [first_date, second_date])
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
            ax = axes[2*i + 1]
            plt.sca(ax)
        else:
            ax = axes[int(np.floor(i / 2))][2*(i % 2) + 1]
            plt.sca(ax)
        
        ratio = lambda_t[datasets[i]].to_numpy()[:, diff[0]] / lambda_t[datasets[i]].to_numpy()[:, diff[1]]
        if outliers:
            ax.boxplot(ratio, whis=(5,95))
        else:
            ax.boxplot(ratio, whis=(5,95), sym="")
        plt.ylabel("ratio " + datasets[i])
        plt.title("ratio boxplot")
        y_low_lim_2.append(ax.get_ylim()[0])
        y_up_lim_2.append(ax.get_ylim()[1])
        
        
    # finally adjust the limits 
    for i in range(0, len(datasets)):
        if len(datasets) <= 2:
            ax = axes[2*i]
        else:
            ax = axes[int(np.floor(i / 2))][2*(i % 2)]
        ax.set_ylim((min(y_low_lim), max(y_up_lim)))
        if len(datasets) <= 2:
            ax = axes[2*i + 1]
        else:
            ax = axes[int(np.floor(i / 2))][2*(i % 2) + 1]
        ax.set_ylim((min(y_low_lim_2), max(y_up_lim_2)))
        
        
        
    return
