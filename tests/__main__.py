import errno
import unittest

import filtertool.cli as cli
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
            "overlay", "python.png", ".5", ".5",
            "rotate", "90",
            "overlay", "python.png", "1", ".1"
            ]
        expected = [
            (filter_gs, {}),
            (filter_gs, {}),
            (filter_rot, {"DEGREES": 180}),
            (filter_gs, {}),
            (filter_overlay, {"IMG_2": "python.png","X_PLACE":.5,"Y_PLACE":.5}),
            (filter_rot, {"DEGREES": 90}),
            (filter_overlay, {"IMG_2": "python.png","X_PLACE":1,"Y_PLACE":.1}),
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
        args = ["overlay", "document.pdf", ".5", ".5"]
        with self.assertRaises(SystemExit) as cm:
            cli.gen_filter_sequence(args)

        self.assertEqual(cm.exception.code, errno.EINVAL)


if __name__ == '__main__':
    unittest.main()
