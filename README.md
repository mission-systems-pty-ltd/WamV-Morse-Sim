# WamV-Morse-Sim

The files in this package constitute a real-time Morse model of the WAM-V autonomous marine vehicle developed by the Mission Systems team. The model uses Python scripts to compute the thrust and drag for each hull separately and relies on the Bullet physics engine in Blender to generate the resulting accelerations and velocities in different parts of the model. This simulator uses MOOS-IvP as its middleware and helm, however Morse is compatible with several other middlewares including ROS.

[![wamv_video](https://i.imgur.com/Y5pn1OT.png)](https://www.youtube.com/watch?v=2SkJ2wC5OeA&t=11s)

---

## Table of Contents

- [Features](#features)
- [Description](#description)
- [Installation](#installation)
  * [Install MOOS-IvP](#install-moos-ivp)
  * [Install Pymoos](#install-pymoos)
  * [Install Morse](#install-morse)
  * [Install Other Dependencies](#install-other-Dependencies)
  * [Install WamV Simulation](#install-wamv-simulation)
- [Usage](#faq)
- [Additional Information](#additional-information)
  * [No MOOS?](#no-moos)
  * [Parameters](#parameters)
  * [Environments](#environements)
- [Team](#team)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## Features
The model has the following features:
- A graphically configurable distributed buoyancy system to approximate the forces experienced by floating objects on both irregular and dynamic water surfaces
- A simple fixed thruster model using differential thrust for directional control
- A hydrodynamic force model incorporating both linear and non-linear drag terms
- A MOOS interface responding to DESIRED_THRUST and DESIRED RUDDER messages
- Simulated instrument messages including IMU, GPS and DVL output
- Other features native to Morse, such as configurable cameras etc.
- A simple pygame script allowing joystick control of the model via its MOOS interface  

## Description
Unlike simpler models which treat maritime vehicles as single rigid bodies, this model treats the WAM-V as a compound assembly of rigid bodies held together by flexible joints. The hope is that the compound model responds more realistically to commands generated during actual RobotX tasks, allowing more thorough testing of autonomy algorithms.

While the manoeuvring model used here follows the usual Fossen matrix form and notation, I have discarded the rigid-body and Coriolis-centripetal matrices, as mass-related forces are already handled approximately by the Bullet physics engine and configured through Blender. There are some defects with this approach, including the loss of added mass effects, however, the literature I found indicated that added mass has little influence over WAM-V manoeuvring.

This model of the WAM-V is really the first to work as a compound simulation; that is, as an assembly of separate rigid bodies held together by physics constraints. Previously, Morse used a different paradigm in which sensors and actuators were attached to a common parent object, with the side effect that physics calculations for child objects were deactivated. Only the parent robot would respond to physics effects such as collisions etc. The desire to have multiple constituent parts of a compound robot respond to physics meant abandoning the parent hierarchy for a flat object structure – i.e. all robot components now occupy the same level in the Blender outliner.

One problem when dealing with compound robots is that setting their initial pose via the usual Morse translate and rotate methods without their children attached breaks the rigid body constraints and the model simply falls apart. For this reason, there are special translate and rotate functions for compound robots in wamv/src/helpers/compound.py to permit initialisation. These functions work by scanning all objects in the Blender scene to find those either directly or indirectly constrained by the nominated “root” object, which is also the object to which Morse attaches sensors and actuators.

## Installation
### Install MOOS-IvP
Check if MOOS-IvP is installed (e.g. `which pAntler` should return output similar to `/usr/local/bin/pAntler`). If MOOS-IvP is already installed, skip this step.

The following instruction set should be adequate to install MOOS-IvP on most Linux distributions:
```shell
$ svn co https://oceanai.mit.edu/svn/moos-ivp-aro/releases/moos-ivp-17.7.2 moos-ivp
```
(Note: at time of writing, moos-ivp 17.7.2 was the most recent stable release, check http://oceanai.mit.edu/moos-ivp/pmwiki/pmwiki.php?n=Site.Download for the most stable release, and see other information about the MOOS-IvP software)

Now build MOOS-IvP using the following commands (you may need to add `sudo` if installed into /usr/local or similar):
```shell
$ cd moos-ivp
$ sudo ./build-moos.sh
$ sudo ./build-ivp.sh
```
(Check successful installation using `which pAntler`, which should return output similar to `/usr/local/bin/pAntler`)

### Install Pymoos
There are several versions of pymoos however we found that the following installation instructions for Mohamed Saad Ibn Seddik's pymoos fork was best:
```shell
$ if [ "`uname`" != "Darwin" ] ; then export MOOS_CXX_FLAGS="-fPIC -Wno-long-long"; fi
$ if [ "`uname`" != "Darwin" ] ; then export CXX="g++-4.8"; fi
$ cd ~
$ git clone -b wOnlineCI --depth=1 https://github.com/msis/core-moos
$ cd core-moos
$ mkdir build
$ cd build
$ cmake -DENABLE_EXPORT=ON -DUSE_ASYNC_COMMS=ON -DTIME_WARP_AGGLOMERATION=0.4 -DCMAKE_BUILD_TYPE=$BUILD_TYPE -DCMAKE_CXX_FLAGS=$MOOS_CXX_FLAGS ..
$ cmake --build . --config Release --config -j4
$ sudo cmake --build . --config Release --target install
$ cd ~
$ git clone https://github.com/msis/python-moos.git
$ cd python-moos
$ mkdir build
$ cd build
$ cmake .. -DPYBIND11_PYTHON_VERSION=$PYTHON_VERSION
$ cmake --build .
```

You must then add pymoos to PYTHONPATH environment variable. First find the directory your linux distro has installed pymoos using:
```shell
$ find /usr -type d -name "pymoos"
```
(assuming it has been placed in the /usr directory).

You can then add it to your path by adding the following line to your `~/.bashrc` file:
```shell
$ export PYTHONPATH=${PYTHONPATH}:<parent_directory>
```
replacing `<parent_directory>` with the parent of the pymoos directory (e.g.: `export PYTHONPATH=${PYTHONPATH}:/usr/local/lib/python3/dist-packages`). Do not add the package name directly to the path, as this is the "double import trap" (see http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html). If this line is run only in the shell, then the pymoos library will only be included for that shell.


### Install Morse
Currently this simulation works using a modified version of morse, which is available in the repository. Clone this repository using:
```shell
$ git clone https://github.com/mission-systems-pty-ltd/WamV-Morse-Sim.git
```

Check if Morse is already installed using `morse check`. If morse is installed, you may wish to uninstall morse from your system or install this version separately.

To install the modified morse build, unzip the morse.tar.gz file. Then run the following commands:
```shell
$ cd morse
$ mkdir build && cd build
$ cmake ..
$ sudo make install
```
Add the following line to your `~/.bashrc` file:
```shell
$ export MORSE_ROOT=/usr/local
```

Check successful installation using `morse check`, and check that `MORSE_ROOT` is set by opening a new shell and running `printenv | grep MORSE_ROOT`.

### Install Other Dependencies
This software assumes python 3.6 is installed. You can check your python installation with `python3 -V` which should return output similar to `Python 3.6.7`. More recent python versions may also work.

This software also assumes blender 2.79b is installed. This should be automatically installed when morse is installed. You can check this installation with `blender -v` which should return output similar to `Blender 2.79 (sub 0)`. More recent blender versions may also work.

Some scripts require `matplotlib` to be installed. This can be done by running:
```shell
$ sudo apt-get install python3-matplotlib
```

### Install WamV Simulation
The repository should already have been cloned in the Morse installation step since this simulation uses a **modified morse** build. See the Install Morse section for more information.

If you have successfully installed the modified morse build (`morse check`) then proceed to Usage section.

## Usage
For ease of use, it is easiest to add the following line to your `.morse/config` file, which should be automatically generated after Morse installation, by setting the path to wherever you have cloned the repository. For example a typical path may be `/home/username/src/WamV-Morse-Sim/wamv_morse`:
```shell
$ wamv = /path/to/repository/.../WamV-Morse-Sim/wamv_morse
```

Then to run this code, you must run the moos database in one shell:
```shell
$ MOOSDB
```
You must then run the morse simulation in another shell:
```shell
$ morse run wamv
```
Alternatively, you can use the full path to WamV-Morse-Sim and after running `MOOSDB` in another shell, run:
```shell
$ morse run /path/to/repository/.../WamV-Morse-Sim/wamv_morse
```

## Additional Information

### No MOOS?
If you want to get the model running, but don’t have MOOS, just go to the robot definition in morse/wamv_sim/src/wamv_sim/builder/robots/wamv.py and comment out the add_stream calls for all sensors and actuators. Morse supports a variety of alternative middlewares.

### Parameters Used
The parameters we have chosen for the model are mostly guesses and some experimentation will be needed to match the manoeuvring of an actual WAM-V, which will vary depending on its configuration, thrusters and weight distribution. The thruster models we have used appear to possess a small fin or skeg under the motor body which probably contributes some directional stability. We have noted that most WAM-V models in the literature do not include any lift terms and hence could not be expected to track in a straight line for any length of time without a controller.

If you find serious errors in this code or departures from WAM-V behaviour which cannot be corrected through parameter adjustments, please let us know and we’ll see what we can do to fix the problem. We’ll endeavour to add to this document based on user feedback.

### Environments
Regrettably, we have only had time to supply an empty sea-surface environment with this model. Somebody who knows Blender will be able to easily create a proper RobotX environment with appropriate assets and hazards. There may be even be pre-existing environments hosted by the organisation that could be imported with minimal difficulty.

## Team
This software was written by Mission Systems, a research and development house founded by Sydney University Alumni, David Battle and David Johnson, and which focuses on the fields of robotics, sensing and perception in the air, sea and land domains. More information about what we do can be found at: http://www.missionsystems.com.au/

## Acknowledgements
I want to acknowledge the Morse team, who have been responsible for producing such a useful tool. I would also like to acknowledge Martins Upitis, who is responsible for the superb GLSL water shader shipped with this code, which certainly makes simulations more pleasant to look at.

## License
Information about the licensing of this software is found in the 'LICENSE' file of this repository.
