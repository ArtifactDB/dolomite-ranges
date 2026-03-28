import dolomite_base as dl
from compressed_lists import CompressedSplitBiocFrameList

from .save_atomic_vector_list import _save_compressed_list


@dl.save_object.register
@dl.validate_saves
def save_compressed_genomic_ranges_list(x: CompressedSplitBiocFrameList, path: str, **kwargs):
    """Method for saving :py:class:`~compressed_lists.biocframe_list.CompressedSplitBiocFrameList`
    objects to their corresponding file representations, see
    :py:meth:`~dolomite_base.save_object.save_object` for details.

    Args:
        x:
            Object to be staged.

        path:
            Path to a directory in which to save ``x``.

        data_frame_args:
            Further arguments to pass to the ``save_object`` method for
            ``mcols``.

        kwargs:
            Further arguments to be passed to individual methods.

    Returns:
        `x` is saved to `path`.
    """
    return _save_compressed_list(x, path=path, name="genomic_ranges_list", **kwargs)
