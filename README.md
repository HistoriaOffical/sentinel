# Historia Sentinel

An all-powerful toolset for Historia.

[![Build Status](https://travis-ci.org/historia/sentinel.svg?branch=master)](https://travis-ci.org/historia/sentinel)

Sentinel is an autonomous agent for persisting, processing and automating Historia governance objects and tasks, and for expanded functions in the upcoming Historia releases.

Sentinel is implemented as a Python application that binds to a local version 16.1.0 historiad instance on each Historia Masternode.

This guide covers installing Sentinel onto an existing Masternode in Ubuntu 14.04 / 16.04.

## Installation

### 1. Install Prerequisites

Make sure Python version 2.7.x or above is installed:

    python --version

Update system packages and ensure virtualenv is installed:

    $ sudo apt-get update
    $ sudo apt-get -y install python-virtualenv

Make sure the local Historia daemon running is at least version 16.1 (160100)

    $ historia-cli getinfo | grep version

### 2. Install Sentinel

Clone the Sentinel repo and install Python dependencies.

    $ git clone https://github.com/HistoriaOffical/sentinel.git && cd sentinel
    $ virtualenv ./venv
    $ ./venv/bin/pip install -r requirements.txt

### 3. Set up Cron

Set up a crontab entry to call Sentinel every minute:

    $ crontab -e

In the crontab editor, add the lines below, replacing '/home/YOURUSERNAME/sentinel' to the path where you cloned sentinel to:

    * * * * * cd /home/YOURUSERNAME/sentinel && ./venv/bin/python bin/sentinel.py >/dev/null 2>&1

### 4. Test the Configuration

Test the config by running all tests from the sentinel folder you cloned into

    $ ./venv/bin/py.test ./test

With all tests passing and crontab setup, Sentinel will stay in sync with historiad and the installation is complete

## Configuration

An alternative (non-default) path to the `historia.conf` file can be specified in `sentinel.conf`:

    historia_conf=/path/to/historia.conf

## Troubleshooting

To view debug output, set the `SENTINEL_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py

## Contributing

Please follow the [HistoriaCore guidelines for contributing](https://github.com/HistoriaOffical/historia/blob/master/CONTRIBUTING.md).

Specifically:

* [Contributor Workflow](https://github.com/HistoriaOffical/historia/blob/master/CONTRIBUTING.md#contributor-workflow)

    To contribute a patch, the workflow is as follows:

    * Fork repository
    * Create topic branch
    * Commit patches

    In general commits should be atomic and diffs should be easy to read. For this reason do not mix any formatting fixes or code moves with actual code changes.

    Commit messages should be verbose by default, consisting of a short subject line (50 chars max), a blank line and detailed explanatory text as separate paragraph(s); unless the title alone is self-explanatory (like "Corrected typo in main.cpp") then a single title line is sufficient. Commit messages should be helpful to people reading your code in the future, so explain the reasoning for your decisions. Further explanation [here](http://chris.beams.io/posts/git-commit/).

### License

Released under the MIT license, under the same terms as HistoriaCore itself. See [LICENSE](LICENSE) for more info.
