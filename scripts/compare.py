import sys
import filecmp

def main():
    try:
        dir1, dir2 = sys.argv[1:]
    except Exception as e:
        raise SystemExit(e.__cause__)

    common = [
        'fitgeoid1.err',
        'fitgeoid1.in',
        'fitgeoid1.out',
        'fitgeoid_dif.dat',
        'fitgeoid_dif.err',
        'fitgeoid_dif.gri',
        'fitgeoid_dif2.dat',
        'gbin.err',
        'gbin.in',
        'gbin.out',
        'geoid.err',
        'geoid.in',
        'geoid.out',
        'geoid_fitted.bin',
        'geoid_fitted.gri',
        'gps_measurements_subset.n',
        'point_excluded.dat',
        'point_interpolated.dat',
    ]

    matches, mismatches, errors = filecmp.cmpfiles(dir1, dir2, common, shallow=True)

    print('Matches')
    print('\n'.join(matches))

    print('\nMismatches')
    print('\n'.join(mismatches))

    print('\nErrors')
    print('\n'.join(errors))


if __name__ == '__main__':
    main()
