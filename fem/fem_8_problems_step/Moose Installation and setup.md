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































