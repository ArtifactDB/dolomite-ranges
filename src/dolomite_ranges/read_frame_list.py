from typing import Optional

from compressed_lists import CompressedSplitBiocFrameList
from dolomite_base.read_object import read_object_registry

from .read_atomic_vector_list import _read_compressed_list

read_object_registry["data_frame_list"] = "dolomite_ranges.read_data_frame_list"


def read_data_frame_list(path: str, metadata: Optional[dict], **kwargs) -> CompressedSplitBiocFrameList:
    """Load data frame list.

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
        A :py:class:`~compressed_lists.biocframe_list.CompressedSplitBiocFrameList` object.
    """

    return _read_compressed_list(path, metadata=metadata, name="data_frame_list", **kwargs)
