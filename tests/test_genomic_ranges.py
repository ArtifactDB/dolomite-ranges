# from genomicranges import GenomicRanges, SeqInfo 
# import dolomite_ranges
# from dolomite_base import write_metadata, stage_object
# from tempfile import mkdtemp
# from biocframe import BiocFrame
# import os


# def test_genomic_ranges():
#     gr = GenomicRanges(
#         {
#             "seqnames": ["chrA", "chrB", "chrC"],
#             "starts": [10, 30, 2200],
#             "ends": [20,50,3000],
#             "strand": ["*", "+", "-"]
#         }
#     )

#     dir = mkdtemp()
#     meta = stage_object(gr, dir, "foo")
#     write_metadata(meta, dir)

#     roundtrip = dolomite_ranges.load_genomic_ranges(meta, dir)
#     assert roundtrip.seqnames == gr.seqnames
#     assert roundtrip.start == gr.start
#     assert roundtrip.end == gr.end
#     assert roundtrip.strand == gr.strand


# #def test_genomic_ranges_full_load():
# #    gr = GenomicRanges(
# #        {
# #            "seqnames": ["chrA", "chrB", "chrC"],
# #            "starts": [10, 30, 2200],
# #            "ends": [20,50,3000],
# #            "strand": ["*", "+", "-"],
# #        }
# #    )
# #
# #    gr.metadata = { "ARG": [5, 3, 2, 1 ] }
# #    gr.seq_info = SeqInfo(
# #        seqnames = [ "chrA", "chrB", "chrC" ],
# #        seqlengths = [ 1000, 2000, 3000 ],
# #        is_circular = [ False ] * 3,
# #        genome = [ "hg38" ] * 3
# #    )
# #
# #    dir = mkdtemp()
# #    meta = stage_object(gr, dir, "foo")
# #    write_metadata(meta, dir)
# #
# #    roundtrip = dolomite_ranges.load_genomic_ranges(meta, dir)
# #    assert roundtrip.seq_info.seqlengths == gr.seq_info.seqlengths
# #    assert roundtrip.metadata == gr.metadata
