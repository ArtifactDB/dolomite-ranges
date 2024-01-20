import os

import dolomite_base as dl
import h5py
from dolomite_base import save_object, validate_saves
from genomicranges import SeqInfo


@save_object.register
@validate_saves
def save_sequence_information(x: SeqInfo, path: str, **kwargs):
    """Save Sequence information to disk.

    Args:
        x:
            Object to be saved.

        path:
            Path to a directory in which to save ``x``.

        kwargs:
            Further arguments to be passed to individual methods.

    Returns:
        `x` is saved to `path`.
    """
    os.mkdir(path)

    with open(os.path.join(path, "OBJECT"), "w", encoding="utf-8") as handle:
        handle.write(
            '{ "type": "sequence_information", "sequence_information": { "version": "1.0" } }'
        )

    with h5py.File(os.path.join(path, "info.h5"), "w") as handle:
        ghandle = handle.create_group("sequence_information")

        dl._utils_vector.write_string_list_to_hdf5(ghandle, "name", x.get_seqnames())

        dl._utils_vector.write_integer_list_to_hdf5(
            ghandle, "length", x.get_seqlengths()
        )
        dl._utils_vector.write_boolean_list_to_hdf5(
            ghandle, "circular", x.get_is_circular()
        )
        dl._utils_vector.write_string_list_to_hdf5(ghandle, "genome", x.get_genome())

    return
