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

@click.command()
@click.argument('args', nargs=-1)
@click.option('--verbose', '-v', is_flag=True, help="Include the day of the week in the output.")
def main(args, verbose):
    """
    Datetime Calculator CLI.
    
    Examples:
    \b
    dt-calc 2023-10-27 "+ 15 wd"
    dt-calc -- "+ 10 days"
    """
    if not args:
        # Show help if no arguments provided
        with click.Context(main) as ctx:
            click.echo(ctx.get_help())
        return

    try:
        if len(args) == 1:
            base_date = date.today()
            operation_str = args[0]
        elif len(args) >= 2:
            try:
                base_date = datetime.strptime(args[0], "%Y-%m-%d").date()
                operation_str = args[1]
            except ValueError:
                # If the first argument isn't a date, maybe it's just the operation 
                # and we should use today's date? 
                # But spec says [DATE] [OPERATION]. 
                # Let's try to be helpful if they just passed the operation.
                # However, if args[0] is like "+", it definitely isn't a date.
                if re.match(r"^[+-]", args[0]):
                    base_date = date.today()
                    operation_str = " ".join(args)
                else:
                    raise click.BadParameter(f"Invalid date format: '{args[0]}'. Expected YYYY-MM-DD.")
        else:
            raise click.UsageError("Operation is required.")

        op, amount, unit = parse_operation(operation_str)
        result_date = calculate(base_date, op, amount, unit)
        
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
