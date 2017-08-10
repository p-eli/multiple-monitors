#!/usr/bin/python3
from multiple_monitors.monitor import Monitor
# from monitor import Monitor
import subprocess
import os
import warnings
import functools

SHELLSHEBANG='#!/bin/sh'

class Xrand(object):
    _instance = None
    DEFAULTTEMPLATE = [SHELLSHEBANG, '%(xrandr)s']

    def __new__(cls):
        if not Xrand._instance:
            Xrand._instance = object.__new__(cls)
        return Xrand._instance

    def __init__(self):
        self.environ = dict(os.environ)

    def _output(self, args):
        p = subprocess.Popen(['xrandr'] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.environ)
        ret, err = p.communicate()
        status = p.wait()
        if status != 0:
            raise Exception("XRandR returned error code %d: %s" % (status, err))
        if err:
            warnings.warn("XRandR wrote to stderr, but did not report an error (Message was: %r)" % err)

        return ret

    def init_display_link(self):
        listproviders = self._output(["--listproviders"])
        for item in listproviders.decode('utf-8').split('\n'):
            if 'name:modesetting' in item:
                providers = item.split(' ')[1][0]
                argv = []
                argv.append('--setprovideroutputsource')
                argv.append(providers)
                argv.append("0")
                self._output(argv)

    def apply_profile(self, monitors, display_link=False):
        if display_link:
            self.init_display_link()
        args = []
        for m in monitors:
            args.append("--output")
            args.append(m.name)
            if not m.status:
                args.append("--off")
            else:
                args.append("--mode")
                args.append(str(m.resolution))
                args.append("--pos")
                args.append(str(m.position))
                args.append("--rotate")
                args.append(m.rotate)
                if m.primary:
                    args.append("--primary")
        self._output(args)



    def load_from_x(self):
        monitors = []
        screenline, items = self._load_raw_lines()
        screen = self._load_parse_screenline(screenline)
        for headline, details in items:
            if headline.startswith("  ") or headline == "":
                continue
            headline = headline.replace('unknown connection', 'unknown-connection')
            hsplit = headline.split(" ")
            monitor = Monitor(hsplit[0])
            monitors.append(monitor)
            monitor.status = hsplit[1]
            if hsplit[1] == "connected":
                if hsplit[2] == 'primary':
                    monitor.primary = True
                    resolution = hsplit[3]
                else:
                    monitor.primary = False
                    resolution = hsplit[2]
                res, monitor.position_x, monitor.position_y = resolution.split("+")
                monitor.resolution_x, monitor.resolution_y = res.split('x')
            available_resolution = []
            for item in details:
                available_resolution.append([item[1], item[2]])
            monitor.available_resolution = available_resolution
        return monitors, screen

    def _load_raw_lines(self):
            output = self._output(["--verbose"])
            items = []
            screenline = None
            for l in output.decode('utf8').split('\n'):
                if l.startswith("Screen "):
                    assert screenline is None
                    screenline = l
                elif l.startswith('\t'):
                    continue
                elif l.startswith(2 * ' '):  # [mode, width, height]
                    l = l.strip()
                    if functools.reduce(bool.__or__, [l.startswith(x + ':') for x in "hv"]):
                        l = l[-len(l):l.index(" start") - len(l)]
                        items[-1][1][-1].append(l[l.rindex(' '):])
                    else:  # mode
                        items[-1][1].append([l.split()])
                else:
                    items.append([l, []])
            return screenline, items

    def _load_parse_screenline(self, screenline):
            ssplit = screenline.split(" ")
            ssplit_expect = {"Screen":None, "minimum":None, "current":None, "maximum":None}
            for key in ssplit_expect.keys():
                for item in range(len(ssplit)):
                    if key == ssplit[item]:
                        if key != "Screen":
                            ssplit_expect[key] = [ssplit[item+1], ssplit[item+3]]
                        else:
                            ssplit_expect[key] = ssplit[item + 1]
            return ssplit_expect

# if __name__ == "__main__":
#     xrand = Xrand()
#     xrand.init_display_link()