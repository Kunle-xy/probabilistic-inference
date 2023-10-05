import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import argparse
from typing import List, Any, Union
import logging
import os, sys
print(sys.path)
sys.path.append(sys.path[0] + '/..')


from utils import helper
from src import main


# gaussian probability density function
class pdf():

  def __init__(self, data: pd.DataFrame):
    self.data = data
    self.x = np.array(data['X'])
    self.y = np.array(data['Y'])
    self.xy = np.array(data['XY'])
    self.x_var = np.square(np.std(self.x))
    self.x_err = np.std(self.x)
    self.y_var = np.square(np.std(self.y))
    self.y_err = np.std(self.y)
    self.xy_var = (np.mean(self.xy) - \
                      np.mean(self.y) * \
                      np.mean(self.x))
    self.corr  = self.xy_var/(self.x_err * self.y_err)

  def gaussian(self, a,b):
    c = 1 / (2* np.pi * self.x_err * self.y_err * np.sqrt(1-self.corr**2))
    d = -1 / (2 * (1-self.corr**2))
    e = (a - np.mean(self.x)) / self.x_err
    g = (b - np.mean(self.y)) /self.y_err
    return  1 * c * np.exp(d * ( e**2 - 2*self.corr*e*g + g**2))

# passes dataframe into pdf class and estaimates the probability

def item(gau1:pdf, gau2:pdf, section,xx, weight1, weight2):

  #  if both lines have equal weight or mass value
  if weight1 == weight2:
    items2 = [gau2.gaussian(section,y) for y in section] # object function for every point on the vertical section line
    items2 = items2/np.max(items2) # for each plot to have a peak of 1
    items1 = [gau1.gaussian(xx,y) for y in section] # object function
    items1 = items1/np.max(items1) # for each plot to have a peak of 1

  else: # when mass values are dissimilar
    items2 = [gau2.gaussian(xx,y) for y in section] # object function for every point on the vertical section line
    items1 = [gau1.gaussian(xx,y) for y in section] # object function for every point on the vertical section line
    item = np.concatenate((items2, items1), axis = 0) # fuses all probabilities
    item = item/np.max(item) # normalization

    items2 = item[:len(items2)] # fragment back to each line
    items1 = item[len(items2):] # fragment back to each line

  return items1, items2


def item_sing(gau3: pdf,section,xx,):
    items3 = [gau3.gaussian(xx,y) for y in section]
    items3 = items3/np.max(items3)
    return items3


# to plot combine map probability

def plot_boundaries(args:dict, xx, x_range,  action = ''):
  # combined scattered plots
    _, _, error1, error2, distance = helper.create_data(args, xx)

    y1a = helper.ypoint(args['line_1'], x_range, 'linear_margin', 2 * error1)
    # upper bound margin
    y1b = helper.ypoint(args['line_1'], x_range, 'linear_margin', 2 * error1) # lower bound margin

    y2a = helper.ypoint(args['line_2'], x_range, 'linear_margin', 2 * error2)
    # upper bound margin
    y2b = helper.ypoint(args['line_2'], x_range, 'linear_margin', 2 * error2)

    if distance > 0: # if line 1 is above line 2
        # end points for upper bound margin from line 1
        ls_up = list(zip(x_range,y1a)) # xcurve from earlier sample plots, upper bound margin
        ls_up.sort() # sort x,y values from left to right
        line_up = list(ls_up[0]) # picks and turn to list first end
        last_up = list(ls_up[-1]) # picks and turn to list second end
        line_up.extend(last_up) # extends list with second end

        y_up = helper.ypoint(line_up, xx) # finds the equation of line from points and corresponding y value at any point x

        # end points for lower bound margin from line 2
        ls_down = list(zip(x_range,y2b))  # xcurve from earlier sample plots, upper bound margin
        ls_down.sort() # sort x,y values from left to right
        line_down = list(ls_down[0]) # picks and turn to list first end
        last_down= list(ls_down[-1]) # picks and turn to list second end
        line_down.extend(last_down) # extends list with second end

        y_down = helper.ypoint(line_down, xx)  # finds the equation of line from points and corresponding y value at any point x

    else: # if line 2 is above line 1. same comment as above
        ls_down = list(zip(x_range,y1b))
        ls_down.sort()
        line_down = list(ls_down[0])
        last_down = list(ls_down[-1])
        line_down.extend(last_down)

        y_down = helper.ypoint(line_down, xx)

        ls_up = list(zip(x_range,y2a))
        ls_up.sort()
        line_up = list(ls_up [0])
        last_up= list(ls_up [-1])
        line_up.extend(last_up )

        y_up = helper.ypoint(line_up, xx)

    return np.array((y_up, y_down)) # returns the sum probabilities and value of y_up and y_down


    # helper function
def takeSecond(x):
    return x[1] #selects and returns second item in a list

def get_prob(args, df1, df2, section, xx):
    gau1 = pdf(df1) # object instance
    gau2 = pdf(df2) # object instance
    items1, items2 = item(gau1, gau2, section, xx, args['weight_1'], args['weight_2'])
    items3 = items1 + items2 # probability of line 1 + line 2
    items3 = items3/np.max(items3) # normalization
    return items3.tolist()
