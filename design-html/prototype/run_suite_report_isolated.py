"""Redirect only one QA JSON report; test actions and application storage stay real."""
import argparse
import errno
import os
from pathlib import Path
import runpy
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--script', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    script, original, destination = args.script.resolve(), args.report.resolve(), args.output.resolve()
    assert script.parent == root
    assert original.is_relative_to(root / 'evidence/current') and destination.is_relative_to(root / 'evidence/current')
    assert original != destination
    write_text = Path.write_text

    def report_write(path, value, *options, **kwargs):
        if path.resolve() != original:
            return write_text(path, value, *options, **kwargs)
        temporary = destination.with_name(destination.name + '.tmp-' + str(os.getpid()))
        for attempt in range(10):
            try:
                result = write_text(temporary, value, *options, **kwargs)
                temporary.replace(destination)
                return result
            except OSError as error:
                if error.errno not in [errno.EINVAL, errno.EACCES, errno.EPERM] or attempt == 9:
                    raise
                time.sleep(0.05)
        raise AssertionError('Report writer did not finish')

    Path.write_text = report_write
    sys.argv = [str(script)]
    runpy.run_path(str(script), run_name='__main__')


if __name__ == '__main__':
    main()
