#moose/installation #software_installation/direct #software_installation/direct/conda 

First add the channel from which we can install `moose`
```bash
conda config --add channels https://conda.software.inl.gov/public
```

Now create an environment named `moose` in `conda` to install our `moose`

```bash
conda create -n moose moose-dev=2024.10.01=mpich
```
Activate the environment by
```bash
conda activate moose
```

Now install `moose` from the source by cloning it as follows
```bash
git clone https://github.com/idaholab/moose.git
cd moose
git checkout master
```

Running the following will install moose
```bash
cd ~/projects/moose/test
make -j 12
```
And one can test the installation by running tests as
```bash
cd ~/projects/moose/test
./run_tests -j 12
```

This way one needs update both `conda` and local git folder, in order to have `moose` installed.

# How to write a kernel

## The header file

1. Import the requisite already existing kernel header file
2. declare the constructor (Public method)
3. declare a function to validate the parameters (Public method)
4. declare a method to compute the residual at one quadrature point. This will further be defined in the .C file. (Protected method)
5. declare a method to compute the Jacobian at one quadrature point. This will further be defined in the .C file. (Protected method)
6. Define the class variables, which are used in the computation of the kernel values (private)

## The source file

We need to ensure the following functions are implemented, while implementing our own code in `MOOSE`.

1. Register the class in the app
2. Define the valid parameters for the kernel and assign default values if possible
3. Initialise the Class (this is similar to $__init__$  in python)
4. computeQpResidual, i.e., compute the quadrature point residual
4. computeQpJacobian, i.e., compute the quadrature point jacobian

