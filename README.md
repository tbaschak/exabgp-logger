# exabgp-logger
logging BGP activity as JSON to couchdb using exabgp

This is the Open Source repository for a tool written as part of a [talk](http://bsideswpg.ca/speakers/#theo-baschak) for [BSidesWpg](http://bsideswpg.ca).

## Requirements

This tool uses exabgp in the backend to BGP peer with multiple AS numbers. I am using 1 exabgp process per peer, per protocol (so v4 and v6 would be 2 processes). 

`pip install exabgp`

If you've never run exabgp it will ask you to run the following, you may need to prepend the command with `sudo`.

`exabgp --fi > /usr/local/etc/exabgp/exabgp.env`

## Usage

In the `exabgp` directory are sample v4 and v6 configuration files, as well as bash scripts to start daemonized exabgp processes for each. Exabgp will then call `bin/routes.sh` and log each BGP update to a local couchdb server. `routes.sh` can be copied/modified to log to a per-peer database insead of a common one, and then couchdb replication used to combine all updates into one common database, keeping the original per-peer updates still separate.

