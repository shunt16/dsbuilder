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
* ``err_corr`` - (optional) dictionary defining of uncertainty error-correlation structure, only include if variable is an uncertainty. See :ref:`uncertainty variables <uncertainty variables>` section for more.
* ``encoding`` - (optional) variable `encoding <http://xarray.pydata.org/en/stable/user-guide/io.html?highlight=encoding#writing-encoded-data>`_.

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


.. _uncertainty variables:

Defining uncertainty variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uncertainty variables are created when an uncertainty error-correlation structure definition is included in the variable definition dictionary, with the ``"err_corr"`` entry. This entry is dictionary where each key/value pair defines the error-correlation along a given dimension. The key is the name of the dimension (i.e. from ``dim_names``) and the value is a dictionary with the following entries:

* ``form`` - error-correlation form, defines functional form of error-correlation structure along
  dimension (recommended values from the `FIDUCEO project defintions list <https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e5c84c9e2c&appId=PPGMS>`_, names
  ``dsbuilder.dataset_util.ERR_CORR_DEFS.keys()``)
* ``params`` - parameters of the error-correlation structure defining function for dimension
  (number of parameters required depends on the particular form, if FIDUCEO forms used param numbers checked)
* ``units`` - units of the error-correlation function parameters for dimension (ordered as the parameters)

for example:

.. code-block:: python

    err_corr = {
        "x": {
            "form": "rectangular_absolute",
            "params": [val1, val2],
            "units": ["m", "m"]
        },
        "y": {
            "form": "random",
            "params": [],
            "units": []
        }
    }

.. note::
    If the error-correlation structure is not defined along a particular dimension (i.e. it is not
    included in ``err_corr``), the error-correlation is assumed random. Variable attributes are
    populated to the effect of this assumption.

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
