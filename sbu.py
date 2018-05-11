import pandas as pd
import os


CSV_PATH = os.path.join('.', 'TRACv1csv.csv')


class Sbu:
    def __init__(self, name, description_type):
        '''
        name is a sbu string
        description_type is a string assigned Policy or Procedure
        '''

        self.name = name
        self.description_type = description_type
        self.approved = 0
        self.unapproved = 0
        self.expired_yes = 0
        self.expired_no = 0
        self.reg_yes = 0
        self.reg_no = 0
        self.freq_daily = 0
        self.freq_weekly = 0
        self.freq_monthly = 0
        self.freq_annually = 0

    def populate_counts(self, dataframe):
        '''
        dataframe is a panadas dataframe of the data
        populate_counts populates the instance counters from the dataframe
        '''

        reg_pattern = r'^(%s)' % (self.description_type)
        filtered_dataframe = dataframe.loc[dataframe['sbu'] == self.name, :]
        filtered_dataframe = filtered_dataframe.loc[filtered_dataframe['description'].str.match(reg_pattern), :]

        for row in filtered_dataframe.itertuples():
            self.increment_counts(row)

    def increment_counts(self, row):
        '''
        row is a row from a pandas dataframe
        incrment_counts increments the appropriate instance counter by analyzing the row data
        '''

        if getattr(row, 'approved') == 'Approved':
            self.approved += 1
        else:
            self.unapproved += 1
        if getattr(row, 'expired') == 'Yes':
            self.expired_yes += 1
        else:
            self.expired_no += 1
        if getattr(row, 'regulatory') == 'Yes':
            self.reg_yes += 1
        else:
            self.reg_no += 1
        if getattr(row, 'reviewFrequency') == 'Daily':
            self.freq_daily += 1
        elif getattr(row, 'reviewFrequency') == 'Weekly':
            self.freq_weekly += 1
        elif getattr(row, 'reviewFrequency') == 'Monthly':
            self.freq_monthly += 1
        else:
            self.freq_annually += 1


def create_dataframe(filepath):
    '''
    filepath is the location of the csv file
    create_dataframe returns a pandas dataframe of the csv file
    '''

    COLS_TO_USE = ['serial',
                   'description',
                   'sbu',
                   'scope',
                   'reviewFrequency',
                   'lastReviewDate',
                   'nextReviewDate',
                   'days',
                   'expired',
                   'regulatory',
                   'approved',
                   'responsibility',
                   'note']

    dataframe = pd.read_csv(filepath)
    dataframe.columns = COLS_TO_USE
    dataframe.set_index('serial', inplace=True)

    return dataframe


def create_sbu_objects(description_type, filepath):
    '''
    description_type is a string containing either Policy or Procedure
    filepath is the location of the csv file
    returns a list of Sbu objects with their counts populated
    '''

    dataframe = create_dataframe(filepath)
    sbus = pd.unique(dataframe['sbu'])

    sbu_objects_list = []
    for sbu in sbus:
        sbu_objects_list.append(Sbu(sbu, description_type))

    for sbu_object in sbu_objects_list:
        sbu_object.populate_counts(dataframe)

    return sbu_objects_list


def create_sbu_policy_objects(filepath):
    '''
    filepath is the location of the csv file
    returns a list of Sbu objects which are of description_type=Policy with their
    counts populated
    '''

    sbu_objects_list = create_sbu_objects(description_type='Policy', filepath=filepath)
    return sbu_objects_list


def create_sbu_procedure_objects(filepath):
    '''
    filepath is the location of the csv file
    returns a list of Sbu objects which are of description_type=Procedure with their
    counts populated
    '''

    sbu_objects_list = create_sbu_objects(description_type='Procedure', filepath=filepath)
    return sbu_objects_list


def main():
    dataframe = create_dataframe(CSV_PATH)
    sbus = pd.unique(dataframe['sbu'])

    sbu_policy_objects_list = []
    for sbu in sbus:
        sbu_policy_objects_list.append(Sbu(sbu, 'Policy'))

    for sbu_object in sbu_policy_objects_list:
        sbu_object.populate_counts(dataframe)

    for obj in sbu_policy_objects_list:
        print(obj.name)
        print(obj.description_type)
        print(obj.approved)
        print(obj.unapproved)
        print()


if __name__ == '__main__':
    main()
