import click
import json

import web
from discovery import discovery
from websocket_smuggling import websocket_smuggling_var1
from websocket_smuggling import websocket_smuggling_var2

def run_discovery(input_data, output):
    """
    Runs the discovery function and prints the output in the specified format.
    """
    websocket_urls = discovery(input_data)

    if not websocket_urls:
        click.echo("No WebSocket connections found.")
        return

    if output == 'json':
        # Print the result as JSON
        click.echo(json.dumps(websocket_urls, indent=4))
    else:
        # Print the result as plain text
        click.echo("WebSocket connections discovered:")
        click.echo("==============================")
        for url in websocket_urls:
            click.echo(f"- {url}")
        click.echo("\nTotal WebSocket connections found: " + str(len(websocket_urls)))


@click.command()
@click.argument('input_data', type=str)
@click.option('--output', type=click.Choice(['json', 'text']), default='json', help='Output format for messages.')
def discovery_cmd(input_data, output):
    """
    Discover WebSocket connections.

    INPUT_DATA can be a single URL or a path to a file containing multiple URLs.

    This tool will crawl the provided URL(s) and detect if any of the pages or
    JavaScript files create WebSocket connections.
    """
    run_discovery(input_data, output)


def run_websocket_smuggling_upgrade(external_url,internal_url):
    websocket_smuggling_var1(external_url, internal_url)

def run_websocket_smuggling_status(external_url, internal_url, malicoius_site,parameter_name):
    websocket_smuggling_var2(external_url, internal_url,malicoius_site,parameter_name)


@click.command()
@click.argument('external_url', type=str)
@click.argument('internal_url', type=str)
@click.option('--flag', type=click.Choice(['only-upgrade-check', 'status-check']), prompt='vulnerability to check see report for further instructions')
@click.option('--malicious-site', type=str, help='Malicius site url addres to send request from internal network')
@click.option('--parameter_name', type=str, help='Parameter name for POST request')
def websocket_smuggling_cmd(external_url, internal_url,flag,malicious_site,parameter_name):
    """
    Checks for reverse-proxy websocket smuggling vulnerablility.

    EXTERNAL_URL is an external url address of websocket API

    INTERNAL_URL is internal url address of REST API

    This tool will check if websocket smuggling vulnerability is possible.
    """
    if flag == 'only-upgrade-check':
        run_websocket_smuggling_upgrade(external_url, internal_url)
    elif flag == 'status-check':
        run_websocket_smuggling_status(external_url, internal_url, malicious_site,parameter_name)
    else:
        click.echo('Invalid choice. Please choose either option1 or option2.')


@click.command()
@click.option('--payload', type=str, default='payload.json', help='Path to payload.')
@click.option('--url', type=str)
@click.option('--port', type=int, default=8000)
@click.option('--path', type=str, default='')
def create_csrf(payload, url, port, path):
    with open(payload, 'r') as file:
        payload = file.read()
        web.create(payload, url, port, path)


@click.command()
def run_server():
    web.run()


@click.group()
def cli():
    """Tool for discovering WebSocket connections."""
    pass


# Add the discovery command to the CLI group
cli.add_command(discovery_cmd, name='discovery')
cli.add_command(websocket_smuggling_cmd, name='websocket-smuggling')
cli.add_command(create_csrf, name='create_web')
cli.add_command(run_server, name='run_server')

if __name__ == "__main__":
    cli()
