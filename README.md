# py-synflood

SYN flood denial-of-service (DoS) attack coded in Python

## Build

### Install virtualenv

`pip3 install virtualenv`

### Create virtual environment

`virtualenv env`

### Activate virtual environment

`source env/bin/activate`

### Install requirements

`pip3 install -r requirements.txt`

### Generate binary

`pyinstaller --onefile --paths=/env/Lib/site-packages py-synflood.py`

## Usage

`sudo py-synflood <ip_address> <port_numer> <max_threads> <payload> <sleep_interval>`

## Example

`py-synflood 1.2.3.4 80 1 OWNED 1`
