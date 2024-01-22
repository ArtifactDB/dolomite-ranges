import os

import dolomite_base as dl
import h5py
from dolomite_base import save_object, validate_saves
from genomicranges import GenomicRanges


@save_object.register
@validate_saves
def save_genomic_ranges(x: GenomicRanges, path: str, **kwargs):
    """Method for saving :py:class:`~genomicranges.GenomicRanges.GenomicRanges`
    objects to their corresponding file representations, see
    :py:meth:`~dolomite_base.save_object.save_object` for details.

    Args:
        x:
            Object to be staged.

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
            '{ "type": "genomic_ranges", "genomic_ranges": { "version": "1.0" } }'
        )

    # sequence information
    spath = os.path.join(path, "sequence_information")
    dl.save_object(x.get_seqinfo(), spath)

    with h5py.File(os.path.join(path, "ranges.h5"), "w") as handle:
        ghandle = handle.create_group("genomic_ranges")

        _seqnames, _ = x.get_seqnames(as_type="factor")
        ghandle.create_dataset(
            "sequence",
            data=_seqnames,
            dtype="u4",
            compression="gzip",
            chunks=True,
        )

        _ranges = x.get_ranges()
        ghandle.create_dataset(
            "start",
            data=_ranges.get_start(),
            dtype="i4",
            compression="gzip",
            chunks=True,
        )

        ghandle.create_dataset(
            "width",
            data=_ranges.get_width(),
            dtype="u4",
            compression="gzip",
            chunks=True,
        )

        ghandle.create_dataset(
            "strand",
            data=x.get_strand(),
            dtype="i4",
            compression="gzip",
            chunks=True,
        )

        if x.get_names() is not None:
            dl._utils_vector.write_string_list_to_hdf5(ghandle, "name", x.get_names())

    _range_annotation = x.get_mcols()
    if _range_annotation is not None and _range_annotation.shape[1] > 0:
        dl.save_object(_range_annotation, path=os.path.join(path, "range_annotations"))

    _meta = x.get_metadata()
    if _meta is not None and len(_meta) > 0:
        dl.save_object(_meta, path=os.path.join(path, "other_annotations"))

    return
