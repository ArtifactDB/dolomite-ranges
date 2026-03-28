from typing import Optional

from dolomite_base.read_object import read_object_registry
from genomicranges import CompressedGenomicRangesList

from .read_atomic_vector_list import _read_compressed_list

read_object_registry["genomic_ranges_list"] = "dolomite_ranges.read_genomic_ranges_list"


def read_genomic_ranges_list(path: str, metadata: Optional[dict], **kwargs) -> CompressedGenomicRangesList:
    """Load genomic ranges into a
    :py:class:`~genomicranges.grangeslist.CompressedGenomicRangesList` object.

    This method
    should generally not be called directly but instead be invoked by
    :py:meth:`~dolomite_base.read_object.read_object`.

    Args:
        path:
            Path to the directory containing the object.

        metadata:
            Metadata for the object.

        kwargs:
            Further arguments, ignored.

    Returns:
        A :py:class:`~genomicranges.grangeslist.CompressedGenomicRangesList` object.
    """

    return _read_compressed_list(path, metadata=metadata, name="genomic_ranges_list", **kwargs)
