## SYN Flood tester
Test your applications reciliency against SYN flood attacks.
Please only use on services you own, and be aware there is a high probability that this tool will crash your service.

## Guide
```bash
./tester.py --help
Usage: tester.py [OPTIONS]

Options:
  --target-ip TEXT               The ipv4/ipv6 address of the device under
                                 test  [required]
  --target-port INTEGER          The TCP port to target
  --max-connections INTEGER      Max open TCP connections to device
  --interval INTEGER             Interval between new connections in ms
  --validation-method TEXT       validation method to validate the service
                                 still works (Options: HTTP_GET, HTTPS_GET,
                                 none)
  --validation-interval INTEGER  interval between validation checks
  --help                         Show this message and exit.
```


## Examples
```bash
./tester.py --target-ip 2001:db8:ae1:50::43
  0%|▎                                                                                       | 3/1000 [00:01<06:44,  2.46it/s]
  Application under test failed after creating 3 connections


./tester.py --target-ip 10.40.0.109 --target-port 5001 --interval 50 --max-connections 100
100%|███████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:10<00:00,  9.68it/s]
Application under test completed the test successfully, consider increasing max connections, or decreasing interval
```