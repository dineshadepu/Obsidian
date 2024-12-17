
# Question: Create a mesh?

![[mesh_types.png]]

While creating a mesh, we have several different options:
1. Uniform
2. Non-uniform
3. Sparse

```cpp
    Cabana::Grid::UniformMesh<double> uniform;
    Cabana::Grid::NonUniformMesh<double> nonuniform_double;
    Cabana::Grid::SparseMesh<double, 3> sparse;
```

The dimension of the mesh can be found from the class variable `num_space_dim`

```cpp
    std::cout << "Uniform mesh with dimension " << uniform.num_space_dim
              << std::endl;
```

A given mesh have several cells, edges, nodes, faces. Depending on the dimension a mesh may not have edges, as in two-dimension. 

## Check if a given cell is cell, edge is edge etc

Given a type, we want to check if it is a certain type, such as if it is edge, face or cell. This is done by:
```cpp
    std::cout << "Is Cell a Cell? "
              << Cabana::Grid::isCell<Cabana::Grid::Cell>() << std::endl;
    std::cout << "Is Node a Node? "
              << Cabana::Grid::isNode<Cabana::Grid::Node>() << std::endl;
    std::cout << "Is Cell a Node? "
              << Cabana::Grid::isNode<Cabana::Grid::Cell>() << "\n"
              << std::endl;
```

## Check if a given cell belongs to a given MPI rank?

We have several cells, to check if a given cell belongs to the same MPI rank or the neighbouring rank, that is it is a ghost can be found from

```cpp
Cabana::Grid::Own
```

# Global mesh

## How a global mesh can be created?

Global mesh with a constant cell size in all the dimensions can be created by:

```cpp
    double cell_size = 0.23;
    std::array<int, 3> global_num_cell = { 22, 19, 21 };
    std::array<double, 3> global_low_corner = { 1.2, 3.3, -2.8 };
    std::array<double, 3> global_high_corner = {
        global_low_corner[0] + cell_size * global_num_cell[0],
        global_low_corner[1] + cell_size * global_num_cell[1],
        global_low_corner[2] + cell_size * global_num_cell[2] };
    auto global_mesh_num_cell = Cabana::Grid::createUniformGlobalMesh(
        global_low_corner, global_high_corner, global_num_cell );
```

Similarly with a variable cell size:
```cpp
    std::array<double, 3> cell_size_array = { 0.23, 0.19, 0.05 };
    std::array<double, 3> global_high_corner_2 = {
        global_low_corner[0] + cell_size_array[0] * global_num_cell[0],
        global_low_corner[1] + cell_size_array[1] * global_num_cell[1],
        global_low_corner[2] + cell_size_array[2] * global_num_cell[2] };
    auto global_mesh_cell_size_array = Cabana::Grid::createUniformGlobalMesh(
        global_low_corner, global_high_corner_2, cell_size_array );
```

## Get the mesh properties, such as, extent, lowest corner, size

```cpp
    double low_x =
        global_mesh_cell_size_array->lowCorner( Cabana::Grid::Dim::I );
    double high_z =
        global_mesh_cell_size_array->highCorner( Cabana::Grid::Dim::K );
    double extent_y =
        global_mesh_cell_size_array->extent( Cabana::Grid::Dim::J );
    double cells_y =
        global_mesh_cell_size_array->globalNumCell( Cabana::Grid::Dim::J );
```

# Partitioners

## How to partition a given mesh into several MPI ranks

### Automatic partition

There are two way to partition, one is `DimBlock` (automatic) and `ManualBlock` (manual) way. 

```cpp
  Cabana::Grid::DimBlockPartitioner<3> dim_block_partitioner;
```

Get the ranks per dimension 
```cpp
  std::array<int, 3> ranks_per_dim_block =
    dim_block_partitioner.ranksPerDimension( MPI_COMM_WORLD, { 0, 0, 0 } );
```

And print them
```cpp
  // Print the created decomposition.
  if ( comm_rank == 0 )
    {
      std::cout << "Ranks per dimension (automatic): ";
      for ( int d = 0; d < 3; ++d )
        std::cout << ranks_per_dim_block[d] << " ";
      std::cout << std::endl;
    }
  // ========================
```

