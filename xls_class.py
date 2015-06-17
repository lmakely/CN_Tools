__author__ = 'Jwely'

try:
    import xlrd
    import xlwt

except ImportError:
    import pip
    pip.main(["install", "xlrd"])
    pip.main(["install", "xlwt"])
    import xlrd
    import xlwt



class xls_class():
    """
    class for reading and writing xls files.
    """

    def __init__(self):

        self.filepath   = ""
        self.workbook   = None
        self.worksheets = {}

        return


    def read(self, filepath):
        """

        :param filepath: filepath to xlsx or xls file to read.
        :return:
        """

        self.filepath   = filepath
        workbook        = xlrd.open_workbook(self.filepath)
        self.sheetnames = workbook.sheet_names()

        for sheetname in self.sheetnames:
            new_sheet = sheet(sheetname, self.filepath)
            new_sheet.read(workbook)
            self.worksheets[sheetname] = new_sheet

        return self.worksheets


    def write(self, filepath):

        book = xlwt.Workbook(encoding = " utf-8")

        for sheet in self.worksheets:
            self.worksheets[sheet].write(book)
        book.save(filepath)
        return filepath




class sheet():

    def __init__(self, name, filepath):

        self.name       = name
        self.filepath   = filepath
        self.rows       = []
        return


    def __getitem__(self, (row, col)):
        return self.rows[row][col]


    def __setitem__(self, (row, col), value):
        self.rows[row][col] = value
        return


    def viewsheet(self):
        """
        :return: prints a heads up view of this sheets data
        """

        for i, row in enumerate(self.rows):
            print("{0} {1}".format(str(i).ljust(6), row))
        return


    def read(self, workbook):

        sheet    = workbook.sheet_by_name(self.name)
        numrows  = sheet.nrows - 1
        numcells = sheet.ncols -1

        for i in range(numrows):
            rowvals = []

            for j in range(numcells):

                # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                cell_type  = sheet.cell_type(i, j)
                cell_value = sheet.cell_value(i, j)

                if cell_type == 1 or cell_type == 3:
                    cell_value = str(cell_value)
                elif cell_type == 2:
                    cell_value = float(cell_value)
                elif cell_type == 4:
                    cell_value = bool(cell_value)
                else:
                    cell_value = ""

                rowvals.append(cell_value)

            self.rows.append(rowvals)

        return self.rows


    def write(self, workbook):

        worksheet = workbook.add_sheet(self.name)
        for i, row in enumerate(self.rows):
            for j, col in enumerate(row):
                worksheet.write(i, j, col)

        return worksheet




if __name__ == "__main__":

    # some stuff
    testfile = "Reference/Matching_XL.xlsx"
    xls = xls_class()
    xls.read(testfile)

    # view a worksheet
    # xls.worksheets["CAD_SDS"].viewsheet()

    # view row 1 column 3
    print xls.worksheets["CAD_SDS"][1, 3]

    # view row 1, all columns
    print xls.worksheets["CAD_SDS"][1, :]

    # view rows 0-2, all columns
    print xls.worksheets["CAD_SDS"][0:2, :]

    # change row 0 col 0 to "poop"
    xls.worksheets["CAD_SDS"][0,0] = "poop"

    # write the excel file
    xls.write("Reference/Matching_XL2.xls")
