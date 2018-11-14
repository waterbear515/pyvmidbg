#!/usr/bin/env python3

"""LibVMI-based GDB server.

Usage:
  vmidbg.py [options] <port> <vm_name> <process>
  vmidbg.py (-h | --help)

Options:
  -a ADDR, --address=<ADDR>     Server address to listen on [default: 127.0.0.1]
  -h --help                     Show this screen.
  --version                     Show version.

"""

import logging
from docopt import docopt

from .gdbserver import GDBServer
from .libvmistub import LibVMIStub
from .debugcontext import DebugContext


def main():
    args = docopt(__doc__)
    address = args['--address']
    port = int(args['<port>'])
    vm_name = args['<vm_name>']
    process = args['<process>']

    logging.basicConfig(level=logging.DEBUG)

    with DebugContext(vm_name) as ctx:
        ctx.attach(process)
        with GDBServer(address, port, stub_cls=LibVMIStub, stub_args=(ctx,)) as server:
            server.listen()

if __name__ == "__main__":
    main()
