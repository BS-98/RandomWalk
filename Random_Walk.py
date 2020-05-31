# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 20:56:28 2020

@author: Bartek
"""
import csv
import random
import time
from multiprocessing import Process, Queue
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def plot(typ):
    steps = 12000
    #possible_shifts = [[1,0], [-1,0], [0,1], [0,-1]]
    shift = [-1, 0, 1]
    start_corr_2D = [0, 0]
    start_corr_3D = [0, 0, 0]
    
    path_2D = np.zeros(shape=(steps,2)) 
    path_3D = np.zeros(shape=(steps,3)) 
    
    path_2D[0] = start_corr_2D
    path_3D[0] = start_corr_3D
    
    for i in range(1, steps):
        
         shift_2D = [random.choice(shift), random.choice(shift)]
         shift_3D = [random.choice(shift), random.choice(shift), random.choice(shift)]
    #     next_corr = list(map(sum, zip(start_corr, random.choice(possible_shifts))))
         next_corr_2D = list(map(sum, zip(start_corr_2D, shift_2D)))
         next_corr_3D = list(map(sum, zip(start_corr_3D, shift_3D)))
    
         
         path_2D[i] = next_corr_2D
         path_3D[i] = next_corr_3D
         
         start_corr_2D = next_corr_2D
         start_corr_3D = next_corr_3D
    
          
    if typ == "2D":
        #2D
        fig = plt.figure(figsize=(8,8),dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter(path_2D[:,0], path_2D[:,1],c='blue',alpha=0.5,s=0.05)
        ax.plot(path_2D[:4000,0], path_2D[:4000,1],c='blue',alpha=0.8,lw=0.25)
        ax.plot(path_2D[4000:8000,0], path_2D[4000:8000,1],c='red',alpha=0.8,lw=0.25)
        ax.plot(path_2D[8000:,0], path_2D[8000:,1],c='green',alpha=0.8,lw=0.3)
        plt.title('2D Random Walk')
        plt.tight_layout(pad=0)
        plt.show()
    
    if typ == "3D":
        #3D
        fig = plt.figure(figsize=(8,8),dpi=280)
        ax = fig.add_subplot(111, projection='3d')
        ax.grid(False)
        ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False
        ax.scatter3D(path_3D[:,0], path_3D[:,1], path_3D[:,2], 
                      c='blue', alpha=0.25, s=0)
        ax.plot3D(path_3D[:4000,0], path_3D[:4000,1], path_3D[:4000,2], 
                   c='blue', alpha=0.5, lw=0.5)
        ax.plot3D(path_3D[4000:8000,0], path_3D[4000:8000,1], path_3D[4000:8000,2], 
                   c='red', alpha=0.5, lw=0.5)
        ax.plot3D(path_3D[8000:,0], path_3D[8000:,1], path_3D[8000:,2], 
                   c='green', alpha=0.8, lw=0.8)
        plt.title('3D Random Walk')
        plt.tight_layout(pad=0)
        plt.show()

def animate(q):
    xs = [0]
    ys = [1]

    
    def _animate(i):
        while not q.empty():
            x, y = q.get()
            xs.append(x)
            ys.append(y)
        plt.cla()
        #    plt.scatter(xs, ys, c='red', marker='*')

        if i < 10:
            plt.plot(xs, ys, c='blue', lw=0.6)
        elif 10 <= i < 50:
            plt.plot(xs, ys, c='red', lw=0.6)
        else:
            plt.plot(xs, ys, c='green', lw=0.6)

        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), _animate, interval=300)

    plt.tight_layout()
    plt.show()



def main():
    steps = 12000
    shift = [-1, 0, 1]
    start_corr_2D = [0, 0]
    start_corr_3D = [0, 0, 0]

    path_2D = np.zeros(shape=(steps,2))
    path_3D = np.zeros(shape=(steps,3))

    path_2D[0] = start_corr_2D
    path_3D[0] = start_corr_3D

    fieldnames = ["X", "Y"]
    data_queue = Queue()
    plot_process = Process(target=animate, args=(data_queue,))
    plot_process.start()


    with open('data.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        info = {
            "X": start_corr_2D[0],
            "Y": start_corr_2D[1],
            }

        csv_writer.writerow(info)


    for i in range(1, steps):

        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            shift_2D = [random.choice(shift), random.choice(shift)]
            shift_3D = [random.choice(shift), random.choice(shift), random.choice(shift)]

            next_corr_2D = list(map(sum, zip(start_corr_2D, shift_2D)))
            next_corr_3D = list(map(sum, zip(start_corr_3D, shift_3D)))

            path_2D[i] = next_corr_2D
            path_3D[i] = next_corr_3D

            start_corr_2D = next_corr_2D
            start_corr_3D = next_corr_3D

            info = {
            "X": next_corr_2D[0],
            "Y": next_corr_2D[1],
            }
            data_queue.put((next_corr_2D[0], next_corr_2D[1]))
            csv_writer.writerow(info)

        time.sleep(0.3)

    plot_process.join()



if __name__ == '__main__':
    mode = input("Real-time? (y/n):")

    if mode == "y":
        main()
        
    elif mode == "n":
        
        plot_type = input("Plot (2D/3D):")
        
        if plot_type == "2D":
            plot(typ="2D")
            
        elif plot_type == "3D":
            plot(typ="3D")