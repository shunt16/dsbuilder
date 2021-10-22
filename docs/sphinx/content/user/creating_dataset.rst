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


.. code-block:: python

        import numpy as np

        # define ds variables
        variables_dict = {
            "temperature": {
                "dtype": np.float32,
                "dim": ["x", "y", "time"],
                "attrs": {
                    "units": "K",
                    "u_components": ["u_temperature"]
                }
            },
            "u_temperature": {
                "dtype": np.int16,
                "dim": ["x", "y", "time"],
                "attrs": {"units": "%"},
                "err_corr": [
                    {
                        "dim": "x",
                        "form": "systematic",
                        "params": [],
                        "units": []
                    }
                ]
            },
            "quality_flag_time": {
                "dtype": "flag",
                "dim": ["time"],
                "flag_meanings": ["bad", "dubious"]
            },
        }

        # define dim_size_dict to specify size of arrays
        dim_sizes_dict = {
            "x": 500,
            "y": 600,
            "time": 6
        }

        # create dataset
        ds = create_template_dataset(variables_dict, dim_sizes_dict)