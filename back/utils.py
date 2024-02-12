from io import StringIO

import numpy
import pandas as pd

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
    'DYS461', 'DYS435']

AVERAGE_MUTATION_RATE = 'amr'
YEARS_PER_GENERATION = 'ypg'


def get_prepared_df(rq):
    data = rq.data
    data_decoded = data.decode()
    data_replaced = data_decoded.replace('-', ',')
    data_tab_separated = data_replaced.replace(' ', '\t')
    data_comma_separated = data_tab_separated.replace('\t', ',')
    df = pd.read_csv(StringIO(data_comma_separated), sep=',', header=None, names=full_ftdna_strs_order, index_col=0)
    df = df.dropna(axis=1, how='all')
    df.index.name = 'Kit'
    return df


def get_extended_df(df, headers):
    subtracted_df = (df - df.values[0]).abs()
    str_count = len(df.columns)
    df['Different markers'] = (subtracted_df != 0).sum(axis=1)
    df['Steps'] = subtracted_df.sum(axis=1)
    df = df.drop(columns=full_ftdna_strs_order, errors='ignore')
    df['lambda_obs'] = df['Steps'] / str_count
    df['lambda'] = df['lambda_obs'] * (1 + numpy.exp(df['lambda_obs'])) / 2
    amr = headers[AVERAGE_MUTATION_RATE]
    ypg = headers[YEARS_PER_GENERATION]
    df['TMRCA'] = round(df['lambda'] / 2 / float(amr) * int(ypg)).astype(int)
    df = df.drop(columns=['lambda_obs', 'lambda'], errors='ignore')
    df = df.drop(df.index[0])
    return df
