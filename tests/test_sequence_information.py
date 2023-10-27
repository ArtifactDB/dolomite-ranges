from genomicranges import SeqInfo
import dolomite_ranges
from dolomite_base import write_metadata, stage_object
from tempfile import mkdtemp
import os


def test_sequence_information():
    si = SeqInfo(
        ["chrA", "chrB", "chrC"],
        [10, None, 2200],
        [None,True,False],
        ["hg19","hg38",None]
    )

    dir = mkdtemp()
    meta = stage_object(si, dir, "foo")
    write_metadata(meta, dir)

    roundtrip = dolomite_ranges.load_sequence_information(meta, dir)
    assert roundtrip.get_seqnames() == si.get_seqnames()
    assert roundtrip.get_seqlengths() == si.get_seqlengths()
    assert roundtrip.get_is_circular() == si.get_is_circular()
    assert roundtrip.get_genome() == si.get_genome()


def test_sequence_information_all_none():
    si = SeqInfo(
        ["chrA", "chrB", "chrC"],
        [None] * 3,
        [None] * 3,
        [None] * 3
    )

    dir = mkdtemp()
    meta = stage_object(si, dir, "foo")
    write_metadata(meta, dir)

    roundtrip = dolomite_ranges.load_sequence_information(meta, dir)
    assert roundtrip.get_seqnames() == si.get_seqnames()
    assert roundtrip.get_seqlengths() == si.get_seqlengths()
    assert roundtrip.get_is_circular() == si.get_is_circular()
    assert roundtrip.get_genome() == si.get_genome()
