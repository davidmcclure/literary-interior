

import pytest

from lint.utils import flatten_dict


@pytest.mark.parametrize('d,flat', [

    (

        {
            '1_1': {
                '2_1': {
                    '3_1': 1,
                    '3_2': 2,
                },
                '2_2': {
                    '3_3': 3,
                    '3_4': 4,
                },
            },
            '1_2': {
                '2_3': {
                    '3_5': 5,
                    '3_6': 6,
                },
                '2_4': {
                    '3_7': 7,
                    '3_8': 8,
                },
            },
        },

        [
            (('1_1', '2_1', '3_1'), 1),
            (('1_1', '2_1', '3_2'), 2),
            (('1_1', '2_2', '3_3'), 3),
            (('1_1', '2_2', '3_4'), 4),
            (('1_2', '2_3', '3_5'), 5),
            (('1_2', '2_3', '3_6'), 6),
            (('1_2', '2_4', '3_7'), 7),
            (('1_2', '2_4', '3_8'), 8),
        ]

    )

])
def test_flatten_dict(d, flat):

    result = list(flatten_dict(d))

    assert len(result) == len(flat)
    assert set(result) == set(flat)
