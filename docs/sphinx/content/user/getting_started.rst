Getting Started
===============

This section will get you up and running with **dsbuilder** in 10 minutes or so. For more information checkout the :ref:`User Guide <user guide>`.

Setting up
----------

**dsbuilder** can be installed using ``pip``::

    pip install dsbuilder

And then imported into your work:

.. code-block:: python

   import dsbuilder


Defining a template dataset
---------------------------

Dataset specifications are described in python dictionaries. Most importantly is the **variables** dictionary, which defines the dataset variable structure. Each entry in this dictionary is a new variable. The key of the dictionary entry is the name of the variable, the value is a further dictionary that defines the variable with the following entries:

* ``dim`` - list of variable dimension names.
* ``dtype`` - variable data type, generally a :py:class:`numpy.dtype`, though for some :ref:`special variables <special variables>` particular values may be required.
* ``attributes`` - dictionary of variable metadata, for some :ref:`special variables <special variables>` particular entries may be required.
* ``encoding`` - (optional) variable `encoding <http://xarray.pydata.org/en/stable/user-guide/io.html?highlight=encoding#writing-encoded-data>`_.

Therefore, a **variables** dictionary for a dataset containing red, green and blue radiance band variables may look as follows:

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

Creating a template dataset
---------------------------

With the **variables** dictionary prepared, only two more specifications are required to build a template dataset. First a dictionary that defines the sizes of all the dimensions used in the **variables** dictionary, e.g.:

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

Where ``ds`` is an empty :py:class:`xarray.Dataset` with variables defined by the template definition. Fill values for the empty arrays are chosen using the `cf convention values <http://cfconventions.org/cf-conventions/cf-conventions.html#missing-data>`_.

Populating and writing the dataset
----------------------------------

`Populating <http://xarray.pydata.org/en/stable/user-guide/data-structures.html#dictionary-like-methods>`_ and `writing <http://xarray.pydata.org/en/stable/user-guide/io.html#reading-and-writing-files>`_ the dataset can be achieved using xarray's builtin functionality. Here's a dummy example:

.. code-block:: python

   ds["band_red"] = ... # populate variable with red image array
   ds["band_green"] = ... # populate variable with green image array
   ds["band_blue"] = ... # populate variable with blue image array

   ds.to_netcdf("path/to/file.nc")
