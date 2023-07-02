#!/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import config
import update


class CommandDispatcher(object):

    @staticmethod
    def update(args, dir, deps):
        return update.update_deps(args, dir, deps)


def process_package(args, dir, optional):
    deps = config.load(dir, optional)
    if deps is not None:
        if not args.routin(args, dir, deps):
            return False
        for dep in deps:
            if not process_package(args, os.path.join(dir, dep.PATH), True):
                return False


def main():
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            prog='srcdep',
            description='A simple, source code based dependency management tool.',
            epilog='Powered by Streamlet Studio.')
        subparsers = parser.add_subparsers(
            help='commands for solving dependencies')
        update_parser = subparsers.add_parser(
            'update', help='update dependencies')
        update_parser.add_argument(
            '--force',
            '-f',
            action='store_true',
            help='force update dependency. will delete the dependency directory and rebuild it.'
        )
        update_parser.set_defaults(routin=CommandDispatcher.update)
        args = parser.parse_args()
    else:
        args = argparse.Namespace()
        args.routin = CommandDispatcher.update
        args.force = False
    if not process_package(args, os.getcwd(), False):
        return -1
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
