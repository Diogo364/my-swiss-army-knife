import click
import re
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def parse_operation(operation_str):
    """Parses operation string like '+ 15 wd' or '- 2 months'."""
    match = re.match(r"^([+-])\s*(\d+)\s*([\w-]+)$", operation_str.strip())
    if not match:
        raise ValueError("Invalid operation format. Expected '[operator] [amount] [unit]' (e.g., '+ 15 wd')")
    return match.groups()

def calculate(base_date: date, op: str, amount_str: str, unit: str) -> date:
    """Performs the date arithmetic."""
    amount = int(amount_str)
    if op == '-':
        amount = -amount
    
    unit = unit.lower()
    
    if unit in ['days', 'day']:
        return base_date + timedelta(days=amount)
    
    elif unit in ['wd', 'working-days']:
        current_date = base_date
        step = 1 if amount > 0 else -1
        remaining = abs(amount)
        while remaining > 0:
            current_date += timedelta(days=step)
            # weekday() returns 0 for Monday, 6 for Sunday
            if current_date.weekday() < 5:
                remaining -= 1
        return current_date
    
    elif unit in ['weeks', 'week']:
        return base_date + timedelta(weeks=amount)
    
    elif unit in ['months', 'month']:
        return base_date + relativedelta(months=amount)
    
    elif unit in ['years', 'year']:
        return base_date + relativedelta(years=amount)
    
    else:
        raise ValueError(f"Unknown unit: '{unit}'. Supported units: days, wd, working-days, weeks, months, years.")

@click.command(context_settings=dict(ignore_unknown_options=True, allow_interspersed_args=True))
@click.argument('date_or_op', required=False)
@click.argument('op', required=False)
@click.option('--verbose', '-v', is_flag=True, help="Include the day of the week in the output.")
def main(date_or_op, op, verbose):
    """
    Datetime Calculator CLI.

    \b
    Usage:
    dt-calc [DATE] OPERATION
    dt-calc OPERATION (uses today as base date)

    \b
    Arguments:
      DATE        Base date in YYYY-MM-DD format (defaults to today).
      OPERATION   Quoted string: "[operator] [amount] [unit]" (e.g., "+ 15 wd").

    \b
    Supported Units:
      day, days          Calendar days
      wd, working-days   Working days (Monday to Friday)
      week, weeks        Standard weeks
      month, months      Calendar months
      year, years        Calendar years

    \b
    Examples:
    dt-calc 2023-10-27 "+ 15 wd"
    dt-calc "+ 10 days"
    dt-calc 2023-10-27 "- 1 month"
    """
    if date_or_op is None:
        # Show help if no arguments provided
        with click.Context(main) as ctx:
            click.echo(ctx.get_help())
        return

    try:
        if op is None:
            # Only one argument provided: treat it as the operation
            base_date = date.today()
            operation_str = date_or_op
        else:
            # Two arguments provided: DATE and OPERATION
            try:
                base_date = datetime.strptime(date_or_op, "%Y-%m-%d").date()
                operation_str = op
            except ValueError:
                # If the first argument isn't a date, maybe it's part of the operation?
                # But with two arguments, we expect the first to be a date.
                raise click.BadParameter(f"Invalid date format: '{date_or_op}'. Expected YYYY-MM-DD.")

        parsed_op, amount, unit = parse_operation(operation_str)
        result_date = calculate(base_date, parsed_op, amount, unit)
        
        output = result_date.strftime("%Y-%m-%d")
        if verbose:
            output += f" ({result_date.strftime('%A')})"
        
        click.echo(output)

    except ValueError as e:
        click.secho(f"Error: {e}", fg="red", err=True)
        raise click.Abort()
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", fg="red", err=True)
        raise click.Abort()

if __name__ == "__main__":
    main()
