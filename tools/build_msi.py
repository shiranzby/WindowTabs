#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用仓库自带的 WiX Toolset 3.11.1 生成简体中文安装包 (WtSetup.msi)。

前置：先运行 build.py 生成 WtProgram\\bin\\Release。

用法:
    python build-local\\build_msi.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# 脚本既可以放在仓库内的 tools/ 下，也可以放在仓库同级的目录里，两种都支持。
if os.path.exists(os.path.join(ROOT, "WtProgram", "WtProgram.fsproj")):
    REPO = ROOT
else:
    REPO = os.path.join(ROOT, "WindowTabs")
WIX = os.path.join(REPO, "packages", "WiX.Toolset.UnofficialFork.3.11.1", "tools", "wix")
SETUP = os.path.join(REPO, "WtSetup")
TARGET_DIR = os.path.join(REPO, "WtProgram", "bin", "Release")


def run(args, cwd):
    print("$ " + " ".join(args))
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    if out.strip():
        print(out.rstrip())
    if p.returncode != 0:
        raise SystemExit("命令失败, 退出码 %d" % p.returncode)
    return out


def main():
    candle = os.path.join(WIX, "candle.exe")
    light = os.path.join(WIX, "light.exe")
    for exe in (candle, light):
        if not os.path.exists(exe):
            raise SystemExit("找不到 WiX 工具: " + exe)

    sat = os.path.join(TARGET_DIR, "zh-CN", "WindowTabs.resources.dll")
    if not os.path.exists(sat):
        raise SystemExit("缺少中文附属程序集, 请先运行 build.py: " + sat)

    obj = os.path.join(SETUP, "obj", "Release")
    out = os.path.join(SETUP, "bin", "Release")
    os.makedirs(obj, exist_ok=True)
    os.makedirs(out, exist_ok=True)

    wixobj = os.path.join(obj, "WtSetup.wixobj")
    msi = os.path.join(out, "WtSetup.msi")

    # WtSetup.wxs 里用 $(var.WtProgram.TargetDir) 引用已编译产物
    run([candle, "-nologo", "-out", wixobj,
         "-dWtProgram.TargetDir=" + TARGET_DIR + os.sep,
         "WtSetup.wxs"], cwd=SETUP)
    run([light, "-nologo", "-out", msi, wixobj], cwd=SETUP)

    print()
    print("安装包已生成: " + msi)


if __name__ == "__main__":
    main()
