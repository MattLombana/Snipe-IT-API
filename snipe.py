#! /usr/bin/env python3

import SnipeITApi
import pprint


snipeapi = None


def pp(s):
    pprinter = pprint.PrettyPrinter(indent=4)
    pprinter.pprint(s)


def main():
    global snipeapi

    server = 'https://develop.snipeitapp.com'
    token = 'CHANGEME'
    snipeapi = SnipeITApi.SnipeAPI(server, token)

    ready_to_deploy = 2
    vm_model = 24

    names = [
        'pc1',
        'pc2',
    ]
    for name in names:
        snipeapi.create_asset(ready_to_deploy, vm_model, name=name)



if __name__ == '__main__':
    main()
