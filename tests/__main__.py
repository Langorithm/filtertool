import errno
import unittest

import filtertool.cli as cli
import filtertool.filter_class as filter_class
import filtertool.exceptions as exceptions
from filtertool.filter_class import *


class CLITestCase(unittest.TestCase):

    def test_gen_filter_sequence_single_correct(self):
        args = ["gRaYsCale"]
        expected = [
            (filter_gs, {})
        ]
        seq = cli.gen_filter_sequence(args)
        self.assertEqual(expected, seq)

    def test_gen_filter_sequence_long_correct(self):
        args = [
            "gRaYsCale",
            "grayscale",
            "rotate", "180",
            "grayscale",
            "overlay", "python.png",
            "rotate", "90",
            "overlay", "python.png"
            ]
        expected = [
            (filter_gs, {}),
            (filter_gs, {}),
            (filter_rot, {"Degrees": 180}),
            (filter_gs, {}),
            (filter_overlay, {"Image2_filename": "python.png"}),
            (filter_rot, {"Degrees": 90}),
            (filter_overlay, {"Image2_filename": "python.png"}),
        ]
        seq = cli.gen_filter_sequence(args)
        self.assertEqual(expected, seq)

    def test_gen_filter_sequence_empty(self):
        args = []
        expected = []
        seq = cli.gen_filter_sequence(args)
        self.assertEqual(args, seq)

    def test_gen_filter_sequence_wrong_type(self):
        args = ["rotate", "ninety"]
        with self.assertRaises(SystemExit) as cm:
            cli.gen_filter_sequence(args)

        self.assertEqual(cm.exception.code, errno.EINVAL)

    def test_gen_filter_sequence_invalid_param(self):
        args = ["overlay", "document.pdf"]
        with self.assertRaises(SystemExit) as cm:
            cli.gen_filter_sequence(args)

        self.assertEqual(cm.exception.code, errno.EINVAL)


class OutputTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_main(self):
        pass

    def test_(self):
        pass

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
