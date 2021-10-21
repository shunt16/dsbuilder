"""
Handling for multiple ds format specs
"""

from typing import Optional, Dict, List
import xarray
from dsbuilder import create_template_dataset


"""___Authorship___"""
__author__ = "Sam Hunt"
__created__ = "17/9/2020"


class DSBuilder:
    """
    Class to generate xarray Datasets following various file format specification.

    :param variables_defs: variables_dict for each product format
    :param metadata_defs: metadata for each product format

    Each dictionary has as keys ``"ds_format"`` strings that define the names of the different available dataset
    formats, e.g. "Level-0".

    For ``variables_defs`` the corresponding entries should be a `variable definition dictionary <https://dsbuilder.readthedocs.io/en/latest/content/quickstart.html#defining-a-template-dataset>`_.

    For ``metadata_defs`` the corresponding entries should be a dictionary of per product metadata.
    """

    def __init__(
        self,
        variables_defs: Optional[Dict] = None,
        metadata_defs: Optional[Dict] = None
    ):

        self.variables_defs = variables_defs if variables_defs is not None else {}
        self.metadata_defs = metadata_defs if metadata_defs is not None else {}

    def create_ds_template(
        self,
        dim_sizes_dict: Dict[str, int],
        ds_format: str
    ) -> xarray.Dataset:
        """
        Returns template dataset

        :param dim_sizes_dict: entry per dataset dimension with value of size
        :param ds_format: product format string (value returned by ``self.return_ds_formats()``)

        :returns: Empty dataset
        """

        # Find variables
        if ds_format in self.return_ds_formats():
            variables_dict = self.variables_defs[ds_format]
        else:
            raise NameError(
                "Invalid format name: "
                + ds_format
                + " - must be one of "
                + str(self.variables_defs.keys())
            )

        # Find metadata def
        metadata = {}
        if ds_format in self.metadata_defs.keys():
            metadata = self.metadata_defs[ds_format]

        else:
            raise RuntimeWarning("No metadata found for file type " + str(ds_format))

        return create_template_dataset(
            variables_dict, dim_sizes_dict, metadata=metadata
        )

    def return_ds_formats(self) -> list:
        """
        Returns available ds format names

        :returns: ds formats
        """

        return list(self.variables_defs.keys())

    def return_ds_format_variable_names(self, ds_format: str) -> List[str]:
        """
        Returns variables for specified ds format

        :param ds_format: product format string (value returned by ``self.return_ds_formats()``)

        :returns: ds format variables
        """

        return list(self.variables_defs[ds_format].keys())

    def return_ds_format_variable_dict(self, ds_format: str, variable_name: str) -> Dict:
        """
        Returns variable definition info for specified ds format

        :param ds_format: product format string (value returned by ``self.return_ds_formats()``)
        :param variable_name: variable name

        :returns: variable definition info
        """

        return self.variables_defs[ds_format][variable_name]

    def return_ds_format_dim_names(self, ds_format: str) -> List[str]:
        """
        Returns dims required for specified ds format

        :param ds_format: product format string (value returned by ``self.return_ds_formats()``)

        :returns: ds format dims
        """

        ds_format_def = self.variables_defs[ds_format]

        ds_format_dims = set()

        for var_name in ds_format_def.keys():
            ds_format_dims.update(ds_format_def[var_name]["dim"])

        return list(ds_format_dims)

    def create_empty_dim_sizes_dict(self, ds_format: str) -> Dict[str, None]:
        """
        Returns empty dim_size_dict for specified ds format

        :param ds_format: product format string (value returned by ``self.return_ds_formats()``)

        :return: empty dim_size_dict
        """

        dim_sizes_dict = dict()
        for dim in self.return_ds_format_dim_names(ds_format):
            dim_sizes_dict[dim] = None

        return dim_sizes_dict


if __name__ == "__main__":
    pass
