# Problem statement

We want to implement a numerical method, a meshless method, within Cabana. Where the
particle interact when their distance between the centres is less both the particle's radius
combined.

$$
\begin{aligned}
m\frac{du}{dt} &= F_{c}\\
\frac{dx}{dt} &= u
\end{aligned}
$$

The force between two particles is computed by

$$
(F_c)^i = k^i \delta_{ij} \hat{n}_{ij}
$$


As part of the integration step, we evolve the properties of the particles by:
$$
\begin{aligned}
u_{t + 1} &= u_{t} + \frac{du}{dt} \Delta t \\
x_{t + 1} &= x_{t} + u_t \Delta t \\
\end{aligned}
$$

# Overview of the implementation


It has following steps:

1. [x] Setup the package
2. [x] Create your particle class, write a test
3. [x] How to write an output file
4. [ ] Write about neighbours depending on the different for loop we use
5. [ ] Write force interaction including the neighbour search functionality, write a test
6. [ ] Write an integrator, write a test
7. [ ] How to write a solver, write a test
8. [ ] How to take inputs from an input file, write a test
9. [ ] Write a final example showing the full implementation which solves the problem
10. [ ] Use automan to automate the results


# Step 1: Setup the package
#cabana/setup_new_package

Provided the problem statement above, we know what properties our particles need to have. They are as following

Todo: Draw figure with the governing equations, and the properties needed, like kind of an extraction. 

With that, we want to create a basic repo, which supports quick compilation without thinking about the hassle of setting up the repository, which has, tests, make file, examples. 

As a basic first point, we will see how we can have a particle class, an example supporting on how to use this particle class, a test suite ready for you to use. 

The repository with the following commit at https://github.com/dineshadepu/Cabana_package_template/tree/08e5625f3c6ecb4a54f597faeb3c3e7faef3ff76, we can see the starting point. 
The files at this point needed can be seen in a tree view:
```bash
 dineshadepu@MacOS
/Users/dineshadepu/life/softwares/Cabana_package_template $
|  Mac OS => tree -I build
.
├── CMakeLists.txt
├── README.md
├── cmake
│   └── FindCLANG_FORMAT.cmake
├── examples
│   ├── CMakeLists.txt
│   └── test_01_particles_creation.cpp
├── src
│   ├── CMakeLists.txt
│   ├── CabanaNewPkg.hpp
│   ├── CabanaNewPkg_Particles.cpp
│   └── CabanaNewPkg_Particles.hpp
└── unit_test
    ├── CMakeLists.txt
    ├── TestCUDA_Category.hpp
    ├── TestHIP_Category.hpp
    ├── TestOPENMP_Category.hpp
    ├── TestPTHREAD_Category.hpp
    ├── TestSERIAL_Category.hpp
    ├── mpi_unit_test_main.cpp
    └── tstParticlesCreation.hpp
```

One need not touch the following files, but need to add/edit files to their package as they 
develop:
```bash
├── CMakeLists.txt [NO]
├── README.md
├── cmake
│   └── FindCLANG_FORMAT.cmake [NO]
├── examples
│   ├── CMakeLists.txt
│   └── test_01_particles_creation.cpp
├── src
│   ├── CMakeLists.txt
│   ├── CabanaNewPkg.hpp
│   ├── CabanaNewPkg_Particles.cpp
│   └── CabanaNewPkg_Particles.hpp
└── unit_test
    ├── CMakeLists.txt
    ├── TestCUDA_Category.hpp [NO]
    ├── TestHIP_Category.hpp [NO]
    ├── TestOPENMP_Category.hpp [NO]
    ├── TestPTHREAD_Category.hpp [NO]
    ├── TestSERIAL_Category.hpp [NO]
    ├── mpi_unit_test_main.cpp [NO]
    └── tstParticlesCreation.hpp
```

We don't need to change the `CMake` files much either, if we add an example or a source file or a
test, we will just add a line to the corresponding `CMake` file in that folder.  This act will be 
demonstrated further as we go deep in the tutorial.


