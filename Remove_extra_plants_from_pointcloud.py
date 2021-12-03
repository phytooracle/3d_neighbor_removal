import os
import cProfile
from posixpath import basename 
import sys 
import alphashape
import argparse
import glob
import pandas as pd
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# parsers ----------------------------------------------------------------------------------------------------------

def get_args():

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i',
                        '--indir',
                        help='Input directory containing pointclouds',
                        metavar='str',
                        type=str,
                        #default=''
                        default='/media/equant/7fe7f0a0-e17f-46d2-82d3-e7a8c25200bb/work/sandbox/3D/2020-02-29/combined_pointclouds/Kigalie_63/'
    )
    
# This isn't used in the script, so I'm commenting it out [NPH]
#    parser.add_argument('-o',
#                        '--outdir',
#                        help='Output directory for .ply files',
#                        metavar='str',
#                        type=str,
#                        #default='',
#    )

    parser.add_argument('-e',
                        '--eps',
                        help='EPS value for DBSCAN clustering',
                        metavar='eps',
                        type=float,
                        #default=0.07,
                        default=0.03,
    )
    
    return parser.parse_args()

# functions ----------------------------------------------------------------------------------------------------------

def overlapped_shapes(shape_list):
    def iterable_overlap(list_):
        overlapping_list = []
        overlap_values = []
        for i in list_:
            for j in [x for x in list_ if x != i]:
                overlap = i[0].intersection(j[0]).area/min(i[0].area, j[0].area)
                overlap_values.append(overlap)
                if overlap < 0.5 or overlap in overlap_values: 
                    if i not in overlapping_list:
                        overlapping_list.append(i)
                    if j not in overlapping_list:
                        overlapping_list.append(j)
                else:
                    overlapping_list.append([i[0].union(j[0]),np.row_stack((i[1], j[1]))])
        return overlapping_list, len(overlapping_list)
    len_list = []
    while list(set(len_list)) == len_list:
        shape_list, new_len = iterable_overlap(shape_list)
        len_list.append(new_len)
    polygon_list = []
    array_list = []
    for i in shape_list:
        polygon_list.append(i[0])
        array_list.append(i[1])
    return array_list, polygon_list

def get_shapes(list_):
    shape_list = []
    for array in list_:
        xy_array = np.delete(array, [2,3], 1)
        alpha_shape = alphashape.alphashape(xy_array, alpha = 2)
        shape_list.append([alpha_shape, np.delete(array, 3, 1)]) 
    return shape_list

def get_largest_pointcloud(list_):
    len_list = []
    for i in range(0, len(list_)):
        len_list.append(len(list_[i]))
    for i in list_:
        if len(i) == max(len_list):
            largest_pointcloud = i
        else:
            pass
    return largest_pointcloud

def save_plant_array_to_ply(array, out_dir, out_file):
    args = get_args()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(array)

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    o3d.io.write_point_cloud(os.path.join(out_dir, out_file + '_clustered.ply'), pcd)
    
#def generate_rotating_gif(array, gif_save_path, n_points=None, force_overwrite=False, scan_number=None):
def generate_rotating_gif(array, gif_save_path, n_points=7000, force_overwrite=False, scan_number=None):

    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(111, projection='3d')
    x = array[:,0]
    y = array[:,1]
    z = array[:,2]
    # c = array[:,3]
    cmap = 'Greens'
    ax.scatter(x, y, z,
               zdir='z',
               c = 'green',
               cmap = 'Dark2_r',
               marker='.',
               s=1,
    )
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.grid(False)
    ax.xaxis.pane.fill = False # Left pane
    ax.yaxis.pane.fill = False # Right pane
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    # Transparent panes
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # No ticks
    ax.set_xticks([]) 
    ax.set_yticks([]) 
    ax.set_zticks([])
    ax.set_box_aspect([max(x)-min(x),max(y)-min(y),max(z)-min(z)])
    def rotate(angle):
        ax.view_init(azim=angle)
    #rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 361, 2), interval=30)
    rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 361, 15), interval=300)
    #rot_animation.save('rotation.gif', dpi=80, writer='imagemagick')
    rot_animation.save(gif_save_path, dpi=80)
# define main ----------------------------------------------------------------------------------------------------------

def main():
    """Make a jazz noise here"""

    #pr = cProfile.Profile()
    #pr.enable()

    args = get_args()
    plant_pcd_filepaths = glob.glob(os.path.join(args.indir, '*combined_multiway_registered_plant.ply'))

    if len(plant_pcd_filepaths) == 0:
        raise ValueError(f"There were no pointclouds found in the input path provided ({args.indir})")

    print(f"Found {len(plant_pcd_filepaths)} pointcloud/s to process...\n    {plant_pcd_filepaths}")

    for pcd in plant_pcd_filepaths:
        
        out_dir = os.path.dirname(pcd)
        out_file = os.path.splitext(os.path.basename(pcd))[0]
        gif_path = os.path.join(out_dir.replace('combined_pointclouds', 'plant_reports'), 'combined_multiway_registered_soil_segmentation_cluster.gif')
 
        plant_pcd = o3d.io.read_point_cloud(pcd)
        with o3d.utility.VerbosityContextManager(
                o3d.utility.VerbosityLevel.Debug) as cm:
            labels = np.array(
                plant_pcd.cluster_dbscan(eps=args.eps, min_points=10, print_progress=True))
        
        labeled_pcd_array = np.column_stack((np.asarray(plant_pcd.points), np.array(labels)))
        
        dbscan_list = []
        for x in set(labeled_pcd_array[:,3]):
            dbscan_list.append(labeled_pcd_array[labeled_pcd_array[:,3] == x]) 
        
        if len(dbscan_list) == 1:
            array = np.delete(labeled_pcd_array, 3, 1)
            save_plant_array_to_ply(array, out_dir, out_file)
            #generate_rotating_gif(array=array, gif_save_path=gif_path)
            continue
            
        max_test_list = []
        max_len = len(get_largest_pointcloud(dbscan_list))
        for x in dbscan_list:
            if len(x) >= 0.05 * max_len:
                max_test_list.append(x)

        if len(max_test_list) == 1:
            array = np.delete(np.asarray(max_test_list[0]), 3, 1)
            save_plant_array_to_ply(array, out_dir, out_file)
            #generate_rotating_gif(array=array, gif_save_path=gif_path)
            continue
            
        shape_list = get_shapes(max_test_list)
        overlapped_array_list, overlapped_polygon_list = overlapped_shapes(shape_list)
        largest_sub_pcd = get_largest_pointcloud(overlapped_array_list)
        save_plant_array_to_ply(largest_sub_pcd, out_dir, out_file)
        #print(f"Generating rotating gif of largest_sub_pcd ({len(largest_sub_pcd)} points)")
        #generate_rotating_gif(array=largest_sub_pcd, gif_save_path=gif_path)

if __name__ == '__main__':
    #main()
    args = get_args()
    #cProfile.run('main()', filename=f"eps{args.eps}.prof")
