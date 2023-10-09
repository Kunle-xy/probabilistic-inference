# import dependencies
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import argparse
from typing import List, Any, Union
import logging


def ypoint(line: List[int], x:int | np.ndarray, f_type: str=None, std_error:int = 0)-> int:
    """
    This function outputs point y using the equation of lie and x point.
    Args:

    """
    slope = (line[3] - line[1])/(line[2] - line[0])
    intercept = line[1] - slope * line[0]
    if f_type:

        if f_type.lower() == 'linear':
            y = x * slope + intercept
            return y
        elif f_type.lower() == 'linear_margin':
            y = x * slope + intercept + std_error
            return y
        else:
            logging.info(f" the f_type must be between ['linear', 'linear_margin']")
    else: return x * slope + intercept

def min_max(line1:List[int], line2:List[int]):
    min = sorted([line1[0], line2[0]])[0] # finds the minimum x value in the graph
    max = sorted([line1[2], line2[2]])[1]
    return min, max

def error(distance: int | float, weight: int | float):
   return np.sqrt(5 + distance * 20 * (1-weight))

def data_sampling(data_size:int, deviation: float | int, line:List[int],min, max,
                f_type: str=None, intercept:int = 0 ):
    np.random.seed(0)
    x = np.random.uniform(min, max, data_size)
    y = ypoint(line, x, f_type, intercept) + np.random.normal(0, deviation, len(x))
    return x, y

def create_data(args: dict, xx: float | int = min, f_type: str = None):

    line1 = args['line_1']
    line2 = args['line_2']
    weight1 = args['weight_1']
    weight2 = args['weight_2']
    data_size = args['data_size']

    line_y1 = ypoint(line1, xx)
    line_y2 = ypoint(line2, xx)

    distance = line_y1 - line_y2
    dist = abs(distance)

    standard_error1 = error(dist, weight1)
    standard_error2 =  error(dist, weight2)

    min, max = min_max(line1, line2)

    #iid samples to plot
    X1,Y1 = data_sampling(data_size, standard_error1, line1,min, max)# since linear, intt is not used
    X2,Y2 = data_sampling(data_size, standard_error2, line1,min, max) # #since linear, intt is not used

    df2 = pd.DataFrame([X2,Y2]).T
    df2 = df2.rename(columns = {0: 'X', 1: 'Y'})
    df2['XY'] = df2['X'] * df2['Y']

    df1 = pd.DataFrame([X1,Y1]).T
    df1 = df1.rename(columns = {0: 'X', 1: 'Y'})
    df1['XY'] = df1['X'] * df1['Y']

    return df1, df2,  standard_error1, standard_error2, distance


COLOR1 = '#FEF9E7'
COLOR2 = '#5E432E'

#red
# color1 = '#FB575D'
# color2 = '#15251B'

# color1 = "#8A5AC2"
# color2 = "#3575D5"

#used
# color1 = '#FEF9E7'
# color2 = '#5E432E'

# color1 = "#D4CC47"
# color2 = "#7C4D8B"

#generalized function for gradients of colors between two extreme colors
def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]


