import decimal
import unittest
import context
import sheets

class TestWorkbook(unittest.TestCase):
    def test_smoke_test(self):
        # Should print the version number of your sheets library,
        # which should be 1.0 for the first project.
        print(f'Using sheets engine version {sheets.version}')

        # Make a new empty workbook
        wb = sheets.Workbook()
        (index, name) = wb.new_sheet()

        # Should print:  New spreadsheet "Sheet1" at index 0
        print(f'New spreadsheet "{name}" at index {index}')

        wb.set_cell_contents(name, 'a1', '12')
        wb.set_cell_contents(name, 'b1', '34')
        wb.set_cell_contents(name, 'c1', '=a1+b1')

        # value should be a decimal.Decimal('46')
        value = wb.get_cell_value(name, 'c1')
        self.assertEqual(value, decimal.Decimal('46'))

        # Should print:  c1 = 46
        print(f'c1 = {value}')

        wb.set_cell_contents(name, 'd3', '=nonexistent!b4')

        # value should be a CellError with type BAD_REFERENCE
        value = wb.get_cell_value(name, 'd3')
        self.assertTrue(isinstance(value, sheets.CellError))
        self.assertEqual(value.get_type(), sheets.CellErrorType.BAD_REFERENCE)

        # Cells can be set to error values as well
        wb.set_cell_contents(name, 'e1', '#div/0!')
        wb.set_cell_contents(name, 'e2', '=e1+5')
        value = wb.get_cell_value(name, 'e2')
        self.assertTrue(isinstance(value, sheets.CellError))
        self.assertEqual(value.get_type(), sheets.CellErrorType.DIVIDE_BY_ZERO)


    def test_is_cell_location_valid(self):
        # Make a new empty workbook
        wb = sheets.Workbook()
        self.assertTrue(wb.is_valid_cell_location('a15'))
        self.assertTrue(wb.is_valid_cell_location('A15'))
        self.assertTrue(wb.is_valid_cell_location('ZZZZ9999'))
        self.assertFalse(wb.is_valid_cell_location(' a15'))
        self.assertFalse(wb.is_valid_cell_location(' a15 '))
        self.assertFalse(wb.is_valid_cell_location(''))
        self.assertFalse(wb.is_valid_cell_location(' '))
        self.assertFalse(wb.is_valid_cell_location('SHEET1'))
        self.assertFalse(wb.is_valid_cell_location('0'))
        self.assertFalse(wb.is_valid_cell_location('!'))

if __name__ == '__main__':
    unittest.main()
