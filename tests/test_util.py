from gfit.util import (
    input_fitgeoid1,
    input_gbin,
    input_geoid,
    make_point_line,
    parse_point_line,
)


def test_input_fitgeoid1():
    expected = """\
file1.gri
file2.n
file3.gri
20 1 1 t
60.0 0.004
53.50 58.00 7.00 17.000020  0.010 0.0166667
"""

    result = input_fitgeoid1('file1.gri', 'file2.n', 'file3.gri')
    assert result == expected


def test_input_gbin():
    expected = """\
geoid.gri
geoid.bin
1
"""

    result = input_gbin('geoid.gri', 'geoid.bin')
    assert result == expected



def test_input_geoid():
    expected = """\
1
geoid.bin
y
point_001.txt
point_001.out
1
"""

    result = input_geoid('geoid.bin', 'point_001.txt', 'point_001.out')
    assert result == expected

    test_data = dict(
        geoid_fitted_bin='geoid.bin',
        point_excluded='point_001.txt',
        point_interpolated='point_001.out',
        not_a_keyword=False,
    )
    result = input_geoid(**test_data)
    assert result == expected


def test_make_point_line():
    test_data = '855110\t56.16540394\t10.20053619\t34.832\t38.9953 0.004'
    expected = '855110\t56.16540394\t10.20053619\n'

    result = make_point_line(test_data)
    assert result == expected


def test_parse_point_line():
    test_data = '   887339   56.75560099  10.29286094    38.082'
    expected = 887339, 38.082
    result = parse_point_line(test_data)
    assert result == expected

