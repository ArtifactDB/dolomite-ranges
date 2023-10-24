import dolomite_base as dl
from dolomite_base import stage_object
from genomicranges import SeqInfo
from biocframe import BiocFrame
from typing import Any
import os


@stage_object.register
def stage_sequence_information(x: SeqInfo, dir: str, path: str, is_child: bool = False, **kwargs) -> dict[str, Any]:
    os.mkdir(os.path.join(dir, path))

    df = BiocFrame(
        { 
            "seqnames": x.get_seqnames(),
            "seqlengths": x.get_seqlengths(),
            "isCircular": x.get_is_circular(),
            "genome": x.get_genome(),
        },
        number_of_rows=len(x)
    )

    oname = "seqinfo.csv.gz"
    dl.write_csv(df, os.path.join(dir, path, oname))

    return {
        "$schema": "sequence_information/v1.json",
        "path": path + "/" + oname,
        "is_child": is_child,
        "sequence_information": {
            "compression": "gzip",
            "dimensions": [len(x), 4]
        }
    }
