#!/usr/bin/env python3
"""Recalculate an .xlsx with LibreOffice headless (UNO) and save a copy with cached values.

usage: python3 lo_recalc.py IN.xlsx OUT.xlsx [Scenario]
If Scenario (1/2/3) is given, Scenarios!C3 is set before recalculation.
"""
import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue


def prop(n, v):
    p = PropertyValue()
    p.Name, p.Value = n, v
    return p


def main():
    src, dst = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    scen = int(sys.argv[3]) if len(sys.argv) > 3 else None
    port = 2002 + (os.getpid() % 500)
    prof = f"/tmp/lo_profile_{port}"
    proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--nologo", "--norestore",
                             f"-env:UserInstallation=file://{prof}",
                             f"--accept=socket,host=127.0.0.1,port={port};urp;"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        ctx = None
        for _ in range(60):
            try:
                ctx = resolver.resolve(f"uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(0.5)
        if ctx is None:
            raise RuntimeError("could not connect to soffice")
        desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(src), "_blank", 0, (prop("Hidden", True),))
        if scen:
            doc.Sheets.getByName("Scenarios").getCellRangeByName("C3").setValue(scen)
        doc.calculateAll()
        doc.storeToURL(uno.systemPathToFileUrl(dst), (prop("FilterName", "Calc MS Excel 2007 XML"),))
        doc.close(True)
    finally:
        try:
            desktop.terminate()
        except Exception:
            pass
        time.sleep(1)
        proc.kill()


if __name__ == "__main__":
    main()