Specifically, the files to see are `CMakeLists.txt` on the root folder:

```bash
# project settings
cmake_minimum_required(VERSION 3.12)

# C only for Cabana HDF5 workaround.
project(CabanaNewPkg LANGUAGES CXX C VERSION 0.1.0)

include(GNUInstallDirs)

# find dependencies
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
# find_package(Cabana 0.6.1 REQUIRED COMPONENTS Cabana::Grid Cabana::Core)
find_package(Cabana REQUIRED)
if( NOT Cabana_ENABLE_MPI )
  message( FATAL_ERROR "Cabana must be compiled with MPI" )
endif()
find_package(nlohmann_json 3.10.0 QUIET)
if(NOT NLOHMANN_JSON_FOUND)
  include(FetchContent)
  # Using most recent release here
  FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz)
  FetchContent_MakeAvailable(json)
endif()

# find Clang Format
find_package( CLANG_FORMAT 14 )

# library
add_subdirectory(src)

# examples
add_subdirectory(examples)

##---------------------------------------------------------------------------##
## Clang Format
##---------------------------------------------------------------------------##
if(CLANG_FORMAT_FOUND)
  file(GLOB_RECURSE FORMAT_SOURCES src/*.cpp src/*.hpp examples/*.cpp examples/*.hpp)
  add_custom_target(format
    COMMAND ${CLANG_FORMAT_EXECUTABLE} -i -style=file ${FORMAT_SOURCES}
    DEPENDS ${FORMAT_SOURCES})
endif()

##---------------------------------------------------------------------------##
## Unit tests
##---------------------------------------------------------------------------##
option(CabanaNewPkg_ENABLE_TESTING "Build tests" OFF)
if(CabanaNewPkg_ENABLE_TESTING)
  find_package(GTest 1.10 REQUIRED)
  # Workaround for FindGTest module in CMake older than 3.20
  if(TARGET GTest::gtest)
    set(gtest_target GTest::gtest)
  elseif(TARGET GTest::GTest)
    set(gtest_target GTest::GTest)
  else()
    message(FATAL_ERROR "bug in GTest find module workaround")
  endif()
  enable_testing()
  add_subdirectory(unit_test)
endif()

```
A more detailed explanation of this cmakefile is given in Cabana basic notes. This file stays the same, and one needs to change "CabanaNewPkg" to their corresponding package name, such as, "CabanaDEM" or "CabanaPD". 

To compile this package, we need to follow these steps:

#cabana/compile
```bash
mkdir build
cd build
cmake \
    -D CMAKE_PREFIX_PATH="$CABANA_INSTALL_DIR" \
    -D CMAKE_INSTALL_PREFIX=install \
    -D CabanaNewPkg_ENABLE_TESTING=ON \
    .. ;
make -j 12
make install
```

You can run the examples with the above commit by executing
```bash
./examples/Tst01ParticlesCreation
```

Or tests by executing the following command inside the build folder:

```bash
ctest
```

however, sometimes this may not work, so we write a seperate makefile to run the tests, the makefile is given as:
```bash
# Define the build directory containing binaries
BUILD_DIR := /Users/dineshadepu/life/softwares/Cabana_package_template/build

# Find all binaries in BUILD_DIR with "test" in the name (macOS compatible)
TEST_BINARIES := $(shell find $(BUILD_DIR) -type f -perm +111 -name "*test*")

# Target to list all test binaries
.PHONY: list_tests
list_tests:
	@echo "Test binaries found:"
	@for test in $(TEST_BINARIES); do echo $$test; done

# Target to run all test binaries
.PHONY: run_tests
run_tests:
	@echo "Running all test binaries..."
	@for test in $(TEST_BINARIES); do \
	    echo "Running $$test"; \
	    $$test; \
	done
```

with this makefile, one can run the tests by executing 
```bash
make run_tests
```
command in the build directory. 

In the next section we will see how to add more properties to our particle class, and how to 
initialise the particles with different configurations. Write corresponding tests to make sure our particle array is working fine. 

