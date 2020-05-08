import pandas as pd
import numpy as np
import os
from covid19_inference import plotting

def update_collection(country, trace=None,varnames=None, change_points=None, other_vars=None):
    """
    Saves the given data into a directory
    
    Parameters
    ----------
    filename: str
    country: str
    trace: pymc3 multitrace
    change_points: dictionary
    other_vars: dictionary, make sure to include the variables that you need later
    
    Returns
    -------
    None
    """
    try:
        os.chdir("results_collection")
    except FileNotFoundError:
        os.mkdir("results_collection")
        os.chdir("results_collection")
    
    try:
        os.chdir(country)
    except FileNotFoundError:
        os.mkdir(country)
        os.chdir(country)
        
    for varname in varnames:
        try:
            df = pd.DataFrame(trace[str(varname)])
        except:
            print("variable not found in trace")
        try:
            f= open(str(varname),"w+")
            f.write(df.to_csv(index=False))
            f.close()
        except TypeError:
            print("bad varname format, nothing written")
    
    try:
        df = pd.DataFrame(other_vars, index = [0])
        f = open("other_vars", "w+")
        f.write(df.to_csv(index=False))
        f.close()
    except TypeError:
        print("other_vars not a dictionary")
    
    try:
        df = pd.DataFrame(change_points)
        f = open("change_points", "w+")
        f.write(df.to_csv(index=False))
        f.close()
    except TypeError:
        print("change_points not a dictionary or index not found")
    
    os.chdir("..")
    os.chdir("..")
    
    return
    
def read_variable(country, variable):
    try:
        os.chdir("results_collection")
    except FileNotFoundError:
        os.mkdir("results_collection")
        os.chdir("results_collection")
    
    try:
        os.chdir(country)
    except FileNotFoundError:
        print("Country not found")
        return
        
    try:
        df = pd.read_csv(variable)
        os.chdir("..")
        os.chdir("..")
        return df
        
    except FileNotFoundError:
        print("variable not found")
        os.chdir("..")
        os.chdir("..")
    
        return
    