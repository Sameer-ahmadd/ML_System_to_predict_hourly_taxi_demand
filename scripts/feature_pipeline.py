from argparse import ArgumentParser
from datetime import datetime, timedelta

import pandas as pd

from src import config
from src.data import (
    fetch_ride_events_from_data_warehouse,
    transform_raw_data_into_ts_data,
)
from src.feature_store_api import get_or_create_feature_group
from src.logger import get_logger

logger = get_logger()


def run(date: datetime):
    """_summary_

    Args:
        date (datetime): _description_

    Returns:
        _type_: _description_
    """
    logger.info('Fetching raw data from data warehouse')

    # fetch raw ride events from the datawarehouse for the last 28 days
    rides = fetch_ride_events_from_data_warehouse(
        from_date=(date - timedelta(days=28)), to_date=date
    )

    # transform raw data into time-series data by aggregating rides per
    # pickup location and hour
    logger.info('Transforming raw data into time-series data')
    ts_data = transform_raw_data_into_ts_data(rides)

    # add new column with the timestamp in Unix seconds
    logger.info('Adding column `pickup_ts` with Unix seconds...')
    ts_data['pickup_hour'] = pd.to_datetime(ts_data['pickup_hour'], utc=True)
    ts_data['pickup_ts'] = ts_data['pickup_hour'].astype(int) // 10**6

    # Debugging: Print schema of ts_data
    logger.info('Schema of ts_data:')
    logger.info(ts_data.dtypes)

    # Debugging: Convert pickup_location_id to int64 if necessary
    ts_data['pickup_location_id'] = ts_data['pickup_location_id'].astype('int64')
    logger.info('Schema of ts_data after conversion:')
    logger.info(ts_data.dtypes)

    # Debugging: Check for null values in pickup_location_id
    logger.info('Null values in pickup_location_id:')
    logger.info(ts_data['pickup_location_id'].isnull().sum())

    # get a pointer to the feature group we wanna write to
    logger.info('Getting pointer to the feature group we wanna save data to')
    feature_group = get_or_create_feature_group(config.FEATURE_GROUP_METADATA)

    # Debugging: Test with a small subset of data
    small_data = ts_data.head(10)
    feature_group.insert(small_data, write_options={'wait_for_job': False})

    # start a job to insert the data into the feature group
    logger.info('Starting job to insert data into feature group...')
    feature_group.insert(ts_data, write_options={'wait_for_job': False})

    logger.info('Finished job to insert data into feature group')


if __name__ == '__main__':
    # parse command line arguments
    parser = ArgumentParser()
    parser.add_argument(
        '--datetime',
        type=lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S'),
        help='Datetime argument in the format of YYYY-MM-DD HH:MM:SS',
    )
    args = parser.parse_args()

    # if args.datetime was provided, use it as the current_date, otherwise
    # use the current datetime in UTC
    if args.datetime:
        current_date = pd.to_datetime(args.datetime)
    else:
        current_date = pd.to_datetime(datetime.utcnow()).floor('H')

    logger.info(f'Running feature pipeline for {current_date=}')
    run(current_date)