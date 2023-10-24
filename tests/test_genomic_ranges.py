from genomicranges import GenomicRanges 
import dolomite_ranges
from dolomite_base import write_metadata, stage_object
from tempfile import mkdtemp
import os


def test_genomic_ranges():
    gr = GenomicRanges(
        BiocFrame({
            "seqnames": ["chrA", "chrB", "chrC"],
            "start": [10, 30, 2200],
            "end": [20,50,3000],
            "strand": ["*", "+", "-"]
        })
    )

    dir = mkdtemp()
    meta = stage_object(gr, dir, "foo")
    write_metadata(meta, dir)

    roundtrip = dolomite_ranges.load_genomic_ranges(meta, dir)