# Step 2: Create your particle class
#cabana/setup_new_package

The updated code for this section can be browsed at the following commit:
https://github.com/dineshadepu/Cabana_package_template/tree/3e2f78278438ee5ce4aaf81a09133c5ac46d495f

As a first step create your own particle class, where it has properties what each particle should 
have. From the governing equations, we can see our particles need the following properties

Todo: Draw a figure

As listed in the figure, we need the following properties to be added to the particles to implement the governing equations:

| Property name | code notation | quantity |
| ------------- | ------------- | -------- |
| mass          | m             | scalar   |
| position      | x             | vector   |
| velocity      | u             | vector   |
| radius        | rad           | scalar   |
| stiffness     | k             | scalar   |
| force         | force         | vector   |
First we will add these properties to our particle class, this is done as following:
```cpp
  private:
    int _no_of_particles;
    aosoa_double_type _m;
    aosoa_vec_double_type _x;
    aosoa_vec_double_type _u;
    aosoa_double_type _rad;
    aosoa_double_type _k;
    aosoa_vec_double_type _force;
```
The types,  `aosoa_double_type, aosoa_vec_double_type` are defined as follows:

```cpp
  public:
    using memory_space = MemorySpace;
    using execution_space = typename memory_space::execution_space;
    static constexpr int dim = Dimension;

    using double_type = Cabana::MemberTypes<double>;
    using int_type = Cabana::MemberTypes<int>;
    using vec_double_type = Cabana::MemberTypes<double[dim]>;
    using vec_int_type = Cabana::MemberTypes<int[dim]>;
    using aosoa_double_type = Cabana::AoSoA<double_type, memory_space, 1>;
    using aosoa_int_type = Cabana::AoSoA<int_type, memory_space, 1>;
    using aosoa_vec_double_type = Cabana::AoSoA<vec_double_type, memory_space, 1>;
    using aosoa_vec_int_type = Cabana::AoSoA<vec_int_type, memory_space, 1>;
```

In order to access them and able to change, we need a public accessor, a sample public accessor looks like:
```cpp
  public:
	// returns access with constant access
    auto sliceMass() {
      return Cabana::slice<0>( _m, "mass" );
    }
	// returns access with constant access
    auto sliceMass() const
    {
      return Cabana::slice<0>( _m, "mass" );
    }
```

We want to add more particles to our existing particles, this is done by using the `resize` functionality, which is already provided as one of  the particle class methods:

```cpp
  public:
    void resize(const std::size_t n)
    {
      _no_of_particles = n;
      _m.resize( n );
      _x.resize( n );
      _u.resize( n );
      _rad.resize( n );
      _k.resize( n );
      _force.resize( n );
    }
```
It is essential one needs to add all the properties to the above method to in order to resize the 
array size.

With this `particle` class, lets see how to use it and create our particles in a siimulation.

## Step 2.1: Using the particle class
In the example, first select the execution and memory space. Then use the `Particles` class to 
create the particles, as follows:
```cpp
  using exec_space = Kokkos::OpenMP;
  using memory_space = typename exec_space::memory_space;

  auto particles = std::make_shared<
    CabanaNewPkg::Particles<memory_space, DIM>>(exec_space(), 1);
```
Here, we first set the number of particles as $1$. The above command will initialise the particles in
the particles class with dummy values, it is essential to initialise the particle, to do that we will use
the `updateParticles` method of the `Particles` class:

```cpp
  // ====================================================
  //            Custom particle initialization
  // ====================================================
  auto x_p = particles->slicePosition();
  auto u_p = particles->sliceVelocity();
  auto k_p = particles->sliceRadius();

  double radius_p_inp = 0.1;
  double k_p_inp = 1e5;

  auto particles_init_functor = KOKKOS_LAMBDA( const int pid )
    {
      // Initial conditions: displacements and velocities
      double m_p_i = 4. / 3. * M_PI * radius_p_inp * radius_p_inp * radius_p_inp * 1000.;
      double I_p_i = 2. / 5. * m_p_i * radius_p_inp * radius_p_inp;
      x_p( pid, 0 ) = radius_p_inp + radius_p_inp / 1000000.;
      u_p( pid, 0 ) = 0.;
      k_p( pid ) = k_p_inp;
    };
  particles->updateParticles( exec_space{}, particles_init_functor );
```

