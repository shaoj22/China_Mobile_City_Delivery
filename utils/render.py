'''
File: render.py
Project: China_Mobile_City_Delivery
Description:
-----------
draw picture of the solution routes.
-----------
Author: 626
Created Date: 2023-1026
'''


import matplotlib.pyplot as plt
import seaborn as sns


def render_route(coordinates, paths):
    """
    render the routes of the solution.

    Args:
        coordinates (list[[]]): coords of the points.
        paths (list[[]]): solution of the routes.
    """
    sns.set(style="whitegrid")  # 设置Seaborn样式
    plt.figure(figsize=(12, 10))  # 设置图表大小
    # 不同路径使用不同颜色和线条样式
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    line_styles = ['-', '--', '-.', ':']
    for idx, path in enumerate(paths):
        path_coordinates = [coordinates[idx] for idx in path]
        path_x, path_y = zip(*path_coordinates)
        color = colors[idx % len(colors)]
        line_style = line_styles[idx % len(line_styles)]
        plt.plot(path_x, path_y, marker='o', linewidth=2, color=color, linestyle=line_style, label=f'Path {idx+1}')
    warehouse_x, warehouse_y = coordinates[0]
    plt.plot(warehouse_x, warehouse_y, marker='s', color='red', markersize=10, label='Warehouse')
    plt.title('Routes Visualization', fontsize=18)  # 增加标题字体大小
    plt.xlabel('Longitude', fontsize=16)  # 坐标轴标签字体大小
    plt.ylabel('Latitude', fontsize=16)  # 坐标轴标签字体大小
    plt.legend(fontsize=14)  # 图例字体大小
    plt.grid(True)
    plt.show()