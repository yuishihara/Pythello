# To build
Download pybind11

```sh
$ git clone https://github.com/pybind/pybind11
```

Create new build directory to avoid messing up and build

```sh
$ ./build2.sh // For python2 build
$ ./build3.sh // For python3 build (Switch python interpreter to use before building)
```

# In case CXXABI_1.3.9 not found error occurs when importing
Try updating libgcc of conda with below command

```sh
$ conda install libgcc
```
