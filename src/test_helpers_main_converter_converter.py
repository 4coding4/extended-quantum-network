import unittest

from src.helper.main.converter.converter import converter_string_boolean, converter_string_int, \
    converter_string_list_int, converter_exit


class TestHelpersMainConverterConverter(unittest.TestCase):
    fail_tuple = (None, True)

    def test_converter_exit(self):
        # create callable functions for testing
        crash = False

        def method(input: str) -> tuple:
            if crash:
                return None, True
            else:
                return input, False

        self.assertEqual("abc",
                         converter_exit(method, "abc", "error"))
        self.assertEqual("input",
                         converter_exit(method, "input", "error"))
        crash = True
        self.assertEqual("error",
                         converter_exit(method, "input", "error", True))

    def test_converter_string_boolean(self):
        self.assertEqual((True, False),
                         converter_string_boolean("True"))
        self.assertEqual((False, False),
                         converter_string_boolean("False"))
        self.assertEqual(self.fail_tuple,
                         converter_string_boolean("true"))
        self.assertEqual(self.fail_tuple,
                         converter_string_boolean("false"))

    def test_converter_string_int(self):
        self.assertEqual((10, False),
                         converter_string_int("10"))
        self.assertEqual(self.fail_tuple,
                         converter_string_int("10.5"))
        self.assertEqual(self.fail_tuple,
                         converter_string_int("abc"))
        self.assertEqual(self.fail_tuple,
                         converter_string_int("ab c"))

    def test_converter_string_list_int(self):
        self.assertEqual(([1, 2, 3], False),
                         converter_string_list_int("1,2,3"))
        self.assertEqual(([1, 2], False),
                         converter_string_list_int("1,2"))
        self.assertEqual(([1, 2, 4], False),
                         converter_string_list_int("1,2,4"))
        self.assertEqual(self.fail_tuple,
                         converter_string_list_int("1,2,abc"))
        self.assertEqual(self.fail_tuple,
                         converter_string_list_int("1,2,3,abc"))
        self.assertEqual(self.fail_tuple,
                         converter_string_list_int("abc,1,2,3"))
        self.assertEqual(self.fail_tuple,
                         converter_string_list_int("1,2,3,a"))
        self.assertEqual(self.fail_tuple,
                         converter_string_list_int("1.2"))


if __name__ == "__main__":
    unittest.main()
