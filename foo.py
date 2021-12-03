import timeit

for eps in [0.01, 0.02]:
    print(f"EPS: {eps}")
    timeit.timeit(foo = plant_pcd.cluster_dbscan(eps=eps, min_points=10, print_progress=True))
