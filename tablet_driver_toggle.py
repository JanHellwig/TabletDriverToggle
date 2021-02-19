#!/usr/bin/env python3

import os
import pywintypes
import win32service
import win32serviceutil


def disable_service(service_name: str) -> None:
    win32serviceutil.StopService(service_name)


def enable_service(service_name: str) -> None:
    win32serviceutil.StartService(service_name)


def is_service_running(service_name: str) -> bool:
    status = win32serviceutil.QueryServiceStatus(service_name)
    return status[1] == win32service.SERVICE_RUNNING


def main():
    if os.name != 'nt':
        raise RuntimeError('This tool only works on Windows')

    wacom_service = 'Wacom Professional Service'

    wacom_running = is_service_running(wacom_service)
    if wacom_running:
        print('Disabling Wacom driver...')
        disable_service(wacom_service)
    else:
        print('Enabling Wacom driver...')
        enable_service(wacom_service)


if __name__ == '__main__':
    try:
        main()
    except pywintypes.error as ex:
        print(ex)
        input()
