import json
import subprocess
from ipaddress import IPv4Address, IPv6Address, ip_address
from pathlib import Path

from tokens import _helper

#
# General utils
#


def format_json(text: str | bytes | bytearray) -> str:
    """A convenience function that combines json.loads() and json.dumps()
    to pretty-print json.
    """
    contents = json.loads(text)
    pretty_contents = json.dumps(contents, indent=2)
    return pretty_contents


def api_token(name: str | Path) -> str:
    """When given a name 'example', searches the ./tokens/ directory for
    a matching file or 'example.txt' and returns the contents, stripping
    out comments and whitespaces.
    """
    token = _helper.get_token(name)
    return token


#
# Get our public IP address using OpenDNS
#


def ask_opendns_my_ip_str() -> str:
    call_dig = subprocess.Popen(
        "dig +short myip.opendns.com @resolver1.opendns.com",
        shell=True,
        stdout=subprocess.PIPE,
    )
    # There's a lot chained together in the next line, but all
    # it does is references the stdout captured from the subprocess,
    # looks at the stdout contents, and converts the contents from
    # byte values to Unicode text.
    dig_response = call_dig.stdout.read().decode()
    # The stdout contents probably included a newline value ("\n" or something),
    # so we should strip that out. Our IP is 192.0.2.1, not 192.0.2.1\n.
    my_ip = dig_response.strip()
    return my_ip


def ask_opendns_my_ip() -> IPv6Address | IPv4Address:
    my_ip = ask_opendns_my_ip_str()
    my_ip = ip_address(my_ip)  # convert to an IP address object
    return my_ip
