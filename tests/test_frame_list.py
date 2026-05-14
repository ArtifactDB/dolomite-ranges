import os
from tempfile import mkdtemp

from biocframe import BiocFrame
from dolomite_base import read_object, save_object
from compressed_lists import CompressedSplitBiocFrameList
import numpy as np
import dolomite_ranges


def test_dataframe_list():
    a = BiocFrame({
        "seqnames":["chr1", "chr2", "chr1", "chr3"],
        "strand":["-", "+", "*", "+"],
        "mcols":BiocFrame({"score": [1, 2, 3, 4]})
    })

    b = BiocFrame({
        "seqnames":["chr2", "chr4", "chr5"],
        "strand":["-", "+", "*"],
        "mcols":BiocFrame({"score": [2, 3, 4]})
    })

    gdf = CompressedSplitBiocFrameList.from_list(lst=[a, b], names=["a", "b"])

    dir = os.path.join(mkdtemp(), "dframe")
    save_object(gdf, dir)

    roundtrip = read_object(dir)
    assert isinstance(roundtrip, CompressedSplitBiocFrameList)
    assert roundtrip.get_names() == gdf.get_names()
    assert len(roundtrip.get_unlist_data()) == len(gdf.get_unlist_data())
    assert list(roundtrip[0].get_column("seqnames")) == gdf[0].get_column("seqnames")
    assert list(roundtrip[0].get_column("strand")) ==gdf[0].get_column("strand")


def test_dframe_empty():
    gdf = CompressedSplitBiocFrameList.empty(n=100)

    print(gdf)

    dir = os.path.join(mkdtemp(), "dframe_empty")
    save_object(gdf, dir)

    roundtrip = read_object(dir)
    assert roundtrip.get_names() == gdf.get_names()
    assert len(roundtrip.get_unlist_data()) == len(gdf.get_unlist_data())
    assert np.allclose(roundtrip.get_element_lengths(), gdf.get_element_lengths())