### Manual partition
```cpp
  int comm_size;
  MPI_Comm_size( MPI_COMM_WORLD, &comm_size );
  std::array<int, 2> input_ranks_per_dim = { comm_size, 1 };

  Cabana::Grid::ManualBlockPartitioner<2> manual_partitioner(input_ranks_per_dim);

  std::array<int, 2> ranks_per_dim_manual =
    manual_partitioner.ranksPerDimension( MPI_COMM_WORLD, { 0, 0 } );

  // Print the created decomposition.
  if ( comm_rank == 0 )
    {
      std::cout << "Ranks per dimension (automatic): ";
      for ( int d = 0; d < 2; ++d )
        std::cout << ranks_per_dim_manual[d] << " ";
      std::cout << std::endl;
    }
```


# Global grid example

## How to create a global grid?

We need the following to create a global grid:
1. Partitioner
```cpp
    Cabana::Grid::DimBlockPartitioner<2> partitioner;
```
2. Global mesh
```cpp
    double cell_size = 0.23;
    std::array<int, 2> global_num_cell = { 27, 15 };
    std::array<double, 2> global_low_corner = { 1.2, 3.3 };
    std::array<double, 2> global_high_corner = {
        global_low_corner[0] + cell_size * global_num_cell[0],
        global_low_corner[1] + cell_size * global_num_cell[1] };
    auto global_mesh = Cabana::Grid::createUniformGlobalMesh(
        global_low_corner, global_high_corner, global_num_cell );
```
3. Is it periodic
```cpp
    std::array<bool, 2> is_dim_periodic = { true, true };
```

With these defined, create the global grid:
```cpp
    auto global_grid = Cabana::Grid::createGlobalGrid(
        MPI_COMM_WORLD, global_mesh, is_dim_periodic, partitioner );
```
## Get the global grid data

1. Check if the grid is periodic
```cpp
        std::cout << "Global global grid information:" << std::endl;
        bool periodic_x = global_grid->isPeriodic( Cabana::Grid::Dim::I );
        std::cout << "Periodicity in X: " << periodic_x << std::endl;
```
2. Number of blocks in y direction
```cpp
        int num_blocks_y = global_grid->dimNumBlock( Cabana::Grid::Dim::J );
        std::cout << "Number of blocks in Y: " << num_blocks_y << std::endl;
```
3. Total number of blocks
```cpp
        int num_blocks = global_grid->totalNumBlock();
        std::cout << "Number of blocks total: " << num_blocks << std::endl;
```
4. Number of cells in x direction
```cpp
        int num_cells_x = global_grid->globalNumEntity( Cabana::Grid::Cell(),
                                                        Cabana::Grid::Dim::I );
        std::cout << "Number of cells in X: " << num_cells_x << std::endl;
```
5. Number of faces in y direction
```cpp
        int num_faces_y = global_grid->globalNumEntity(
            Cabana::Grid::Face<Cabana::Grid::Dim::I>(), Cabana::Grid::Dim::J );
        std::cout << "Number of X Faces in Y: " << num_faces_y << std::endl;
```

## MPI rank management of the grid

Since the global grid is managed by several MPI ranks, each rank will own some cells and the grid will know what part of cells are managed by which rank, and what cells are on the boundary. Lets look at a few methods on the grid type on how to fetch this data. 

1. Get the rank of the low boundary
```cpp
    bool on_lo_x = global_grid->onLowBoundary( Cabana::Grid::Dim::I );
    std::cout << "Rank-" << comm_rank << " on low X boundary: " << on_lo_x
              << std::endl;
```

2. Get the rank of the high boundary
```cpp
    bool on_hi_y = global_grid->onHighBoundary( Cabana::Grid::Dim::J );
    std::cout << "Rank-" << comm_rank << " on high Y boundary: " << on_hi_y
              << std::endl;
```

3. Get the block id
```cpp
    bool block_id = global_grid->blockId();
    std::cout << "Rank-" << comm_rank << " block ID: " << block_id << std::endl;
```

4. Block id in x
```cpp
    bool block_id_x = global_grid->dimBlockId( Cabana::Grid::Dim::I );
    std::cout << "Rank-" << comm_rank << " block ID in X: " << block_id_x
              << std::endl;
```

5. The number of cells this rank owns
```cpp
    int num_cells_y = global_grid->ownedNumCell( Cabana::Grid::Dim::J );
    std::cout << "Rank-" << comm_rank
              << " owned mesh cells in Y: " << num_cells_y << std::endl;
```