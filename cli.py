import time
import click
from database import init_db, set_alert, get_all_alerts
from core import check_market_prices

@click.group()
def main():
    """Enterprise Cryptographic Asset Alert & Scheduling Automator."""
    init_db()

@main.command()
@click.option("--ticker", required=True, help="Coin ID token string (e.g. bitcoin, ethereum).")
@click.option("--price", type=float, required=True, help="Target threshold price level in USD.")
@click.option("--direction", type=click.Choice(["above", "below"]), required=True, help="Trigger condition vector.")
def watch(ticker, price, direction):
    """Register or update an automated market alert rule matrix."""
    set_alert(ticker, price, direction)
    click.echo(click.style(f"🎯 Standardized tracking enabled: Watch {ticker.upper()} when {direction} ${price}", fg="green"))

@main.command()
def status():
    """List out actively registered watches configured within local data states."""
    records = get_all_alerts()
    if not records:
        click.echo("No configured targets found in state registries.")
        return
    click.echo("=== Currently Active Asset Monitors ===")
    for ticker, price, direction in records:
        click.echo(f" • {ticker.upper()}: Alert when price goes {direction} ${price}")

@main.command()
@click.option("--interval", type=int, default=60, help="Deamon evaluation heartbeat pause step in seconds.")
@click.option("--webhook", envvar="ALERT_WEBHOOK", help="Target Slack/Discord incoming webhook integration routing string.")
def monitor(interval, webhook):
    """Execute continuous system processing monitoring runtime loops."""
    click.echo(click.style(f"🚀 Initializing production listener agent daemon loop. Checking every {interval}s...", fg="cyan"))
    if not webhook:
        click.echo(click.style("⚠️ Warning: No notification routing provided. Triggers write directly to local stdout lines only.", fg="yellow"))
    
    try:
        while True:
            check_market_prices(webhook_url=webhook)
            time.sleep(interval)
    except KeyboardInterrupt:
        click.echo(click.style("\nStopping daemon process gracefully. Exiting safely...", fg="red"))
