# 3d_neighbor_removal

# Remove_extra_plants_from_pointcloud

Some pointclouds include parts of multiple plants in them. This code removes
parts of extra plants by performing a DBSCAN on the pointcloud and, if there
are 2 or more large pieces, converting these into polygons and calculating the
area of overlap. If this area is greater than 50%, the pointclouds are
combined. At the end, all clusters aside from the largest are dropped,
returning a cropped pointcloud.

# Examples

Remove_extra_plants_from_pointcloud.py looks for a file named `*combined_multiway_registered_plant.ply`

```
python Remove_extra_plants_from_pointcloud.py -i /media/equant/7fe7f0a0-e17f-46d2-82d3-e7a8c25200bb/work/sandbox/3D/2020-02-29/combined_pointclouds/Marianna_157 -o /media/equant/7fe7f0a0-e17f-46d2-82d3-e7a8c25200bb/work/sandbox/3D/2020-02-29/dbscan_results
```
