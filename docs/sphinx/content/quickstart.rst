Quickstart
==========

This section will get you up and running with **dsbuilder** in 10 minutes or so. For more information checkout the API Docs. Step 1 is importing the **dsbuilder** module.

.. code-block:: python

   import dsbuilder


Defining a template dataset
---------------------------

Dataset specifications are described in python dictionaries. Most importantly is the ``variables`` dictionary, which defines the dataset variable structure. Each entry in this dictionary is a new variable. The key of the dictionary entry is the name of the variable, the value is a further dictionary that defines the variable with the following entries:

* ``dim`` - list of variable dimension names
* ``dtype`` - variable data type, either a `numpy dtype <https://numpy.org/devdocs/user/basics.types.html>`_ or one of the **dsbuilder** :ref:`special dtypes <special dtypes>`.
* ``attributes`` - dictionary of variable metadata
* ``encoding`` - variable `encoding <http://xarray.pydata.org/en/stable/user-guide/io.html?highlight=encoding#writing-encoded-data>`_.

Therefore, a ``variables`` dictionary for a dataset containing red, green and blue radiance band variables may look as follows:

.. code-block:: python

   variable_dict = {
       "band_red": {
           "dim": ["x", "y"],
           "dtype": np.float32,
           "attributes": {"units": "W m-2 sr-1 m-1"},
        }
       "band_green": {
           "dim": ["x", "y"],
           "dtype": np.float32,
           "attributes": {"units": "W m-2 sr-1 m-1"},
        }
       "band_blue": {
           "dim": ["x", "y"],
           "dtype": np.float32,
           "attributes": {"units": "W m-2 sr-1 m-1"},
        }
    }


.. _special dtypes:

Special dtypes
~~~~~~~~~~~~~~

Variable special dtypes allow the quick definition of a set of standardised variable formats. The following special dtypes are available.

Flags
_____

The ``"flag"`` dtype builds a variable in the `cf conventions flag format <https://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#flags>`_. Each datum bit corresponds to boolean condition flag with a given meaning.

The variable must be defined with an attribute that lists the per bit flag meanings as follows:

.. code-block:: python

   variable_dict = {
       "quality_flag": {
           "dim": ["x", "y"],
           "dtype": "flag"
           "attributes": {
               "flag_meanings": ["good_data", "bad_data"]
           }
       }
   }

The smallest necessary integer is used as the flag variable dtype, given the number of flag meanings defined (i.e. 7 flag meanings results in an 8 bit integer variable).

Uncertainties
_____________

This is work in progress!

Creating a template dataset
---------------------------

With the ``variables`` dictionary prepared, only two more specifications are required to build a template dataset. First a dictionary that defines the sizes of all the dimensions used in the ``variables`` dictionary, e.g.:

.. code-block:: python

   dim_size_dict = {"x": 1000, "y": 2000}


Secondly, a dictionary of dataset global metadata, e.g.:

.. code-block:: python

   metadata = {"dataset_name": "my cool image"}


Combining the above together a template dataset can be created as follows:

.. code-block:: python

   ds = dsbuilder.create_template_dataset(
       variables_dict,
       dim_sizes_dict,
       metadata
   )

Where ``ds`` is an empty xarray dataset with variables defined by the template definition. Fill values for the empty arrays are chosen using the `cf convention values <http://cfconventions.org/cf-conventions/cf-conventions.html#missing-data>`_.

Populating and writing the dataset
----------------------------------

`Populating <http://xarray.pydata.org/en/stable/user-guide/data-structures.html#dictionary-like-methods>`_ and `writing <http://xarray.pydata.org/en/stable/user-guide/io.html#reading-and-writing-files>`_ the dataset can be achieved using xarray's builtin functionality. Here's a dummy example:

.. code-block:: python

   ds["band_red"] = ... # populate variable with red image array
   ds["band_green"] = ... # populate variable with green image array
   ds["band_blue"] = ... # populate variable with blue image array

   ds.to_netcdf("path/to/file.nc")
