#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
from .quark import Quark
import argparse
import os
import sys
if sys.version_info.major > 2:
    import configparser
else:
    import ConfigParser as configparser


# Kind of sort of like a factory thing
def invoke_task(instance,options,args):
    if len(args) == 0:
        instance.invoke_task(options.task,options.file)
    else:
        instance.invoke_task(options.task,options.file, *options.args)

def main():
    #print(sys.argv)

    parser = argparse.ArgumentParser(description='Quark: Because Leptons did not sound cool',
                                     prog='quark')
    # NOTE: env and profile need to be swapped
    parser.add_argument('--env', dest='env', type=str,
                        help='which environment you want to deploy to',
                        default='local')
    parser.add_argument('--profile', dest='profile', type=str,
                        help='which runtime profile from config to use',
                        default='staging')
    # I will revist this once the project grows - for now stick with stdlib
    # ConfigObj might be a better long term choice here
    parser.add_argument("--profiles-file", dest="profiles_file", default=os.path.join(os.getcwd(), "deployment_profiles.cfg"))
    parser.add_argument("--dependencies-dir", dest="deps_dir", default=os.path.join(os.getcwd(), ""))
    parser.add_argument("--task", dest="task", type=str, help="what would you like to do?")
    parser.add_argument("--spark", type=str, dest="spark_version", default="1.6.0")
    #parser.add_argument("--type", dest="type", type=str, help="type of asset being deployed")
    parser.add_argument("file", type=str, help="file to deploy", nargs='?')
    parser.add_argument("args", type=str, nargs="*")
    options = parser.parse_args()
    config = configparser.SafeConfigParser(os.environ)
    config.read(options.profiles_file)
    #with open(options.profiles_file) as f:
    #    print(f.read())
    #print(config.sections())
    deployment_environment = config.get(options.env, "deployment_environment")
    if options.task == "lsprofiles":
        for section in config.sections():
            print(section)
        sys.exit(0)
    if deployment_environment == "qubole":
        print("Qubole deployment detected", file=sys.stderr)
        from .qubole import Qubole
        qubole = Qubole(config, options)
        invoke_task(qubole, options, options.args)
    else:
        quark = Quark(config, options)
        print(options.args)
        invoke_task(quark, options, options.args)