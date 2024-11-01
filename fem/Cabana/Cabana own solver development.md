# Problem statement

We want to implement a numerical method, a meshless method, within Cabana. Where the
particle interact when their distance between the centres is less both the particle's radius
combined.

$$
\text{Governing equation}
$$


$$
\text{integration stepper equations}
$$

# Overview of the implementation


It has following steps:

1. Setup the package
2. Create your particle class, write a test
3. Write an integrator, write a test
4. Write force interaction including the neighbour search functionality
5. How to write an output file
6. How to write a solver
7. How to take inputs from an input file
8. Write a final example showing the full implementation which solves the problem
9. Use automan to automate the results


# Step 1: Setup the package

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

```cmake
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
```
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
```
make run_tests
```
command in the build directory. 

In the next section we will see how to add more properties to our particle class, and how to 
initialise the particles with different configurations. Write corresponding tests to make sure our particle array is working fine. 

# Step 2: Create your particle class

As a first step create your own particle class, where it has properties what each particle should 
have. 