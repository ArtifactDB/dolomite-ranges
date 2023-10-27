import dolomite_base as dl
from genomicranges import SeqInfo
from typing import Any
import numpy


def load_sequence_information(meta: dict[str, Any], project, **kwargs) -> SeqInfo:
    """
    Load sequence information into a :py:class:`~genomicranges.SeqInfo.SeqInfo`
    object. This method should generally not be called directly but instead be
    invoked by :py:meth:`~dolomite_base.load_object.load_object`.

    Args:
        meta: Metadata for this object.

        project: Value specifying the project of interest. This is most
            typically a string containing a file path to a staging directory
            but may also be an application-specific object that works with
            :py:meth:`~dolomite_base.acquire_file.acquire_file`.

        kwargs: Further arguments, ignored.

    Returns:
        A :py:class:`~genomicranges.SeqInfo.SeqInfo` object.
    """
    p = dl.acquire_file(project, meta["path"])

    seqmeta = meta["sequence_information"]
    compmethod = "none"
    if "compression" in seqmeta:
        compmethod = seqmeta["compression"]

    names, fields = dl.read_csv(p, num_rows=seqmeta["dimensions"][0], compression=compmethod)
    contents = dict(zip(names, fields))

    seqlengths = []
    for x in contents["seqlengths"]:
        if numpy.ma.is_masked(x):
            seqlengths.append(None)
        else:
            seqlengths.append(int(x))

    is_circular = []
    for x in contents["isCircular"]:
        if numpy.ma.is_masked(x):
            is_circular.append(None)
        else:
            is_circular.append(bool(x))

    genome = []
    for x in contents["genome"]:
        if numpy.ma.is_masked(x) or x is None:
            genome.append(None)
        else:
            genome.append(str(x))

    return SeqInfo(contents["seqnames"], seqlengths, is_circular, genome)
