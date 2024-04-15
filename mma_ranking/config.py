from datetime import date, datetime

IF_SCRAPE_ALL: bool = False
BEGIN_DATE: date = datetime.strptime("1990-01-01", "%Y-%m-%d").date()

N_YEARS: int = 5  # number of years to generate the fighter performance ratio
