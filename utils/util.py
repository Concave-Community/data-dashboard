'''
Precprocessing utility functions

'''

def select_columns(data_frame, column_names):
    new_frame = data_frame.loc[:, column_names]
    return new_frame