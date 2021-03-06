import pandas as pd


def apply_cat_op(
    data: pd.DataFrame,
    attrs: [str],
    operation,
    prefix: str
):
    """
    Apply one operation to data attributes.
    """
    series = [data[attr].map(operation) for attr in attrs]

    _data = pd.concat(series, axis=1).add_prefix(prefix)
    new_attrs = _data.columns.values

    return _data, new_attrs


def apply_cat_ops(
    data: pd.DataFrame,
    attrs: [str],
    operations: [],
    prefixes: [str]
):
    """
    Apply a bunch of operatins to data attributes.
    """

    assert len(operations) == len(prefixes), \
        'Number of prefixes not equal to number of operations'

    result = [apply_cat_op(data, attrs, operation, prefix)
              for (operation, prefix) in zip(operations, prefixes)]
    data_frames, akk = zip(*result)

    _data = pd.concat(data_frames, axis=1)
    new_attrs = _data.columns.values

    return _data, new_attrs
