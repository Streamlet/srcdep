#!/bin/python
# -*- coding: utf-8 -*-


import os, argparse, config, update

class CommandDispatcher(object):
    @staticmethod
    def update(args, dir, deps):
        update.update_deps(args, dir, deps)

def process_package(args, dir, optional):
    deps = config.load(dir, optional)
    if deps is not None:
        args.routin(args, dir, deps)
        for dep in deps:
            process_package(args, os.path.join(dep.PATH), True)

def main():
    parser = argparse.ArgumentParser(
                    prog = 'srcdep',
                    description = 'A simple, source code based dependency management tool.',
                    epilog = 'Powered by Streamlet Studio.')
    subparsers = parser.add_subparsers(help='commands for solving dependencies')
    update_parser = subparsers.add_parser('update', help='update dependencies')
    update_parser.add_argument('--force', '-f', action='store_true', help='force update dependency. will delete the dependency directory and rebuild it.')
    update_parser.set_defaults(routin=CommandDispatcher.update)
    args = parser.parse_args()
    process_package(args, os.getcwd(), False)

if __name__ == '__main__':
    main()
