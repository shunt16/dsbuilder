"""
DatasetUtil class
"""

from dsbuilder.version import __version__
import string
import xarray
from xarray import Variable, DataArray
import numpy as np
from typing import Union, Optional, List, Dict


"""___Authorship___"""
__author__ = "Sam Hunt"
__created__ = "18/5/2020"
__version__ = __version__
__maintainer__ = "Sam Hunt"
__email__ = "sam.hunt@npl.co.uk"
__status__ = "Development"

DEFAULT_DIM_NAMES = list(string.ascii_lowercase[-3:]) + list(
    string.ascii_lowercase[:-3]
)
DEFAULT_DIM_NAMES.reverse()


ERR_CORR_DEFS = {
    "random": {"n_params": 0},
    "rectangle_absolute": {"n_params": 2},
    "rectangular_relative": {"n_params": 2},
    "triangular_relative": {"n_params": 2},
}


class DatasetUtil:
    """
    Class to provide utilities for generating standard xarray DataArrays and Variables
    """

    @staticmethod
    def create_default_array(dim_sizes, dtype, dim_names=None, fill_value=None):
        """
        Return default empty xarray DataArray

        :type dim_sizes: list
        :param dim_sizes: dimension sizes as ints, i.e. [dim1_size, dim2_size, dim3_size] (e.g. [2,3,5])

        :type dtype: type
        :param dtype: numpy data type

        :type dim_names: list
        :param dim_names: (optional) dimension names as strings, i.e. ["dim1_name", "dim2_name", "dim3_size"]

        :type fill_value: int/float
        :param fill_value: (optional) fill value (if None CF compliant value used)

        :return: Default empty array
        :rtype: xarray.DataArray
        """

        if fill_value is None:
            fill_value = DatasetUtil.get_default_fill_value(dtype)

        empty_array = np.full(dim_sizes, fill_value, dtype)

        if dim_names is not None:
            default_array = DataArray(empty_array, dims=dim_names)
        else:
            default_array = DataArray(
                empty_array, dims=DEFAULT_DIM_NAMES[-len(dim_sizes) :]
            )

        return default_array

    @staticmethod
    def create_variable(
        dim_sizes, dtype, dim_names=None, attributes=None, fill_value=None
    ):
        """
        Return default empty xarray Variable

        :type dim_sizes: list
        :param dim_sizes: dimension sizes as ints, i.e. [dim1_size, dim2_size, dim3_size] (e.g. [2,3,5])

        :type dtype: type
        :param dtype: numpy data type

        :type dim_names: list
        :param dim_names: (optional) dimension names as strings, i.e. ["dim1_name", "dim2_name", "dim3_size"]

        :type attributes: dict
        :param attributes: (optional) dictionary of variable attributes, e.g. standard_name

        :type fill_value: int/float
        :param fill_value: (optional) fill value (if None CF compliant value used)

        :return: Default empty variable
        :rtype: xarray.Variable
        """

        if fill_value is None:
            fill_value = DatasetUtil.get_default_fill_value(dtype)

        default_array = DatasetUtil.create_default_array(
            dim_sizes, dtype, fill_value=fill_value
        )

        if dim_names is None:
            variable = Variable(DEFAULT_DIM_NAMES[-len(dim_sizes) :], default_array)
        else:
            variable = Variable(dim_names, default_array)

        variable.attrs["_FillValue"] = fill_value

        if attributes is not None:
            variable.attrs = {**variable.attrs, **attributes}

        return variable

    @staticmethod
    def create_unc_variable(
            dim_sizes: List[int],
            dtype: np.typecodes,
            dim_names: List[str],
            attributes: Optional[Dict] = None,
            pdf_shape: str = "gaussian",
            err_corr: Optional[Dict[str, Dict[str, Union[str, list]]]] = None,
    ) -> xarray.Variable:
        """
        Return default empty 1d xarray uncertainty Variable

        :param dim_sizes: dimension sizes as ints, i.e. `[dim1_size, dim2_size, dim3_size]` (e.g. `[2,3,5]`)
        :param dtype: data type
        :param dim_names: dimension names as strings, i.e. `["dim1_name", "dim2_name", "dim3_size"]`
        :param attributes: dictionary of variable attributes, e.g. standard_name
        :param pdf_shape: (default: `"gaussian"`) pdf shape of uncertainties
        :param err_corr: uncertainty error-correlation structure definition, with each key/value pair defining the
        error-correlation along a given dimension. Where the key is the name of the dimension (i.e. from `dim_names`)
         and the value is a dictionary with the following entries:

        * `form` (*str*) - error-correlation form, defines functional form of error-correlation structure along
          dimension (recommended values from the FIDUCEO project defintions list, names
          `dsbuilder.dataset_util.ERR_CORR_DEFS.keys()`)
        * `params` (*list*) - parameters of the error-correlation structure defining function for dimension
          (number of parameters required depends on the particular form, if FIDUCEO forms used param numbers checked)
        * `units` (*list*) - units of the error-correlation function parameters for dimension
          (ordered as the parameters)

        for example:

        .. code-block:: python

            err_corr_def = {
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
            included in `err_corr_def`), the error-correlation is assumed random. Variable attributes are
            populated to the effect of this assumption.

        :returns: Default empty flag vector variable
        """

        # define uncertainty variable attributes, based on FIDUCEO Full FCDR definition (if required)
        attributes = {} if attributes is None else attributes

        if err_corr is None:
            err_corr = {}

        missing_err_corr_dims = [dim for dim in dim_names if dim not in err_corr.keys()]
        for missing_err_corr_dim in missing_err_corr_dims:
            err_corr[missing_err_corr_dim] = {
                "form": "random",
                "params": [],
                "units": []
            }

        for i, corr_dim in enumerate(err_corr):
            dim_str = "dim" + str(i+1)

            name_str = "_".join(["err", "corr", dim_str, "name"])
            form_str = "_".join(["err", "corr", dim_str, "form"])
            params_str = "_".join(["err", "corr", dim_str, "params"])
            units_str = "_".join(["err", "corr", dim_str, "units"])

            form = err_corr[corr_dim]["form"]

            attributes[name_str] = corr_dim
            attributes[form_str] = form
            attributes[units_str] = err_corr[corr_dim]["units"]

            # if defined form, check number of params valid
            if form in ERR_CORR_DEFS.keys():
                n_params = len(err_corr[corr_dim]["params"])
                req_n_params = ERR_CORR_DEFS[form]["n_params"]
                if n_params != req_n_params:
                    raise ValueError(
                        "Must define " + str(req_n_params) + " for correlation form"
                        + form + "(not " + str(n_params) + ")"
                    )

            attributes[params_str] = err_corr[corr_dim]["params"]

        attributes["pdf_shape"] = pdf_shape

        # Create variable
        variable = DatasetUtil.create_variable(
            dim_sizes,
            dtype,
            dim_names=dim_names,
            attributes=attributes,
        )

        return variable

    @staticmethod
    def create_flags_variable(dim_sizes, meanings, dim_names=None, attributes=None):
        """
        Return default empty 1d xarray flag Variable

        :type dim_sizes: list
        :param dim_sizes: dimension sizes as ints, i.e. [dim1_size, dim2_size, dim3_size] (e.g. [2,3,5])

        :type attributes: dict
        :param attributes: (optional) dictionary of variable attributes, e.g. standard_name

        :type dim_names: list
        :param dim_names: (optional) dimension names as strings, i.e. ["dim1_name", "dim2_name", "dim3_size"]

        :return: Default empty flag vector variable
        :rtype: xarray.Variable
        """

        n_masks = len(meanings)

        data_type = DatasetUtil.return_flags_dtype(n_masks)

        variable = DatasetUtil.create_variable(
            dim_sizes,
            data_type,
            dim_names=dim_names,
            fill_value=0,
            attributes=attributes,
        )

        # add flag attributes
        variable.attrs["flag_meanings"] = (
            str(meanings)[1:-1].replace("'", "").replace(",", "")
        )
        variable.attrs["flag_masks"] = str([2 ** i for i in range(0, n_masks)])[1:-1]

        # todo - make sure flags can't have units

        return variable

    @staticmethod
    def return_flags_dtype(n_masks):
        """
        Return required flags array data type

        :type n_masks: int
        :param n_masks: number of masks required in flag array

        :return: data type
        :rtype: dtype
        """

        if n_masks <= 8:
            return np.uint8
        elif n_masks <= 16:
            return np.uint16
        elif n_masks <= 32:
            return np.uint32
        else:
            return np.uint64

    @staticmethod
    def add_encoding(
        variable, dtype, scale_factor=1.0, offset=0.0, fill_value=None, chunksizes=None
    ):
        """
        Add encoding to xarray Variable to apply when writing netCDF files

        :type variable: xarray.Variable
        :param variable: data variable

        :type dtype: type
        :param dtype: numpy data type

        :type scale_factor: float
        :param scale_factor: variable scale factor

        :type offset: float
        :param offset: variable offset value

        :type fill_value: int/float
        :param fill_value: (optional) fill value

        :type chunksizes: float
        :param chunksizes: (optional) chucksizes
        """

        # todo - make sure flags can't have encoding added

        encoding_dict = {
            "dtype": dtype,
            "scale_factor": scale_factor,
            "add_offset": offset,
        }

        if chunksizes is not None:
            encoding_dict.update({"chunksizes": chunksizes})

        if fill_value is not None:
            encoding_dict.update({"_FillValue": fill_value})

        variable.encoding = encoding_dict

    @staticmethod
    def get_default_fill_value(dtype):
        """
        Returns default fill_value for given data type

        :type dtype: type
        :param dtype: numpy dtype

        :return: CF-conforming fill value
        :rtype: fill_value
        """

        if dtype == np.int8:
            return np.int8(-127)
        if dtype == np.uint8:
            return np.uint8(-1)
        elif dtype == np.int16:
            return np.int16(-32767)
        elif dtype == np.uint16:
            return np.uint16(-1)
        elif dtype == np.int32:
            return np.int32(-2147483647)
        elif dtype == np.uint32:
            return np.uint32(-1)
        elif dtype == np.int64:
            return np.int64(-9223372036854775806)
        elif dtype == np.float32:
            return np.float32(9.96921e36)
        elif dtype == np.float64:
            return np.float64(9.969209968386869e36)


if __name__ == "__main__":
    pass
