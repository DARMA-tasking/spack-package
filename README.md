# spack-package

This repository is a spack repo for _DARMA/vt_ and its required dependencies.

## Installing

Make sure [spack](https://github.com/spack/spack) is installed.

```sh
spack repo add /path/to/spack-package/
```

### Note about spack on clusters

It's important that spack uses the right version of mpi or it may try to build mpi from source. Similarly, it may be useful for it to be configured to use the system's cmake.

Edit `~/.spack/packages.yaml`. For example:

```yaml
packages:
  openmpi:
    paths:
      openmpi@3.1.3%gcc@8.2.0: /path/to/system/openmpi
  cmake:
    paths:
    cmake@3.13.2: /path/to/system/cmake

```

This avoids spack trying to build openmpi and cmake from source. To check what a particular install command will install, use:

```sh
spack install --fake <package_name>
```

However, you will have to uninstall the packages afterwards.

## Usage

Now, darma-vt is accessible to your spack instance.

```sh
spack install darma-vt
```

By default it will install version 1.0. You can specify `darma-vt@develop` to install the latest development version.
