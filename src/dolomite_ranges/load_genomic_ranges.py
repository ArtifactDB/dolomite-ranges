import dolomite_base as dl
from genomicranges import GenomicRanges
from typing import Any
import numpy

from .read_sequence_information import load_sequence_information



def load_genomic_ranges(meta: dict[str, Any], project, **kwargs) -> GenomicRanges:
    """
    Load genomic ranges into a
    :py:class:`~genomicranges.GenomicRanges.GenomicRanges` object. This method
    should generally not be called directly but instead be invoked by
    :py:meth:`~dolomite_base.load_object.load_object`.

    Args:
        meta: Metadata for this object.

        project: Value specifying the project of interest. This is most
            typically a string containing a file path to a staging directory
            but may also be an application-specific object that works with
            :py:meth:`~dolomite_base.acquire_file.acquire_file`.

        kwargs: Further arguments, ignored.

    Returns:
        A :py:class:`~genomicranges.GenomicRanges.GenomicRanges` object.
    """
    p = dl.acquire_file(project, meta["path"])

    grmeta = meta["genomic_ranges"]
    compmethod = "none"
    if "compression" in grmeta:
        compmethod = grmeta["compression"]

    names, fields = dl.read_csv(p, grmeta["length"], compression=compmethod)
    contents = dict(zip(names, fields))
    gr = GenomicRanges(
        {
            "seqnames": contents["seqnames"],
            "starts": list(contents["start"]),
            "ends": [e + 1 for e in contents["end"]],
            "strand": contents["strand"]
        }
    )

    smeta = dl.acquire_metadata(project, grmeta["sequence_information"]["resource"]["path"])
    gr.seq_info = load_sequence_information(smeta, project)

    if "other_data" in grmeta:
        print(project)
        ometa = dl.acquire_metadata(project, grmeta["other_data"]["resource"]["path"])
        gr.metadata = dl.load_object(ometa, project)
    
    if "range_data" in grmeta:
        rmeta = dl.acquire_metadata(project, grmeta["range_data"]["resource"]["path"])
        gr.mcols = dl.load_object(rmeta, project)

    return gr
