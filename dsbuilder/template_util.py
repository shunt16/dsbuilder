"""
Utilities for creating template xarray datasets
"""

from typing import Optional, Dict, List
from dsbuilder.version import __version__
from dsbuilder.dataset_util import DatasetUtil
import xarray


"""___Authorship___"""
__author__ = "Sam Hunt"
__created__ = "18/5/2020"
__version__ = __version__
__maintainer__ = "Sam Hunt"
__email__ = "sam.hunt@npl.co.uk"
__status__ = "Development"


def create_template_dataset(
        variables_dict: Dict[str, Dict],
        dim_sizes_dict: Dict[str, int],
        metadata: Optional[Dict] = None
) -> xarray.Dataset:
    """
    Returns template dataset

    :param variables_dict: dictionary defining variables, as defined below.
    :param dim_sizes_dict: dataset dimension sizes
    :param metadata: dictionary of dataset metadata

    :returns: template dataset

    For the ``variables_dict`` each key/value pair defines one variable, where the key is the variable name and the
    value is a dictionary with the following entries:

    * ``"dtype"`` (*np.typecodes*/*str*) - variable data type, either a numpy data type or special value ``"flag"`` for
      flag variable
    * ``"dim"`` (*list*) - list of variable dimension names
    * ``"attributes"`` (*dict*) - (optional) variable attributes
    * ``"encoding"`` (*dict*) - (optional) variable encoding.

    For more information on the required form of these entries, see the :ref:`variables definition section <variables dict>`
    of the user guide.
    """

    # Create dataset
    ds = xarray.Dataset()

    # Add variables
    ds = TemplateUtil.add_variables(ds, variables_dict, dim_sizes_dict)

    # Add metadata
    if metadata is not None:
        ds = TemplateUtil.add_metadata(ds, metadata)

    return ds


class TemplateUtil:
    """
    Class to create template xarray datasets
    """

    @staticmethod
    def add_variables(
            ds: xarray.Dataset,
            variables_dict: Dict[str, Dict],
            dim_sizes_dict: Dict[str, int]
    ) -> xarray.Dataset:
        """
        Adds defined variables dataset

        :param ds: dataset
        :param variables_dict: dictionary defining variables, see the :ref:`variables definition section <variables dict>` of the user guide for more information.
        :param dim_sizes_dict: entry per dataset dimension with value of size as int

        :returns: dataset with defined variables
        """

        du = DatasetUtil()

        for variable_name in variables_dict.keys():

            variable_attrs = variables_dict[variable_name]

            # Check variable definition
            TemplateUtil._check_variable_definition(variable_name, variable_attrs)

            # Unpack variable attributes
            dtype = variable_attrs["dtype"]
            dim_names = variable_attrs["dim"]
            attributes = (
                variable_attrs["attributes"] if "attributes" in variable_attrs else None
            )

            err_corr = None
            if attributes is not None:
                if "err_corr" in attributes:
                    err_corr = attributes.pop("err_corr")

            # Determine variable shape from dims
            try:
                dim_sizes = TemplateUtil._return_variable_shape(
                    dim_names, dim_sizes_dict
                )
            except KeyError:
                raise KeyError(
                    "Dim Name Error - Variable "
                    + variable_name
                    + " defined with dim not in dim_sizes_dict"
                )

            # Create variable and add to dataset
            if dtype == "flag":
                flag_meanings = attributes.pop("flag_meanings")
                variable = du.create_flags_variable(
                    dim_sizes,
                    meanings=flag_meanings,
                    dim_names=dim_names,
                    attributes=attributes,
                )

            else:

                if err_corr is None:
                    variable = du.create_variable(
                        dim_sizes, dim_names=dim_names, dtype=dtype, attributes=attributes
                    )

                else:
                    variable = du.create_unc_variable(
                        dim_sizes, dim_names=dim_names, dtype=dtype, attributes=attributes, err_corr=err_corr
                    )

                if "encoding" in variable_attrs:
                    du.add_encoding(variable, **variable_attrs["encoding"])

            ds[variable_name] = variable

        return ds

    @staticmethod
    def _check_variable_definition(
            variable_name: str,
            variable_attrs: Dict
    ):
        """
        Checks validity of variable definition, raising errors as appropriate

        :param variable_name: variable name
        :param variable_attrs: variable defining dictionary
        """

        # Variable name must be type str
        if type(variable_name) != str:
            raise TypeError(
                "Invalid variable name: " + str(variable_name) + " (must be string)"
            )

        # todo - add more tests to check validity of variable definition

    @staticmethod
    def _return_variable_shape(
            dim_names: List[str],
            dim_sizes_dict: Dict[str, int]
    ) -> List[int]:
        """
        Returns dimension sizes of specified dimensions

        :param dim_names: dimension names
        :param dim_sizes_dict: dimension sizes, entry per dimension

        :returns: dimension sizes
        """

        return [dim_sizes_dict[dim_name] for dim_name in dim_names]

    @staticmethod
    def add_metadata(
            ds: xarray.Dataset,
            metadata: Dict
    ) -> xarray.Dataset:
        """
        Adds metadata to dataset

        :param ds: dataset
        :param metadata: dictionary of dataset metadata

        :returns: dataset with updated metadata
        """

        ds.attrs.update(metadata)

        return ds


if __name__ == "__main__":
    pass
