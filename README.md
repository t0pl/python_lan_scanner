# Fast network scanner
Accurate network discovery tool (IPs, hostnames, mac and mac vendors)

## Requirements

getmac
```
 pip install getmac
```

## Example

```
 main.py 1-25 -s 1
```

First specify a range, for eg : 1-25 (positional argument)
 -> meaning that it will scan from 10.10.50.1 to 10.10.50.24, for eg
 
### Optional arguments

There are two other (optional) arguments at the moment:
* -a, --all ; which scans from 10.10.1.x to 10.10.255.x, for eg
```
 main.py 1-25 -a
```
* -s, --subnetwork; which scans from 10.10.1.1 for eg
```
 main.py 1-25 -s 1
```
Or you can specify a range as well, like this:
```
 main.py 1-25 -s 1-50 #10.10.1.1/25 to 10.10.50.1/25
```
Or even like this:
```
 main.py 2-25 -s 1,20,50,33
 #10.10.1.2/25
 #10.10.20.2/25
 #and so on
```
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
## Warning

I only tested this on windows and it seems pretty simple actually to make it cross platform so I'll change it.
I've forgotten to create an argument for scanning only 1 ip, but what you can do now is, for eg:
```
 main.py 1-2 -s 1
# 10.10.1.1 only
```
