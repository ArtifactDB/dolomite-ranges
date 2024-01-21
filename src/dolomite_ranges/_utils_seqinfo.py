from typing import Sequence

import h5py
import numpy


def _list_to_numpy_uint_with_mask(x: Sequence) -> numpy.ndarray:
    mask = numpy.ndarray(len(x), dtype=numpy.uint8)
    arr = numpy.ndarray(len(x), dtype=numpy.uint64)
    for i, y in enumerate(x):
        if y is None:
            arr[i] = 0
            mask[i] = 1
        else:
            arr[i] = y
            mask[i] = 0
    return arr, mask


def write_seqlengths_to_hdf5(handle: h5py.Group, name: str, x: list) -> h5py.Dataset:
    has_none = any(y is None for y in x)
    placeholder = None
    if has_none:
        x, mask = _list_to_numpy_uint_with_mask(x)
        placeholder = 2**32 - 1
        for idx, v in enumerate(x):
            if mask[idx] == 1:
                x[idx] = placeholder

    dset = handle.create_dataset(
        name, data=x, dtype="u4", compression="gzip", chunks=True
    )
    if has_none:
        dset.attrs.create("missing-value-placeholder", placeholder, dtype="u4")
    return dset


def read_seqlengths_from_hdf5(handle) -> numpy.ndarray:
    values = handle[:]
    if "missing-value-placeholder" in handle.attrs:
        placeholder = handle.attrs["missing-value-placeholder"]

        if numpy.isnan(placeholder):
            mask = numpy.isnan(values)
        else:
            mask = values == placeholder

        return numpy.ma.MaskedArray(values, mask=mask).tolist()

    return values.astype(numpy.uint64).tolist()
