# import dependencies
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import argparse
from typing import List, Any, Union
import logging
import os, sys
import time
import io
from io import BytesIO
import base64

from utils import *
def string_int(arg):
    return list(map(int, arg.split(",")))

DATA_SIZE = 100

def _helper(proba, color1, color2, threshold):
        sets = [(ix,x) for ix, x in enumerate(proba)] # tuple(index, probability)
        sets.sort(key = probability.takeSecond) # sort sets based on the size of probability (low to high) [(reordered index, low) to (_, high)]
        colors = helper.get_color_gradient(color1, color2, len(proba))
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
        return dict([(list_, colors[1]) for list_, colors in zip(index_list, new_color.items())])


def argument():
    parser = argparse.ArgumentParser(description='A sample argument parser')
    parser.add_argument('--line_1','-l_1', type=string_int, \
                         help='[x1, y1, x2, y2]', required = True)
    parser.add_argument('--line_2','-l_2', type=string_int, \
                         help='[x1, y1, x2, y2]', required = True)
    parser.add_argument('--weight_1','-w_1', type=float, help='mass value for line 1', default = 0.5)
    parser.add_argument('--weight_2','-w_2', type=float, help='mass value for line 2', default = 0.5)
    parser.add_argument('--data_size','-d_s', type=int, help='data size', default = DATA_SIZE)
    parser.add_argument('--shift_rate','-dx', type=float, help='shift rate along x axis', default = 0.1)
    parser.add_argument('--threshold','-thresh', type=float, help='data size', default = 0.01)
    parser.add_argument('--standard_dev','-std', type=int, help='numbr of std error from the mean', default = 2)
    parser.add_argument('--section','-sect', type=float, help='as a percentage between x_min and x_max', default=0.5)
    args = parser.parse_args()
    return args

def run():

    args = vars(argument())
    line1 = args['line_1']
    line2 = args['line_2']
    weight_1 = args['weight_1']
    weight_2 = args['weight_2']
    dx = args['shift_rate']
    threshold = args['threshold']
    data_size = args['data_size']
    std = args['standard_dev']
    target = args['section']
    y_upper,y_lower,x = [], [], []


    x_min, x_max= helper.x_min_max(line1, line2)
    y_min, y_max= helper.y_min_max(line1, line2)
    target = target * (x_max - x_min) + x_min
    x_range = np.linspace(x_min, x_max, data_size)
    xx = x_min

    y_curve1 = helper.ypoint(line1, x_range)
    y_curve2 = helper.ypoint(line2, x_range)
    plt.plot(x_range, y_curve1, color='blue', label='line 1',linewidth=2)
    plt.plot(x_range, y_curve2, color='red', label='line 2',linewidth=2)
    plt.legend(["line1", "line2"], loc ="lower right")

    img1 = io.BytesIO()
    plt.savefig(img1, format='png')
    plt.close()
    img1.seek(0)
    plot_url_1 = base64.b64encode(img1.getvalue()).decode('utf8')

    while xx <= x_max :
        output = probability.plot_boundaries(args, xx, x_range,std)
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

    start = time.time()
    for ix in range(num):
        count = 0
        first  =  top_bottom_points[ix] # top, btm
        range_ = np.linspace(first[1], first[0], data_size).tolist() # create data point between top and btm (inclusive)
        df1, df2, error1, error2, dist= helper.create_data(args, xx)
        proba = probability.get_prob(args, df1, df2, range_, xx)

        new_index_color = _helper(proba, helper.COLOR1, helper.COLOR2, threshold)
        limit = len(range_)// 5  # max number of iterations

        for ij in range(limit):
            color =   new_index_color[count] # finds the index in   new_index_color dict. not sequentially ordered
            try: # add vertical lines every 5 count on a single section point (xx)
                plt.vlines(xx, ymin = range_[count], ymax = range_[count + 5], color = color,\
                        label =  f'mass = {weight_1:.2f}, {weight_2:.2f}')
            except IndexError:
                pass

            count += 5

        xx += dx
    plt.title(f'weight_1: {weight_1} and weight_2: {weight_2} ', color = '#5e432e')
    img2 = io.BytesIO()
    plt.savefig(img2, format='png')
    plt.close()
    img2.seek(0)
    plot_url_2 = base64.b64encode(img2.getvalue()).decode('utf8')


    if target:
        count = 0
        df1_, df2_, error1, error2, dist= helper.create_data(args, xx)
        range_y = np.linspace(y_min, y_max, data_size).tolist()
        proba_ = probability.get_prob(args, df1_, df2_, range_y, target)
        new_index_color_ = _helper(proba_, helper.COLOR1, helper.COLOR2, threshold)
        limit = len(range_y)// 5

        for ij in range(limit):
            color = new_index_color_[count] #color index
            fir = range_y[count-5:count + 5] # section line
            las = proba_[count-5 :count + 5] # probabilities
            plt.plot(fir, las,  color = 'brown') # plot(x,prob)
            plt.fill_between(fir, las,color=color,alpha=.5)
            count += 5
        plt.title(f'section @ {target}', color = '#5e432e')

        img3 = io.BytesIO()
        plt.savefig(img3, format='png')
        plt.close()
        img3.seek(0)
        plot_url_3 = base64.b64encode(img3.getvalue()).decode('utf8')


        print(f'{plot_url_1}, {plot_url_2}, {plot_url_3}')

    else: print(f'{plot_url_1}, {plot_url_2}')


if __name__ == "__main__":
    run()

