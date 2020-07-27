# Stereo Vision based on Event Camera

## Introduction
This project is used to reproduce the results published in <br/>
Kogler, J., Sulzbachner, C., Humenberger, M., Eibensteiner, F.,
Address-Event Based Stereo Vision with Bio-Inspired Silicon Retina Imagers,
Advances in Theory and Applications of Stereo Vision (2011), pp. 165-188. 
https://u.pcloud.link/publink/show?code=XZ0QktkZJeG08fzrsT0y587cBu2vpy3EEbk7

We omit the calibration process of the left and right cameras, because the images we use have already been calibrated.

The project implements the following functions: <br/>

- In the [CameraBuffer](src/CameraBuffer.py) class, the event procedures are being simulated. <br/>
This class includes two methods, one is to prepare data, it puts the collected data into memory.
The other is to find the corresponding event. Both of these two methods have implementations corresponding to two different data structures, 
one is ordinary Array, the other is a dictionary, also called the hashmap.

- In the [Util](src/Util.py) class, loading method and matching costs functions are been implemented. <br/>
The loading method is mainly used to adapt to different formats of data. 
Three common linear and nonlinear methods are provided in the cost calculation method.

- The [OutputController](src/OutputController.py) class is the most important class in the entire project, 
which implements the very important WMI data structure in the event data processing process. <br/>
In addition, some related methods such as refreshing WMI, applying filters, evaluating cost values, etc., are all implemented in this class.

- The data we used were provided by Professor Marianne Maertens and Professor Guillermo Gallego Bonet. http://www.psyco.tu-berlin.de/

## Usage
See template.py

## Result

## Reference
Kogler, J., Sulzbachner, C., Humenberger, M., Eibensteiner, F.,
Address-Event Based Stereo Vision with Bio-Inspired Silicon Retina Imagers,
Advances in Theory and Applications of Stereo Vision (2011), pp. 165-188. 
https://u.pcloud.link/publink/show?code=XZ0QktkZJeG08fzrsT0y587cBu2vpy3EEbk7