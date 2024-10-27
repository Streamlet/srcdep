#!/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import config
import update


class CommandDispatcher(object):

    @staticmethod
    def update(args, dir, dep):
        return update.update_dep(args, dir, dep)


def process_package(args, current_dir, project_dir, root_dir, is_root, processed_deps):
    deps = config.load(os.path.join(current_dir, project_dir), not is_root)
    if deps is None:
        return True
    dest_dir = root_dir if args.flat else project_dir
    for dep in deps:
        print('Processing %s...' % os.path.join(project_dir, dep.PATH))
        dep.PROJECT_DIR = project_dir
        if not args.allow_version_conflict or args.flat:
            processed_dep = processed_deps[dep.name(
            )] if dep.name() in processed_deps else None
            if processed_dep is not None:
                if dep.version() != processed_dep.version():
                    print('Failed to process "%s[%s]". Version conflict with "%s[%s]"' % (
                        os.path.join(dep.PROJECT_DIR, dep.PATH), dep.version(),
                        os.path.join(processed_dep.PROJECT_DIR, processed_dep.PATH), processed_dep.version()))
                    return False
                elif args.flat:
                    continue
            processed_deps[dep.name()] = dep
        if not args.routin(args, os.path.join(current_dir, dest_dir), dep):
            return False
        if not process_package(args, current_dir, os.path.join(project_dir, dep.PATH), root_dir, False, processed_deps):
            return False
    return True


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
            help='force update dependency, that means deleting the dependency directory and rebuild it.'
        )
        update_parser.add_argument(
            '--flat',
            action='store_true',
            help='flattern dependencies.'
        )
        update_parser.add_argument(
            '--allow-version-conflict',
            action='store_true',
            help='allow different versions of a same dependency exists in project.'
        )
        update_parser.set_defaults(routin=CommandDispatcher.update)
        args = parser.parse_args()
    else:
        args = argparse.Namespace()
        args.routin = CommandDispatcher.update
        args.force = False
        args.flat = False
        args.allow_version_conflict = True
    if not process_package(args, os.getcwd(), '', '', True, {}):
        return -1
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
