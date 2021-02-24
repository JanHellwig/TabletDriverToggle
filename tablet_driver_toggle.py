#!/usr/bin/env python3

import os
import pywintypes
import win32file
import win32service
import win32serviceutil


def install_wintab_dll(service: str) -> None:
    # https://www.reddit.com/r/wacom/comments/j1yfw5/wacom_and_huion_driver_conflict/
    win32file.CreateSymbolicLink(
        os.path.join(os.environ.get('SystemRoot'), 'System32', 'Wintab32.dll'),
        'Wintab32-{}.dll'.format(service), 0)
    win32file.CreateSymbolicLink(
        os.path.join(os.environ.get('SystemRoot'), 'SysWOW64', 'Wintab32.dll'),
        'Wintab32-{}64.dll'.format(service), 0)


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

    if is_service_running(wacom_service):
        disable_service(wacom_service)
        install_wintab_dll('huion')
        print('Now active: Huion')
    else:
        install_wintab_dll('wacom')
        enable_service(wacom_service)
        print('Now active: Wacom')

    input()


if __name__ == '__main__':
    try:
        main()
    except pywintypes.error as ex:
        print(ex)
        input()
