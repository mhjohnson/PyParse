import unittest
from PyParse import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.filepath = 'tests/example.csv'
        self.field_map = {
            "facilityType"  : 0,
            "state"         : 1,
            "facilityName"  : 2,
            "shpNumAn"      : 3,
            "shpCentre"     : 4,
            "streetAddress" : 5,
            "locality"      : 6,
            "postalcode"    : 7,
            "hrsBusiness"   : 8,
            "wheelChair"    : 9,
            "displayWD"     : 10,
            "facilityType2" : 11,
            "xCoord"        : 12,
            "yCoord"        : 13,
            "uuid"          : 14,
            "result"        : 15,
            "audio"         : 16 }

    def test_header_detection(self):
        """test that it detects that file has header"""
        parser = Parser(self.filepath, self.field_map)
        self.assertTrue(parser.has_header, "File should be detected has having a header")

    def test_no_header_detection(self):
        """test that it detects no header for file that does not contain header"""
        filepath = 'tests/example_noheader.csv'
        parser = Parser(filepath, self.field_map)
        self.assertFalse(parser.has_header, "File should NOT be detected as having a header")

    def test_header_override(self):
        """test forcing parser to recognize header state if it is forced"""
        filepath = 'tests/example_noheader.csv'

        parser_w_header = Parser(self.filepath, self.field_map,
                has_header=False)

        parser_no_header = Parser(filepath, self.field_map,
                has_header=True)

        self.assertFalse(parser_w_header.has_header, "Forced state should not have header")
        self.assertTrue(parser_no_header.has_header, "Forced state should have header")

    def test_skip_header_row_if_present(self):
        """should skip returning header if header is detected"""
        parser = Parser(self.filepath, self.field_map)
        first_row = parser.next()
        self.assertNotEqual(first_row['facilityType'], 'Fcilty_typ', "Header row should be skipped if present")

    def test_selective_field_map(self):
        """Check that field map is returning only desired fields based
        on field map"""
        custom_field_map = {'state':1, 'streetAddress':5}
        parser = Parser(self.filepath, custom_field_map)
        first_row = parser.next()
        self.assertEqual(first_row['state'], 'NSW')
        self.assertEqual(first_row['streetAddress'], '131 Monaro Street')
        self.assertEqual(len(first_row.keys()), 2, "dictionary should only represent 2 fields!")

    def test_skip_junk_data_by_kw(self):
        """Check that Parser will skip junk data (eg: description) at top of file and find first row
        by a keyword"""

        filepath = 'tests/example_w_junk_heading.csv'
        options = {
                'has_header'  : True, # must be forced
                'firstRow_kw' : 'Fcilty_typ',
        }

        parser = Parser(filepath, self.field_map, **options)
        first_row = parser.next()
        self.assertEqual(first_row['facilityName'], 'Queanbeyan', "Should have return first row with anticipated facilityName")
        

    def test_clean_end(self):
        parser = Parser(self.filepath, self.field_map)
        for d in parser:
            pass

if __name__ == '__main__':
    unittest.main()

