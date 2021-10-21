.. template_python_module documentation master file, created by sphinx-quickstart

dsbuilder: creating datasets, to specification
==============================================

**dsbuilder** is a python module to help you build and write data files (primarily `NetCDF <https://www.unidata.ucar.edu/software/netcdf/>`_) with a specified format of dimensions, variables and metadata etc. It is built on top of `xarray <http://xarray.pydata.org/en/stable/>`_.

Although xarray itself provides a `simple interface <http://xarray.pydata.org/en/stable/user-guide/data-structures.html#creating-a-dataset>`_ for creating `datasets <http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html>`_, building complex datasets to particular standards in a documented way can become a bit of a pain. Particularly when defining standard variable formats, e.g. flags or uncertainties. **dsbuilder** looks to solve this problem by building template datasets with easily defined dictionaries, that may be populated with data and written to file using xarray's built in functionality.

A simple dataset containing a radiance image may be built as follows:

.. code-block:: python

   from dsbuilder import create_template_dataset

   ds_variables = {
       "radiance": {
           "dim": ["lambda", "x", "y"],
           "dtype": np.float32,
           "attributes": {
               "standard_name": "toa_outgoing_radiance_per_unit_wavelength",
               "long_name": "'toa' means top of atmosphere. The TOA outgoing radiance"
                            " is the upwelling radiance, i.e., toward outer space. "
                            "Radiance is the radiative flux in a particular direction, "
                            "per unit of solid angle. In accordance with common usage "
                            "in geophysical disciplines, 'flux' implies per unit area, "
                            "called 'flux density' in physics",
               "units": "W m-2 sr-1 m-1",
               "preferred_symbol": "L"
           }
       }
   }

   ds = create_template_dataset(
       variables_dict = ds_variables,
       dim_sizes_dict = {"lambda": 10, "x": 1000, "y": 1000},
   )

   ds["radiance"] = ... # populate variable with radiance image array

   ds.to_netcdf("path/to/file.nc")

**dsbuilder** is developed within Earth observation community, so it is designed with adhering to the `cf conventions <https://cfconventions.org>`_ particularly in mind. Eventually, **dsbuilder** will do this more automatically.

For more information see the User Guide and API Reference documentation.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   content/quickstart

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   content/API/dsbuilder

Contributions
-------------

**dsbuilder** is written and maintained by `Sam Hunt <https://github.com/shunt16>`_.