import pytest
from datetime import date
from datetime_calculator import parse_operation, calculate
from click.testing import CliRunner
from datetime_calculator import main

def test_parse_operation():
    assert parse_operation("+ 15 days") == ("+", "15", "days")
    assert parse_operation("- 2 months") == ("-", "2", "months")
    assert parse_operation("+10wd") == ("+", "10", "wd")
    
    with pytest.raises(ValueError, match="Invalid operation format"):
        parse_operation("invalid")

def test_calculate_days():
    base = date(2023, 10, 27)
    assert calculate(base, "+", "10", "days") == date(2023, 11, 6)
    assert calculate(base, "-", "10", "days") == date(2023, 10, 17)

def test_calculate_working_days():
    # 2023-10-27 is a Friday
    base = date(2023, 10, 27)
    # +1 working day should be Monday (2023-10-30)
    assert calculate(base, "+", "1", "wd") == date(2023, 10, 30)
    # +5 working days should be the next Friday (2023-11-03)
    assert calculate(base, "+", "5", "wd") == date(2023, 11, 3)
    # -1 working day should be Thursday (2023-10-26)
    assert calculate(base, "-", "1", "wd") == date(2023, 10, 26)

def test_calculate_months():
    # Jan 31st + 1 month -> Feb 28th
    base = date(2024, 1, 31) # 2024 is leap year
    assert calculate(base, "+", "1", "month") == date(2024, 2, 29)
    
    base2 = date(2023, 1, 31)
    assert calculate(base2, "+", "1", "month") == date(2023, 2, 28)

def test_cli_basic():
    runner = CliRunner()
    result = runner.invoke(main, ["2023-10-27", "+ 5 days"])
    assert result.exit_code == 0
    assert "2023-11-01" in result.output

def test_cli_verbose():
    runner = CliRunner()
    result = runner.invoke(main, ["2023-10-27", "+ 5 days", "--verbose"])
    assert result.exit_code == 0
    assert "2023-11-01 (Wednesday)" in result.output

def test_cli_default_today(mocker):
    from datetime import date
    # Patch 'date' where it's used in main.py
    mock_date = mocker.patch("datetime_calculator.date")
    mock_date.today.return_value = date(2023, 10, 27)
    # Ensure date(...) calls (like date.fromisoformat) would still work or 
    # if code does date(y, m, d). 
    # Actually, main.py uses date.today() and datetime.strptime(...).date()
    
    runner = CliRunner()
    result = runner.invoke(main, ["+ 1 day"])
    assert result.exit_code == 0
    assert "2023-10-28" in result.output

def test_calculate_weeks():
    assert calculate(date(2023, 10, 27), "+", "2", "weeks") == date(2023, 11, 10)

def test_calculate_years():
    base = date(2023, 10, 27)
    assert calculate(base, "+", "1", "year") == date(2024, 10, 27)
    # Leap year handling
    base_leap = date(2024, 2, 29)
    assert calculate(base_leap, "+", "1", "year") == date(2025, 2, 28)

def test_cli_dash_dash(mocker):
    from datetime import date
    mock_date = mocker.patch("datetime_calculator.date")
    mock_date.today.return_value = date(2023, 10, 27)

    runner = CliRunner()
    # Testing "--" as per spec: dt-calc -- "+ 10 days"
    result = runner.invoke(main, ["--", "+ 10 days"])
    assert result.exit_code == 0
    assert "2023-11-06" in result.output

def test_cli_subtraction_no_dash_dash():
    runner = CliRunner()
    # 2023-10-27 is a Friday. -1 working day should be Thursday (2023-10-26)
    result = runner.invoke(main, ["2023-10-27", "- 1 wd"])
    assert result.exit_code == 0
    assert "2023-10-26" in result.output

def test_cli_one_argument_as_op(mocker):
    from datetime import date
    mock_date = mocker.patch("datetime_calculator.date")
    mock_date.today.return_value = date(2023, 10, 27)
    
    runner = CliRunner()
    result = runner.invoke(main, ["+ 1 day"])
    assert result.exit_code == 0
    assert "2023-10-28" in result.output

def test_cli_invalid_date():
    runner = CliRunner()
    result = runner.invoke(main, ["not-a-date", "+ 5 days"])
    assert result.exit_code != 0
    assert "Invalid date format" in result.output
