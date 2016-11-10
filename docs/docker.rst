Supplychainpy with Docker
=========================

The docker image for supplychainpy uses the continuumio/anaconda3 image, with a pre-installed version of supplychainpy and all the dependencies.


.. parsed-literal::

    docker run -ti -v directory/on/client:directory/in/container --name fruit-smoothie -p5000:5000 supplychainpy/suchpy bash


The port, container name and directories can be changed as needed. Use a shared volume (as shown above) to present a CSV to the container for generating the report.

Make sure you specify the host as "0.0.0.0" for the reporting instance running in the container.


.. parsed-literal::

    supplychainpy data.csv -a -loc / -lx --host 0.0.0.0