However it is essential, one needs to make sure this initializer works across the architechtures, 
and the initialiser is parallel.

Sometimes, we want to resize the number of particles, either reduce them or increase them:
This can be achieved by the `resize` method functionality as:
```cpp
  particles->resize(20);

  auto x_p_20 = particles->slicePosition();
  auto u_p_20 = particles->sliceVelocity();

  for (int i=0; i < u_p_20.size(); i++){
    x_p_20( i, 0 ) = 3 * i * radius_p_inp + radius_p_inp / 1000000.;

    u_p_20( i, 0 ) = 0.;
  }
```
It is essential, that we need to again get new pointers to the properties of the particles, since they get outdated once we resize.  




# Step 3: Output file
#cabana/write_output

The code files corresponding to this section development can be seen at https://github.com/dineshadepu/Cabana_package_template/tree/79c6f80e81ce0f5e0fe0150ee306ec499ed0c54f commit. 

In order to view the data of the particles we need to output the particles, this is done through hdf5 files. To the existing `Particles` class, we add the following method:

```cpp
    void output(  const int output_step,
                  const double output_time,
                  const bool use_reference = true )
    {
      // _output_timer.start();

#ifdef Cabana_ENABLE_HDF5
      Cabana::Experimental::HDF5ParticleOutput::writeTimeStep(
                                                h5_config,
	                                            _output_folder_name+"/particles",
												// "particles",
												MPI_COMM_WORLD,
												output_step,
                                                output_time,
                                                _no_of_particles,
                                                slicePosition(),
                                                sliceVelocity(),
                                                sliceForce(),
                                                sliceMass(),
                                                sliceRadius(),
                                                sliceStiffness());
#else
      std::cout << "No particle output enabled.";
#endif
    }

```
Further, we add variable to create a directory output where we want to save the output files by:
```cpp
    // Output folder name
    std::string _output_folder_name;
#ifdef Cabana_ENABLE_HDF5
    Cabana::Experimental::HDF5ParticleOutput::HDF5Config h5_config;
#endif
```

And a method to create a folder:
```cpp
    void set_output_folder(std::string output_folder_name)
    {
      _output_folder_name = output_folder_name;

      // Check if src folder exists
      if (!fs::is_directory(_output_folder_name) || !fs::exists(_output_folder_name)) {
        // create src folder
        fs::create_directory(_output_folder_name);
      }
    }
```

And a new constructor method which would create a output folder:
```cpp
    // Constructor which initializes particles on regular grid.
    template <class ExecSpace>
    Particles( const ExecSpace& exec_space, std::size_t no_of_particles,
               std::string output_folder_name): Particles(exec_space, no_of_particles)
    {
      set_output_folder(output_folder_name);
    }
```

## Step 3.1: Using output data functionality

We wrote three tests to test the output functionality code, which are:
```cpp
testParticlesOutputFolderCreationFromInitializer();
testParticlesOutputFolderCreationFromSetOutputFolder();
testParticlesHdfFile();
```
These test, if the folder and the hdf5 files created successfully.

From these tests, we can see, an output folder can be created either by a separate method assigned, or through while creating the Particles. That is:
```cpp
auto particles = std::make_shared<
	CabanaNewPkg::Particles<memory_space, DIM>>(exec_space(), 1);
particles->set_output_folder("test_particles_output_folder_creation_3_output");
```
or through the initializer:
```cpp
    auto particles = std::make_shared<
      CabanaNewPkg::Particles<memory_space, DIM>>(
      exec_space(), 1, "test_particles_output_folder_creation_output"
      );
```

While, at a given time, output can be written by:
```cpp
particles->output(total_steps/step, time);
```