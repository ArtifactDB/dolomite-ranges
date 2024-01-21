import os

import dolomite_base as dl
import h5py
from dolomite_base.read_object import registry
from genomicranges import SeqInfo

from ._utils_seqinfo import read_seqlengths_from_hdf5

registry["sequence_information"] = "dolomite_ranges.read_sequence_information"


def read_sequence_information(path: str, metadata: dict, **kwargs) -> SeqInfo:
    """Load sequence information into a
    :py:class:`~genomicranges.SeqInfo.SeqInfo` object.

    This method should generally not be called directly but instead be
    invoked by :py:meth:`~dolomite_base.read_object.read_object`.

    Args:
        path:
            Path to the directory containing the object.

        metadata:
            Metadata for the object.

        kwargs:
            Further arguments, ignored.

    Returns:
        A :py:class:`~genomicranges.SeqInfo.SeqInfo` object.
    """

    with h5py.File(os.path.join(path, "info.h5"), "r") as handle:
        ghandle = handle["sequence_information"]

        seqnames = dl._utils_vector.load_vector_from_hdf5(
            ghandle["name"], "string", True
        )

        seqlengths = read_seqlengths_from_hdf5(ghandle["length"])

        is_circular = dl._utils_vector.load_vector_from_hdf5(
            ghandle["circular"], "boolean", True
        )
        is_circular = is_circular.tolist()

        genome = dl._utils_vector.load_vector_from_hdf5(
            ghandle["genome"], "string", True
        )

    return SeqInfo(seqnames, seqlengths, is_circular, genome)
