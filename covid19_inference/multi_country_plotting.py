import pandas as pd
import numpy as np
import datetime
from covid19_inference import data_collection
import matplotlib.pyplot as plt

def boxplot_lambda(country, date, ax):
    other_vars = data_collection.read_variable(country, "other_vars")
    bd = other_vars["bd"].to_numpy()[0]
    diff_data_sim = other_vars["diff_data_sim"].to_numpy()[0]

    diff = (date-datetime.datetime.strptime(bd, "%Y-%m-%d")).days + diff_data_sim
    lambda_t = data_collection.read_variable(country, "lambda_t").to_numpy()
    fig, ax = plt.axes()
    ax.boxplot(lambda_t[:,diff])
    
    return ax

def boxplots_lambda(country, dates):

    other_vars = data_collection.read_variable(country, "other_vars")
    bd = other_vars["bd"].to_numpy()[0]
    diff_data_sim = other_vars["diff_data_sim"].to_numpy()[0]
    diff = []
    for date in dates:
        diff.append((date-datetime.datetime.strptime(bd, "%Y-%m-%d")).days + diff_data_sim)
    lambda_t = data_collection.read_variable(country, "lambda_t").to_numpy()
    ax = plt.axes()
    ax.boxplot(lambda_t[:,diff])
    mu = data_collection.read_variable(country, "mu").to_numpy()
    xlims = ax.get_xlim()
    ax.hlines(np.median(mu), xlims[0], xlims[1], linestyle="-")
    return ax