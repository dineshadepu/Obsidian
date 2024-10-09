
# Installation ({091024})
#pybamm-software-installation #python-installation #conda #software-installation-from-source 

Before installing `pybamm` software, first install `conda`package manager. Which can be done the following way

## Conda installation
#python-installation #python-installation-with-conda #bashrc 

1. Download the binary (sh) executable file from the website, which can be found at https://www.anaconda.com/download/success. 
2. Once downloaded, execute the following command from the terminal to install anaconda:
```bash
	bash <conda-installer-name>-latest-Linux-x86_64.sh
```

Then follow the instructions, which will paste the following code into `.bashrc` file finally:

```sh
export PATH=$HOME/anaconda3/bin:$PATH
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/dineshadepu/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/dineshadepu/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/dineshadepu/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/dineshadepu/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

3. Now create a virtual environment with `conda` to manage proper software management. 
```sh
conda create -n pybamm anaconda
conda activate pybamm
```

## `pybamm` installation
#pybamm-installation 

### Install `pybamm` from source. 

1. Clone the source
2. Change the directory
3. Install the package
```sh
git clone https://github.com/pybamm-team/PyBaMM
cd PyBaMM
pip install -e .[all,dev,docs]
```
We can add additional options, such as to use `jax`, which will essentially allow our simulations to run on GPU and other architectures faster.

### Install `pybamm` from pre-built packages

From `conda`
```sh
conda install -c conda-forge pybamm
```
From `pip`
```sh
pip install pybamm
```











