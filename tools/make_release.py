#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
打包发布产物到 release\\ 目录。

前置：先运行 build.py（编译主程序）与 build_msi.py（生成安装包）。

产出：
    release\\WindowTabs-<版本>-zh-CN-portable.zip    免安装绿色版
    release\\WindowTabs-<版本>-zh-CN-installer.msi   安装包

用法:
    python build-local\\make_release.py
"""
import os
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# 脚本既可以放在仓库内的 tools/ 下，也可以放在仓库同级的目录里，两种都支持。
if os.path.exists(os.path.join(ROOT, "WtProgram", "WtProgram.fsproj")):
    REPO = ROOT
else:
    REPO = os.path.join(ROOT, "WindowTabs")
BIN = os.path.join(REPO, "WtProgram", "bin", "Release")
MSI = os.path.join(REPO, "WtSetup", "bin", "Release", "WtSetup.msi")
OUT = os.path.join(HERE, "out")
VERSION = "2025.06.30"

# 主程序用 --standalone --staticlink: 编译，运行时只依赖 .NET Framework 本身，
# 真正需要随包分发的只有 exe、config 和中文附属程序集。
PORTABLE = [
    "WindowTabs.exe",
    "WindowTabs.exe.config",
    "zh-CN/WindowTabs.resources.dll",
]

README_TXT = """WindowTabs {ver} 简体中文汉化版（免安装绿色版）
=================================================

运行
----
双击 WindowTabs.exe 即可，程序会常驻系统托盘（右下角图标）。

- 右键托盘图标 -> "设置..."      打开设置窗口
- 右键任意窗口的标签页           打开标签页菜单

中文显示
--------
中文版 Windows 会自动显示中文。
如果系统是其它语言，想强制用中文，先执行：

    set WINDOWTABS_LANG=zh-CN
    WindowTabs.exe

想长期生效（用户级）：

    setx WINDOWTABS_LANG zh-CN

环境
----
需要 .NET Framework 4.x（Win10 / Win11 已内置）。

如果某个程序的窗口没有出现标签页（尤其是以管理员权限运行的程序），
请右键 WindowTabs.exe -> "以管理员身份运行"。

文件说明
--------
WindowTabs.exe                      主程序
WindowTabs.exe.config               运行时配置
zh-CN\\WindowTabs.resources.dll      简体中文资源；删掉它会退回英文界面

项目地址
--------
https://github.com/shiranzby/WindowTabs
""".format(ver=VERSION)


def main():
    exe = os.path.join(BIN, "WindowTabs.exe")
    sat = os.path.join(BIN, "zh-CN", "WindowTabs.resources.dll")
    for p in (exe, sat, MSI):
        if not os.path.exists(p):
            raise SystemExit("缺少产物: " + p)

    # 只清理上一次生成的发布文件，不做整目录删除
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    else:
        for name in os.listdir(OUT):
            p = os.path.join(OUT, name)
            if os.path.isfile(p):
                os.remove(p)

    zip_name = "WindowTabs-%s-zh-CN-portable.zip" % VERSION
    zip_path = os.path.join(OUT, zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in PORTABLE:
            src = os.path.join(BIN, rel.replace("/", os.sep))
            z.write(src, rel)
        z.writestr("README.txt", README_TXT)
    print("绿色版: %s  (%.1f KB)" % (zip_path, os.path.getsize(zip_path) / 1024.0))

    msi_name = "WindowTabs-%s-zh-CN-installer.msi" % VERSION
    msi_path = os.path.join(OUT, msi_name)
    shutil.copyfile(MSI, msi_path)
    print("安装包: %s  (%.1f KB)" % (msi_path, os.path.getsize(msi_path) / 1024.0))

    print()
    print("zip 内文件:")
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            print("    %-40s %8d" % (info.filename, info.file_size))


if __name__ == "__main__":
    main()
