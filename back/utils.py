from io import StringIO

import numpy
import pandas as pd

ftdna_strs_order = [
    'Kit', 'DYS393', 'DYS390', 'DYS19', 'DYS391', 'DYS385', 'DYS426', 'DYS388', 'DYS439', 'DYS389I', 'DYS392',
    'DYS389II', 'DYS458', 'DYS459', 'DYS455', 'DYS454', 'DYS447', 'DYS437', 'DYS448', 'DYS449', 'DYS464', 'DYS460',
    'Y-GATA-H4', 'YCAII', 'DYS456', 'DYS607', 'DYS576', 'DYS570', 'CDY', 'DYS442', 'DYS438', 'DYS531', 'DYS578',
    'DYF395S1', 'DYS590', 'DYS537', 'DYS641', 'DYS472', 'DYF406S1', 'DYS511', 'DYS425', 'DYS413', 'DYS557', 'DYS594',
    'DYS436', 'DYS490', 'DYS534', 'DYS450', 'DYS444', 'DYS481', 'DYS520', 'DYS446', 'DYS617', 'DYS568', 'DYS487',
    'DYS572', 'DYS640', 'DYS492', 'DYS565', 'DYS710', 'DYS485', 'DYS632', 'DYS495', 'DYS540', 'DYS714', 'DYS716',
    'DYS717', 'DYS505', 'DYS556', 'DYS549', 'DYS589', 'DYS522', 'DYS494', 'DYS533', 'DYS636', 'DYS575', 'DYS638',
    'DYS462', 'DYS452', 'DYS445', 'Y-GATA-A10', 'DYS463', 'DYS441', 'Y-GGAAT-1B07', 'DYS525', 'DYS712', 'DYS593',
    'DYS650', 'DYS532', 'DYS715', 'DYS504', 'DYS513', 'DYS561', 'DYS552', 'DYS726', 'DYS635', 'DYS587', 'DYS643',
    'DYS497', 'DYS510', 'DYS434', 'DYS461', 'DYS435'
]
full_ftdna_strs_order = [
    'DYS393', 'DYS390', 'DYS19', 'DYS391', 'DYS385a', 'DYS385b', 'DYS426', 'DYS388', 'DYS439', 'DYS389I', 'DYS392',
    'DYS389II', 'DYS458', 'DYS459a', 'DYS459b', 'DYS455', 'DYS454', 'DYS447', 'DYS437', 'DYS448', 'DYS449', 'DYS464a',
    'DYS464b', 'DYS464c', 'DYS464d', 'DYS460', 'Y-GATA-H4', 'YCAIIa', 'YCAIIb', 'DYS456', 'DYS607', 'DYS576', 'DYS570',
    'CDYa', 'CDYb', 'DYS442', 'DYS438', 'DYS531', 'DYS578', 'DYF395S1a', 'DYF395S1b', 'DYS590', 'DYS537', 'DYS641',
    'DYS472', 'DYF406S1', 'DYS511', 'DYS425', 'DYS413a', 'DYS413b', 'DYS557', 'DYS594', 'DYS436', 'DYS490', 'DYS534',
    'DYS450', 'DYS444', 'DYS481', 'DYS520', 'DYS446', 'DYS617', 'DYS568', 'DYS487', 'DYS572', 'DYS640', 'DYS492',
    'DYS565', 'DYS710', 'DYS485', 'DYS632', 'DYS495', 'DYS540', 'DYS714', 'DYS716', 'DYS717', 'DYS505', 'DYS556',
    'DYS549', 'DYS589', 'DYS522', 'DYS494', 'DYS533', 'DYS636', 'DYS575', 'DYS638', 'DYS462', 'DYS452', 'DYS445',
    'Y-GATA-A10', 'DYS463', 'DYS441', 'Y-GGAAT-1B07', 'DYS525', 'DYS712', 'DYS593', 'DYS650', 'DYS532', 'DYS715',
    'DYS504', 'DYS513', 'DYS561', 'DYS552', 'DYS726', 'DYS635', 'DYS587', 'DYS643', 'DYS497', 'DYS510', 'DYS434',
    'DYS461', 'DYS435'
]

