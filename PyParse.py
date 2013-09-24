"""
PyParse v1.0
    The overall goal of this project was to make parsing files an easier
    and more *maintainable* task.
    Author: Matthew H. Johnson, PharmD.
"""

import csv

class Parser(object):
    def __init__(self, filepath, field_map, dialect=None,
            has_header=None, line_skip=0):
        """Initializes parser 
        Arguments:
            filepath (str)    : path of target file
            field_map (dict)  : fieldname -> index (int) value map of fields for rows
            dialect (obj)     : optional, predefined csv dialect
                                if not provided in kwargs, will attempt to auto-detect 
                                the csv dialect 
            has_header (bool) : required, if not specified in dialect kwarg
                                optional, if relying on auto-detection
                                for dialect
            line_skip (int)   : optional, default = 0;
                                in case junk is present at top of file,
                                this is an easy way to skip initial lines
                                containing junk data
        """
        self.has_header = has_header
        self.field_map  = field_map
        self.header     = field_map.keys()
        self.filepath   = filepath

        # auto-detects csv dialect if not provided one
        if not dialect:
            dialect    = self._dialect(filepath)
        self.dialect   = dialect
        self.reader    = csv.reader(open(filepath, 'rb'), dialect=dialect)

        # skip junk data if specified
        for i in range(line_skip):
            self.reader.next()

        # skip first row if file is thought to have header
        if self.has_header:
            self.reader.next()

    def field_value(self, row, field_name):
        """extracts value based on predefined fieldname expressed in field_map
        Arguments
            row (list)       : target row
            field_name (str) : pre-defined target name of field
        Returns:
            index value of field || None if fieldname not found
        """
        try:
            return row[self.field_map[field_name]]
        except IndexError:
            return None
        return

    def row_dict(self, row):
        """returns dictionary version of row using keys from self.field_map"""
        d = {}
        for field_name,index in self.field_map.items():
            d[field_name] = self.field_value(row, field_name)
        return d

    def _dialect(self, filepath):
        """returns detected dialect of filepath and sets self.has_header
        if not passed in __init__ kwargs
        Arguments:
            filepath (str): filepath of target csv file
        """
        with open(filepath, 'rb') as csvfile:
            sample = csvfile.read(1024)
            dialect = csv.Sniffer().sniff(sample)
            if self.has_header == None:
                # detect header if header not specified
                self.has_header = csv.Sniffer().has_header(sample)
            csvfile.seek(0)
        return dialect

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "{0}".format(self.filepath) % self.filepath

    def __iter__(self):
        return self

    def next(self):
        try:
            row = self.reader.next()
            return self.row_dict(row)
        except StopIteration:
            raise StopIteration


if __name__ == '__main__':
    pass
        
