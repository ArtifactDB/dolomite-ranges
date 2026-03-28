import os
from typing import Optional

import dolomite_base as dl
import h5py
from compressed_lists import Partitioning, splitAsCompressedList
from dolomite_base.read_object import read_object_registry

read_object_registry["atomic_vector_list"] = "dolomite_ranges.read_atomic_vector_list"


def read_atomic_vector_list(path: str, metadata: Optional[dict], **kwargs):
    """Load a list of atomic vectors from its on-disk representation.

    Args:
        path:
            Path to the directory containing the object.

        metadata:
            Metadata for the object.

        kwargs:
            Further arguments, ignored.


    """
    return _read_compressed_list(path, metadata, "atomic_vector_list", **kwargs)


def _read_compressed_list(path: str, metadata: Optional[dict], name: str, **kwargs):
    concat_path = os.path.join(path, "concatenated")
    concat = dl.alt_read_object(concat_path, **kwargs)

    fpath = os.path.join(path, "partitions.h5")
    with h5py.File(fpath, "r") as fhandle:
        ghandle = fhandle[name]
        lengths = dl.load_vector_from_hdf5(ghandle["lengths"], expected_type=int, report_1darray=True)

        names = None
        if "names" in ghandle:
            names = dl.load_vector_from_hdf5(ghandle["names"], expected_type=str, report_1darray=True)

        output = splitAsCompressedList(concat, Partitioning.from_lengths(lengths=lengths, names=names))

    _elem_annotation_path = os.path.join(path, "element_annotations")
    if os.path.exists(_elem_annotation_path):
        _mcols = dl.alt_read_object(_elem_annotation_path, **kwargs)
        output = output.set_element_metadata(_mcols)

    _meta_path = os.path.join(path, "other_annotations")
    if os.path.exists(_meta_path):
        _meta = dl.alt_read_object(_meta_path, **kwargs)
        output = output.set_metadata(_meta.as_dict())

    return output
