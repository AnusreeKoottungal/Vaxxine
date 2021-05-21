from datetime import datetime
import logging
import pytz

logging.basicConfig(filename="process.log", level=logging.INFO, filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def print_with_date(stmt):
    print(stmt)
    logging.info(stmt)

