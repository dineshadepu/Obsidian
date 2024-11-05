
# Test the neighbours

Lets create particles on a grid with equi-distance among them:



![[neighbours_grid_figure.png]]


In `Cabana`, given a list of points with positions, using the functionality provided by `Cabana` we 
would like to find the points closer to a given point with in a given cutoff. As part of our problems,
we created points on a grid from $0$ to $1$ with $0.1$ spacing between them. We want to find all the 
points closer to a given point, within a distance of $0.11$. 

Here I chosen a top to bottom approach to explain the neighbours and the final command which
gives us the neighbours is:
```cpp
Cabana::NeighborList<ListType>::getNeighbor(verlet_list, i, j )
```
Where $i$ is the index of the point we are looking for, and $j$ is a id which runs from $0$ to total number 
of neighbours index $i$ would have. 

Let's break it down: 
1. What is `verlet_list`?

```cpp
  ListType verlet_list( positions, 0, positions.size(), neighborhood_radius,
						cell_ratio, grid_min, grid_max );
```
2. What is `ListType`? 
```cpp
  using ListAlgorithm = Cabana::FullNeighborTag;
  using ListType =
    Cabana::VerletList<memory_space, ListAlgorithm,
                       Cabana::VerletLayoutCSR,
                       Cabana::TeamOpTag>;
```

Here, `ListAlgorithm` can be `Cabana::HalfNeighborTag`or `Cabana::FullNeighborTag`, depending on what we choose, we will have full neighbour list or half neighbour list. Depending on 
this one needs to write their force interaction codes. It can be parallel and consider all the neighbours or just half of them and do pair wise interactions (more about this later).

More about layout and build tag can be found at
https://github.com/ECP-copa/Cabana/wiki/Core-Neighbor-Lists#verletlist. Few options are 
```cpp
                       Cabana::VerletLayout2D,
                       Cabana::TeamVectorOpTag>;
```

3. Further, in order to get the neighbours, we need positions of the particles, which can be got 
from the AoSoA, radius cutoff with which we are looking for neighbours, minimum grid point and 
maximum grid point, such that all the particles are covered. For our current example, the grid points are 
```cpp
  double grid_min[3] = { -0.3, -0.3, -0.3 };
  double grid_max[3] = { 1.3, 1.3, 0.3 };
  double neighborhood_radius = 0.1005;
  double cell_ratio = 1.0;
```

**Note** It is very important that the grid limits exhaust the particles position else, we will run into segfault.

Full code of neighbours of above explanation can be found at https://github.com/dineshadepu/Cabana_package_template/blob/54e2fdb9c49dd02e4ce6f8c4386ec81c44485594/examples/test_02_compute_neighbours.cpp.