AVERAGE_MUTATION_RATE = 'amr'
YEARS_PER_GENERATION = 'ypg'
REMOVE_PALINDROMES = 'rp'
CORRECT_389 = 'corr389'
PROCESS_SAMPLES_WITH_NA = 'pswn'


def get_df(data):
    csv = data \
        .decode('utf-8') \
        .replace(' ', ',') \
        .replace('\t', ',')
    df = pd.read_csv(StringIO(csv), sep=',', header=None, names=ftdna_strs_order, index_col=0)
    return df


def get_solved_na_df_1(df):
    notna_columns_of_reference = df.columns[df.iloc[0].notna()].tolist()
    df = df[notna_columns_of_reference]
    return df


def get_solved_na_df_2(df, headers):
    if headers[PROCESS_SAMPLES_WITH_NA] == "True":
        reference_df = df.iloc[:1]
        samples_df = df.iloc[1:]
        samples_df = samples_df.mask(reference_df.iloc[0].notnull() & samples_df.isnull(), reference_df, axis=1)
        df = pd.concat([reference_df, samples_df])
    else:
        df = df.dropna(axis=0, how='any')
    return df


def get_solved_duplications_df(df):
    for column in df:
        if df[column].dtype == 'object':
            column_splitted = df[column].str.split('-')
            if column in ['DYS385', 'DYS459', 'YCAII', 'CDY', 'DYF395S1', 'DYS413']:
                df[column + 'a'] = column_splitted.str[0]
                df[column + 'b'] = column_splitted.str[-1]
                df = df.drop(columns=column, errors='ignore')
            elif column in ['DYS464']:
                df[column + 'a'] = column_splitted.str[0]
                df[column + 'b'] = column_splitted.str[1]
                df[column + 'c'] = column_splitted.str[-2]
                df[column + 'd'] = column_splitted.str[-1]
                df = df.drop(columns=column, errors='ignore')
            else:
                df[column] = column_splitted.str[-1]
    return df


def get_solved_composites_df(df, headers):
    if headers[CORRECT_389] == "True":
        if 'DYS389I' in df.columns \
                and 'DYS389II' in df.columns:
            df['DYS389II'] = df['DYS389II'] - df['DYS389I']
    return df


def get_solved_palindromes_df(df, headers):
    if headers[REMOVE_PALINDROMES] == "True":
        df = df.drop(
            columns=['DYS385a', 'DYS385b', 'DYS459a', 'DYS459b', 'YCAIIa', 'YCAIIb', 'CDYa', 'CDYb', 'DYF395S1a',
                     'DYF395S1b', 'DYS413a', 'DYS413b'],
            errors='ignore'
        )
        df = df.drop(
            columns=['DYS464a', 'DYS464b', 'DYS464c', 'DYS464d'],
            errors='ignore'
        )
    return df


def get_solved_deletions_df(df):
    reference_df = df.iloc[:1]
    samples_df = df.iloc[1:]
    samples_df = samples_df.mask((reference_df.iloc[0] != 0) & (samples_df == 0), reference_df + 1, axis=1)
    df = pd.concat([reference_df, samples_df])
    reference_row = df.iloc[0]
    reference_zero_columns = reference_row[reference_row == 0].index
    df.loc[:, reference_zero_columns] = (df.loc[:, reference_zero_columns] > 0).astype('int64')
    return df


def get_subtracted_df(df):
    subtracted_df = (df - df.values[0]).abs()
    df['Different markers'] = (subtracted_df != 0).sum(axis=1)
    df['Steps'] = subtracted_df.sum(axis=1)
    df = df.drop(columns=full_ftdna_strs_order, errors='ignore')
    return df


def get_tmrca_df(df, str_count, headers):
    df['lambda_obs'] = df['Steps'] / str_count
    df['lambda'] = df['lambda_obs'] * (1 + numpy.exp(df['lambda_obs'])) / 2
    amr = headers[AVERAGE_MUTATION_RATE]
    ypg = headers[YEARS_PER_GENERATION]
    df['TMRCA'] = round(df['lambda'] / 2 / float(amr) * float(ypg)).astype('int64')
    df = df.drop(columns=['lambda_obs', 'lambda'], errors='ignore')
    return df
