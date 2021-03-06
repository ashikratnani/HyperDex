#!/usr/bin/env python

# Copyright (c) 2012, Cornell University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of HyperDex nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import socket
import sys

import argparse
import pyparsing

import hypercoordinator.parser


def send_text(host, port, text):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    s.connect((host, port))
    s.sendall(text)
    data = s.recv(4096)
    if data.endswith('.\n'):
        data = data[:-2]
    if data != 'SUCCESS\n':
        sys.stdout.write(data)
        return 1
    return 0


def add_space(args):
    data = sys.stdin.read()
    try:
        parser = (hypercoordinator.parser.space + pyparsing.stringEnd)
        space = parser.parseString(data)[0]
    except ValueError as e:
        print str(e)
        return 1
    except pyparsing.ParseException as e:
        print str(e)
        return 1
    text = 'add space\n{0}\n.\n'.format(data)
    return send_text(args.host, args.port, text)


def del_space(args):
    return send_text(args.host, args.port, 'del space {0}\n'.format(args.space))


def validate_space(args):
    data = sys.stdin.read()
    try:
        parser = (hypercoordinator.parser.space + pyparsing.stringEnd)
        space = parser.parseString(data)[0]
    except ValueError as e:
        print str(e)
        return 1
    except pyparsing.ParseException as e:
        print str(e)
        return 1
    return 0


def main(args, name='hyperdex-control'):
    parser = argparse.ArgumentParser(prog=name)
    parser.add_argument('--host', metavar='COORDHOST',
                        help='Address of the coordiantor',
                        default='127.0.0.1')
    parser.add_argument('--port', metavar='COORDPORT', type=int,
                        help='Port for coordinator control connections',
                        default=6970)
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_add_space = subparsers.add_parser('add-space', help='add-space help')
    parser_add_space.set_defaults(func=add_space)
    parser_del_space = subparsers.add_parser('del-space', help='del-space help')
    parser_del_space.add_argument('space', metavar='SPACE', help='the space to delete')
    parser_del_space.set_defaults(func=del_space)
    parser_validate_space = subparsers.add_parser('validate-space', help='validate help')
    parser_validate_space.set_defaults(func=validate_space)
    args = parser.parse_args(args)
    return args.func(args)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
