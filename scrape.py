import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

class WikiTable():
    """
    Creates a pandas dataframe with data read from a wikipedia table
    """
    def __init__(self, url=None, table_class=None, columns=None, cell_details=None, show_logs=False, header_offset=False):
        # self.url = url
        self.table_class = table_class
        self.show_logs = show_logs
        self.header_offset=header_offset
        
        # checks on init - could expand this
        if type(columns)!=list:        
            raise Exception('Type Error: columns must be a list')

        self.columns = columns

        if cell_details:
            if type(cell_details['attributes'])!=list:
                raise Exception('Type Error: attrs must be a list')

            self.attributes = cell_details['attributes']
            self.elements = cell_details['elements']

        # make some soup
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')
        
        # get table and set the colidx
        self.table = self.get_table()
        self.colidx = self.get_colidx()

        if self.show_logs:
            print('Col indicies: ', self.colidx)

        # initiate the rowspan info to create the offset matrix
        self.osm = self.process_spans().astype(int)

        # run the get_table info
        if cell_details:
            self.df = self.get_tableinfo()
        else:
            self.df = self.get_simple()

    def get_table(self):
        '''
        Gets the table out of the soup
        '''
        # get the table
        return self.soup.find('table', {'class':self.table_class})
    
    # this function gets the indecies of the headers to read the rows
    def get_colidx(self):
        '''
        Gets the indicies fo the columns to read the rows
        '''
        # get the table headers and match the col names
        table_headers = self.table.findAll('th')
        table_headers = [str(th.contents[0]).strip() for th in table_headers]

        # get the indicies of the column headers
        return [table_headers.index(col) for col in self.columns]

    def process_spans(self):
        '''
        Manages the row spans in the table by creating a matrix:
        - offset: to manage the offsets created by the rowspans impacting each column
        - rowspan: to keep track of the rows remaining
        - colspan: likewise incorporate the column spans too
        '''
        
        # get all of the table body rows
        rows = self.table.findAll('tr')
        num_rows = len(rows)
        # print('\nTable has {} rows:'.format(num_rows))
        # print('Looking for rowspans:')
        
        # first go through each row to get the max number of cells
        max_cols = 0
        # print('  - creating rowspan and offset matricies with {} rows'.format(num_rows))
        # print('  - getting max row length')
        for row in rows:
            num_cells = len(row.findAll('td'))
            # print(num_cells, end=', ')
            if num_cells > max_cols:
                max_cols = num_cells

        # print('  - matrix size ({}, {})\n'.format(num_rows-1, max_cols))
        
        # rowspan, colspan and offset matricies
        rsm = np.ones((num_rows, max_cols))
        csm = np.ones((num_rows, max_cols))
        osm = np.zeros((num_rows, max_cols))
        # rosm = np.zeros((num_cells, max_cols))

        # go through each row and cell and find the rowspans and colspans
        # print('  - finding rowspans & colspans ... ')
        row_idx = 0
        for row in rows:
            cells = row.findAll('td')
            
            # check if we're in the headers
            if len(cells) == 0:
                cells = row.findAll('th')

            cell_idx = 0
            for cell in cells:
                # row spans
                if 'rowspan' in cell.attrs:
                    rs = int(cell.attrs['rowspan'])
                    if rs > 1:
                        rsm[row_idx, cell_idx] = rs
                        # print('    - rowspan of {} in pos({}, {})'.format(rs, row_idx, cell_idx))                
                # col spans
                if 'colspan' in cell.attrs:
                    cs = int(cell.attrs['colspan'])
                    if cs > 1:
                        csm[row_idx, cell_idx] = cs
                        # print('    - colspan of {} in pos({}, {})'.format(cs, row_idx, cell_idx))
                cell_idx += 1
            row_idx += 1

        # print('\n', rsm)

        # now we need to adjust the rowspan and colspan positions based on the preceding rowspans and colspans
        # scan through the rowspan matrix and shift the cells effected by each rowspan accross one column
        # print('\n  - adjusting rowspans and colspans by preceding spans')
        n, m = rsm.shape
        for i in range(n-1):
            for j in range(m-1):
                rs = int(rsm[i, j])
                cs = int(csm[i, j])
                
                # adjust any colspans in this row
                rsm[i, j+cs:] = rsm[i, j+1:max_cols-cs+1]
                csm[i, j+cs:] = csm[i, j+1:max_cols-cs+1]

                # adjust any rowspans in this column - !!! THIS IS WRONG !!!
                rsm[i+1:i+rs, j+cs:] = rsm[i+1:i+rs, j:-cs]
                csm[i+1:i+rs, j+cs:] = csm[i+1:i+rs, j:-cs]

        if self.show_logs:
            print('Rowspan matrix')
            print('\n', rsm, '\n')
            print('Colspan matrix')
            print('\n', csm, '\n')

        # now we can create the offset matrix
        # print('  - creating offset matrix')
        for i in range(n-1):
            for j in range(m-1):
                rs = int(rsm[i, j])
                cs = int(csm[i, j])
                if cs > 1:
                    # add an offset to the proceding columns
                    osm[i, j+cs-1:] += cs-1
                if rs > 1:
                    # add an offset to the proceding rows and columns
                    osm[i+1:i+rs, j+cs:] += cs
                
        if self.show_logs:# print('\n',rsm)
            print('\n',osm, '\n')
        
        return osm

    # this function gets the table information
    def get_tableinfo(self):
        '''
        takes a soup element, which is the html of a website
        takes the table class and columns that we want to the info from
        also needs the attribute type
        '''        
        # go through the rows and get the values from the desired table
        all_data = []
        table_rows = self.table.findAll('tr')
        row_idx = 1            
        for row in table_rows[1:]:
            # get the cells 
            record = []
            for idx, att, et in zip(self.colidx, self.attributes, self.elements):       
                # get the cell adjusted by the offset
                cell = row.find_all('td')[idx - self.osm[row_idx, idx]]

                # test if there is anything in the element
                to_test = str(cell.contents[0]).strip()
                
                # check if the cell has any content and make a record if it does
                if len(to_test) > 0:
                    record.append(cell.find(et).attrs[att])
                else:
                    record.append(np.nan)
                    
            # append the row
            all_data.append(record)

            row_idx += 1
            
        # return as a dataframe
        return pd.DataFrame(data=all_data, columns=self.columns)

    def get_simple(self):
        '''
        takes a soup element, which is the html of a website
        takes the table class and columns that we want to the info from
        also needs the attribute type
        '''
        # go through the rows and get the values from the desired table
        all_data = []
        table_rows = self.table.findAll('tr')
        row_idx = 1

        # print ('\nChecking rows:')

        for row in table_rows[1:]:
            record = []
            # check if there's stuff in the rows
            cells = row.find_all('td')

            # if self.show_logs:
            #     print("   - row {} has {} cells".format(row_idx, len(cells)))
            
            # skip the empty rows
            if len(cells) == 0:
                row_idx += 1
                continue
            for idx in self.colidx:                
                # we might need to offset the header index
                # assumes the header is in the first row
                if self.header_offset:
                    idx += self.osm[0, idx]

                # don't try to index stuff the doesn't exist
                adj_idx = idx - self.osm[row_idx, idx]                

                try:
                    cell = cells[adj_idx]
                except Exception:
                    print("GetSimpleError: [row {} has {} cells | we're trying to index {}]\n".format(
                        row_idx, len(cells), adj_idx))                
                
                # if not cell.attrs.get('style'):
                record.append(cell.text)
                # else:
                #     record.append(cell.)
                                   
            # append the row
            # if self.show_logs:
            #     print(record)

            all_data.append(record)

            row_idx += 1
            
        # return as a dataframe

        # print

        return pd.DataFrame(data=all_data, columns=self.columns)
        
