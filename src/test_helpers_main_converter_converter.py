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

        self.assertEqual(converter_exit(method, "abc", "error"), "abc")
        self.assertEqual(converter_exit(method, "input", "error"), "input")
        crash = True
        self.assertEqual(converter_exit(method, "input", "error", True), "error")

    def test_converter_string_boolean(self):
        self.assertEqual(converter_string_boolean("True"), (True, False))
        self.assertEqual(converter_string_boolean("False"), (False, False))
        self.assertEqual(converter_string_boolean("true"), self.fail_tuple)
        self.assertEqual(converter_string_boolean("false"), self.fail_tuple)

    def test_converter_string_int(self):
        self.assertEqual(converter_string_int("10"), (10, False))
        self.assertEqual(converter_string_int("10.5"), self.fail_tuple)
        self.assertEqual(converter_string_int("abc"), self.fail_tuple)
        self.assertEqual(converter_string_int("ab c"), self.fail_tuple)

    def test_converter_string_list_int(self):
        self.assertEqual(converter_string_list_int("1,2,3"), ([1, 2, 3], False))
        self.assertEqual(converter_string_list_int("1,2"), ([1, 2], False))
        self.assertEqual(converter_string_list_int("1,2,4"), ([1, 2, 4], False))
        self.assertEqual(converter_string_list_int("1,2,abc"), self.fail_tuple)
        self.assertEqual(converter_string_list_int("1,2,3,abc"), self.fail_tuple)
        self.assertEqual(converter_string_list_int("abc,1,2,3"), self.fail_tuple)
        self.assertEqual(converter_string_list_int("1,2,3,a"), self.fail_tuple)
        self.assertEqual(converter_string_list_int("1.2"), self.fail_tuple)


if __name__ == "__main__":
    unittest.main()
