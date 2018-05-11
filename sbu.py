import pandas as pd
import os

CSV_PATH = os.path.join('.', 'TRACv1csv.csv')


# dataframe of csv file
def create_dataframe(filepath):
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

    df = pd.read_csv(filepath)
    df.columns = COLS_TO_USE
    df.set_index('serial', inplace=True)

    return df


class Sbu:
    def __init__(self, name, description_type):
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

    def populate_counts(self,dataframe):
        reg_pattern = r'^(%s)'% (self.description_type)
        df = dataframe.loc[dataframe['sbu'] == self.name, :]
        df = df.loc[df['description'].str.match(reg_pattern), :]

        for row in df.itertuples():
            self.increment_counts(row)

    def increment_counts(self, row):
        if getattr(row, 'approved') == 'Approved':
            self.approved += 1
        else:
            self.unapproved+= 1
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


def create_sbu_objects(description_type,filepath):
    df = create_dataframe(filepath)
    sbus = pd.unique(df['sbu'])

    sbu_objects_list=[]
    for sbu in sbus:
        sbu_objects_list.append(Sbu(sbu, description_type))

    for sbu_object in sbu_objects_list:
        sbu_object.populate_counts(df)

    return sbu_objects_list


def create_sbu_policy_objects(filepath):
    sbu_objects_list=create_sbu_objects('Policy',filepath)
    return sbu_objects_list


def create_sbu_procedure_objects(filepath):
    sbu_objects_list=create_sbu_objects('Procedure',filepath)
    return sbu_objects_list


def main():
    df=create_dataframe(CSV_PATH)
    sbus = pd.unique(df['sbu'])

    sbu_policy_objects_list=[]
    for sbu in sbus:
        sbu_policy_objects_list.append(Sbu(sbu,'Policy'))

    for sbu_object in sbu_policy_objects_list:
        sbu_object.populate_counts(df)

    for obj in sbu_policy_objects_list:
        print(obj.name)
        print(obj.description_type)
        print(obj.approved)
        print(obj.unapproved)
        print()


if __name__ == '__main__':
    main()
