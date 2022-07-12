import typer
import sys
from razorpay_transactions.properties import Mode
from razorpay_transactions.worker import Worker

app = typer.Typer()


@app.command()
def welcome():
    print("Welcome To Payment Reports. If you see this message, installation was successful")


@app.command()
def generate_reports(mode: Mode = typer.Option(..., case_sensitive=False),
                     columns_in_summary: str = typer.Option(...),
                     days_preceding: int = 1, polling_interval: int = 3600,
                     filters: str = None, input_json_path: str = None):
    worker = Worker(mode=mode, columns_in_summary=columns_in_summary.split(','), days_preceding=days_preceding,
                    polling_interval=polling_interval, filters=filters, input_json_path=input_json_path)
    worker()


def main():
    """
    Entry point to console scripts
    :return:
    """
    sys.exit(app())


main()
