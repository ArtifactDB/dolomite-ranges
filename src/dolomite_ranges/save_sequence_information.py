import os
from typing import Any

import dolomite_base as dl
from biocframe import BiocFrame
from dolomite_base.save_object import save_object, validate_saves
from genomicranges import SeqInfo


@save_object.register
@validate_saves
def save_sequence_information(
    x: SeqInfo, path: str, is_child: bool = False, **kwargs
) -> dict[str, Any]:
    """

    Args:
        x: 
            Object to be saved.

        path: 
            Path to a directory in which to save ``x``.
            
        is_child (bool, optional): _description_. Defaults to False.

    Returns:
        dict[str, Any]: _description_
    """
    os.mkdir(os.path.join(dir, path))

    df = BiocFrame(
        {
            "seqnames": x.get_seqnames(),
            "seqlengths": x.get_seqlengths(),
            "isCircular": x.get_is_circular(),
            "genome": x.get_genome(),
        },
        number_of_rows=len(x),
    )

    oname = "seqinfo.csv.gz"
    dl.write_csv(df, os.path.join(dir, path, oname))

    return {
        "$schema": "sequence_information/v1.json",
        "path": path + "/" + oname,
        "is_child": is_child,
        "sequence_information": {"compression": "gzip", "dimensions": [len(x), 4]},
    }
