import pandas as pd
from sbu import CSV_PATH
from sbu import create_dataframe

DESCRIPTION_MAPPER = {
    'policy': r'^(Policy)',
    'procedure': r'^(Procedure)'
}

SBU_MAPPER = {
    'retail': 'Retail',
    'corporate': 'Corporate',
    'treasury': 'Treasury',
    'financial': 'Financial',
    'operations': 'Operations',
    'human resources': 'Human resources',
    'investments': 'Investments',
    'rmc': 'RMC',
    'accounts': 'Accounts',
    'infotech': 'Infotech'
}

COUNTER_MAPPER = {
    'approved': {
        'column': 'approved',
        'value': 'Approved'
    },
    'unapproved': {
        'column': 'unapproved',
        'value': 'Unapproved'
    },
    'expired_yes': {
        'column': 'expired',
        'value': 'Yes'
    },
    'expired_no': {
        'column': 'expired',
        'value': 'No'
    },
    'reg_yes': {
        'column': 'regulatory',
        'value': 'Yes'
    },
    'reg_no': {
        'column': 'regulatory',
        'value': 'No'
    },
    'freq_daily': {
        'column': 'reviewFrequency',
        'value': 'Daily'
    },
    'freq_weekly': {
        'column': 'reviewFrequency',
        'value': 'Weekly'
    },
    'freq_monthly': {
        'column': 'reviewFrequency',
        'value': 'Monthly'
    },
    'freq_annually': {
        'column': 'reviewFrequency',
        'value': 'Annually'
    }
}


class TracEntry:
    def __init__(self, serial, description, sbu, scope,
                 reviewFequency, lastReviewDate, nextReviewDate,
                 days, expired, regulatory, approved, responsibility, note):
        self.serial = serial
        self.description = description
        self.sbu = sbu
        self.scope = scope
        self.reviewFrequency = reviewFequency
        self.lastReviewDate = lastReviewDate
        self.nextReviewDate = nextReviewDate
        self.days = days
        self.expired = expired
        self.regulatory = regulatory
        self.approved = approved
        self.responsibility = responsibility
        self.note = note


def create_trac_entry_objects(dataframe):
    trac_entries = []

    for row in dataframe.itertuples():
        serial = getattr(row, 'Index') #serial is called for some reason
        description = getattr(row, 'description')
        sbu = getattr(row, 'sbu')
        scope = getattr(row, 'scope')
        reviewFrequency = getattr(row, 'reviewFrequency')
        lastReviewDate = getattr(row, 'lastReviewDate')
        nextReviewDate = getattr(row, 'nextReviewDate')
        days = getattr(row, 'days')
        expired = getattr(row, 'expired')
        regulatory = getattr(row, 'regulatory')
        approved = getattr(row, 'approved')
        responsibility = getattr(row, 'responsibility')
        note = getattr(row, 'note')

        trac_entry = TracEntry(serial, description, sbu, scope, reviewFrequency,
                               lastReviewDate, nextReviewDate, days, expired,
                               regulatory, approved, responsibility, note)
        trac_entries.append(trac_entry)

    return trac_entries


def create_trac_entry_dataframe(dataframe, description, sbu, counter):
    description_reg_pattern = DESCRIPTION_MAPPER[description]
    sbu = SBU_MAPPER[sbu]
    counter = COUNTER_MAPPER[counter]

    dataframe = dataframe.loc[dataframe['sbu'] == sbu, :]
    dataframe = dataframe.loc[dataframe['description'].str.match(description_reg_pattern), :]
    dataframe = dataframe.loc[dataframe[counter['column']] == counter['value'], :]

    return dataframe


def main():
    df = create_dataframe(CSV_PATH)
    df = create_trac_entry_dataframe(df, 'policy', 'operations', 'expired_no')

    trac_entries=create_trac_entry_objects(df)

    for entry in trac_entries:
        print(entry.note)


if __name__ == '__main__':
    main()
