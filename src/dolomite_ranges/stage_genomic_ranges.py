import dolomite_base as dl
from dolomite_base import stage_object, write_metadata
from biocframe import BiocFrame
from genomicranges import GenomicRanges, SeqInfo
from typing import Any
from collections import OrderedDict
import os


@stage_object.register
def stage_genomic_ranges(x: GenomicRanges, dir: str, path: str, is_child: bool = False, **kwargs) -> dict[str, Any]:
    """Method for saving :py:class:`~genomicranges.GenomicRanges.GenomicRanges`
    objects to their corresponding file representations, see
    :py:meth:`~dolomite_base.stage_object.stage_object` for details.

    Args:
        x: Object to be staged.

        dir: Staging directory.

        path: Relative path inside ``dir`` to save the object.

        is_child: Is ``x`` a child of another object?

        kwargs: Further arguments, ignored.

    Returns:
        Metadata that can be edited by calling methods and then saved with 
        :py:meth:`~dolomite_base.write_metadata.write_metadata`.
    """
    os.mkdir(os.path.join(dir, path))

    df = BiocFrame(
        { 
            "seqnames": x.seqnames,
            "start": x.start,
            "end": [y - 1 for y in x.end], # inclusive end.
            "strand": x.strand
        },
        row_names = x.row_names
    )
    oname = "ranges.csv.gz"
    dl.write_csv(df, os.path.join(dir, path, oname))

    si = x.seq_info
    if si is None:
        all_seqnames = list(set(x.seqnames))
        si = SeqInfo(
            seqnames=all_seqnames,
            seqlengths=[None] * len(all_seqnames),
            is_circular=[None] * len(all_seqnames),
            genome=[None] * len(all_seqnames)
        )
    seq_info = stage_object(si, dir, path + "/seqinfo", is_child = True)
    seq_resource = write_metadata(seq_info, dir=dir)

    gr_meta = {
        "compression": "gzip",
        "length": len(x),
        "sequence_information": { "resource": seq_resource },
    }

    if x.metadata is not None and len(x.metadata):
        other_meta = stage_object(x.metadata, dir, path + "/metadata", is_child=True)
        gr_meta["other_data"] = { "resource": write_metadata(other_meta, dir=dir) }

    mc = x.mcols()
    if isinstance(mc, OrderedDict):
        mc = BiocFrame(mc, number_of_rows=len(x))
    if mc is not None and mc.shape[1] > 0:
        other_meta = stage_object(mc, dir, path + "/mcols", is_child=True)
        gr_meta["range_data"] = { "resource": write_metadata(other_meta, dir=dir) }

    return {
        "$schema": "genomic_ranges/v1.json",
        "path": path + "/" + oname,
        "is_child": is_child,
        "genomic_ranges": gr_meta
    }
