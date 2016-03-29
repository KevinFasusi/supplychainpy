Formulas and Equations
======================

The formal expression of the formulas and equations used in the library are detailed here.

Lead-time Demand
----------------

.. math::

	LD = LT \times D

where:
	LD = Lead-time Demand

	LT = Lead-time

	D = Demand

Standard Deviation of Lead-time demand
--------------------------------------

.. math::

	\sigma_{LTD} = \sqrt{LT \times \sigma_{D}^2 + D^2 \times \sigma_{LT}^2}

where:
	\sigma_{LTD} =  Standard deviation of lead-time demand

	LT = Lead-time

	D = Demand


Reorder Level
-------------
The formula used for calculating the reorder level is:

.. math::

	RL = LT \times D \times Z \times \sigma \times \sqrt{LT}

where:
	Z = service level

	LT = Lead-time

	D = Demand


Safety Stock
------------

The formula used for safety stock is:

.. math::

	SS = Z \times \sigma \times \sqrt{LT}

where:
	SS = Safety Stock

	Z = service level

	LT = Lead-time


Economic Order Quantity (eoq)
-----------------------------

The economic order quantity is calculated using:

.. math::

    eoq_{0} = \sqrt \frac{2 \times R \times D}{HC}

where:
    R = Reorder Cost

    D = Demand

    HC = Holding Cost


Purchase Order Quantity
-----------------------

For the monte carlo siimulation, the

In release 0.0.3 the purchase order quantity will be compared against a forecast to assess whether it requires adjustment.


Backlog and Shortage units
--------------------------

To aggregate the backlog and shortage units for the `summarise_frame`


Normal Sum Deviation
--------------------

The standard deviation is calculated by first summing the average variance for backlog and quantity sold.


.. math::

	\sigma_{xy}^2 = \sigma_{x}^2 + \sigma_{y}^2


