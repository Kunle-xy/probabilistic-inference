# import dependencies
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import argparse
from typing import List, Any, Union
import logging
import os, sys
print(sys.path)
sys.path.append(sys.path[0] + '/..')

from utils import helper, probability

DATA_SIZE = 200

def argument():
    parser = argparse.ArgumentParser(description='A sample argument parser')
    parser.add_argument('--line_1','-l_1', type=int, \
                        nargs = "+", help='[x1, y1, x2, y2]', required = True)
    parser.add_argument('--line_2','-l_2', type=int, \
                        nargs = "+", help='[x1, y1, x2, y2]', required = True)
    parser.add_argument('--weight_1','-w_1', type=float, help='mass value for line 1', default = 0.5)
    parser.add_argument('--weight_2','-w_2', type=float, help='mass value for line 2', default = 0.5)
    parser.add_argument('--data_size','-d_s', type=int, help='data size', default = DATA_SIZE)
    parser.add_argument('--shift_rate','-dx', type=float, help='shift rate along x axis', default = 0.1)
    parser.add_argument('--threshold','-thresh', type=float, help='data size', default = 0.1)
    args = parser.parse_args()
    return args

def run():
    args = vars(argument())
    print(args)
    line1 = args['line_1']
    line2 = args['line_2']
    weight_1 = args['weight_1']
    weight_2 = args['weight_2']
    dx = args['shift_rate']
    threshold = args['threshold']

    y_upper,y_lower,x = [], [], []
    data_size = args['data_size']

    x_min, x_max= helper.min_max(line1, line2)
    x_range = np.linspace(x_min,x_max,data_size)
    xx = x_min
    while xx <= x_max :
        output = probability.plot_boundaries(args, xx, x_range)
        x.append(xx) # x values
        xx = xx + dx #  min to max with dx
        y_upper.append(output[0]) # y_up adds on
        y_lower.append(output[1]) # y_down adds on

    y1 = np.array(y_upper) #conver to array
    y2 = np.array(y_lower) #conver to array
    x = np.array(x) #conver to array

    top_bottom_points = [(top, botm) for top, botm in zip(y1,y2)]
    xx = x_min
    count = 0
    num = len(x.tolist())
    for ix in range(num):
        count = 0
        first  =  top_bottom_points[ix] # top, btm
        range_ = np.linspace(first[1], first[0], data_size).tolist() # create data point between top and btm (inclusive)
        df1, df2, error1, error2, dist= helper.create_data(args, xx)
        proba = probability.get_prob(args, df1, df2, range_, xx)

        sets = [(ix,x) for ix, x in enumerate(proba)] # tuple(index, probability)

        sets.sort(key = probability.takeSecond) # sort sets based on the size of probability (low to high) [(reordered index, low) to (_, high)]

        colors = helper.get_color_gradient(helper.COLOR1, helper.COLOR2, len(proba))
        prob_color = dict([(value[1], color) for value,color in zip(sets, colors)])

        index_color = dict([(value[0], color) for value,color in zip(sets, colors)])

        index_list = list(map(lambda x: x[0], index_color.items()))
        new_color = {}

        for keys, values in prob_color.items():
            if keys < threshold: #any less than or equal 10% probability
                value = 'white'
                new_color[keys] = value
            else:
                new_color[keys] = values
        new_index_color = dict([(list_, colors[1]) for list_, colors in zip(index_list, new_color.items())])


        limit = len(range_)// 5  # max number of iterations
        for ij in range(limit):
            color =   new_index_color[count] # finds the index in   new_index_color dict. not sequentially ordered
            try: # add vertical lines every 5 count on a single section point (xx)
                plt.vlines(xx, ymin = range_[count], ymax = range_[count + 5], color = color,\
                        label =  f'mass = {weight_1:.2f}, {weight_2:.2f}')

            except IndexError:
                pass

            count += 5

        xx += 0.1
        plt.show()



if __name__ == "__main__":
    run()