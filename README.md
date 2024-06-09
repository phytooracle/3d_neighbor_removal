# 3D Neighbor Removal
This script removes neighboring plants from an individual plant point clouds. 

Some pointclouds include parts of multiple plants in them. This code removes parts of extra plants by performing a DBSCAN on the pointcloud and, if there are 2 or more large pieces, converting these into polygons and calculating the area of overlap. If this area is greater than 50%, the pointclouds are combined. At the end, all clusters aside from the largest are dropped, returning a cropped pointcloud.

## Inputs
Individual plant point clouds that have udnergone pre- and post-processing, as well as individual plant clipping and plant registration.

## Outputs
Subdirectories containing segmented point clouds, with neighboring plants removed.

## Arguments and Flags
* **Required Arguments:**
  * **Name of individual plant:** '-plant', '--plant_name'
  * **Directory where outputs will be saved:** '-pod', '--data_output_dir', default="segmentation_pointclouds"
  * **Directory where the dashboard figures and data will be saved.:** '-fod', '--figure_output_dir', default="plant_reports"
  * **Epsilon (EPS) value:** '-e', '--eps', default=0.05
  * **Name of the output filenam:** '-of', '--output_filename', default="final.ply"
