import logging
import click

from app.browser import run_script
from app.coupon import main
from app.logger import Log


@click.command()
@click.option('--gui', '-g', is_flag=True, help='Enable the GUI')
def cli(gui):
    log = Log()
    log.basic_config(
        logfile_name='coupon',
        logfile_path='log',
        file_level=logging.INFO,
        console_level=logging.CRITICAL
    )
    log.get_logger()
    logging.debug('Setup loggers')
    if gui:
        logging.info('Running Graphical User Interface Application')
        main()
    else:
        logging.info('Running terminal script')
        click.echo('Publix Coupon Clipper: \n')
        username = click.prompt('Please enter your username')
        password = click.prompt('Please enter your password', hide_input=True)
        run_script(username, password)
