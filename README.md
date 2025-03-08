# spack-package

This repository is a spack repo for _DARMA/vt_ and its required dependencies.

## Installing

Make sure [spack](https://github.com/spack/spack) is installed.

```sh
spack repo add /path/to/spack-package/
```

### Note about spack on clusters

It's important that spack uses the right version of mpi or it may try to build mpi from source. Similarly, it may be useful for it to be configured to use the system's cmake.

If the system uses modules, be sure the relevant modules are loaded. Then run the following commands (substituting openmpi for mpich, etc. as appropriate):

```sh
#Have spack locate the system's CMake and OpenMPI
spack external find --not-buildable cmake openmpi

#Configure spack to never try to build any type of MPI package for itself
spack config add packages:mpi:buildable:false
```

This avoids spack trying to build openmpi and cmake from source. To check what a particular install command will install, use:

```sh
spack spec <package_name>
```

## Usage

Now, darma-vt is accessible to your spack instance.

```sh
spack install darma-vt
```

By default it will install version 1.0. You can specify `darma-vt@develop` to install the latest development version.

To run the tests for darma-vt, run:

```sh
spack install --test=root darma-vt
```

If darma-vt is already installed, you will have to uninstall it prior to running the above command.
