#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build WindowTabs (localized zh-CN fork) WITHOUT Visual Studio.

Why this script exists
----------------------
WindowTabs targets .NET Framework 4.0 (Win32.dll even targets 2.0) and uses an
old-style fsproj + FSharp.PowerPack.  Visual Studio + the F# desktop workload is
the "official" way to build it, but the build can also be reproduced with the
plain .NET SDK by supplying the three things VS would have provided:

  1. .NET Framework reference assemblies  -> Microsoft.NETFramework.ReferenceAssemblies.*
  2. A modern F# compiler                 -> the one shipped inside the .NET SDK
  3. Legacy F# MSBuild targets            -> also shipped inside the .NET SDK

Notes / gotchas discovered the hard way:
  * .NET Core MSBuild has no ResGen.exe -> pass ResGenExecuteAsTool=false.
  * The legacy AL-based satellite-assembly target is broken on .NET Core MSBuild
    ("AL task does not support EnvironmentVariables"), so we skip it
    (GenerateSatelliteAssembliesForCore=true) and build the resources.dll files
    ourselves with the standalone F# compiler.
  * The Fsc MSBuild task does NOT quote DotnetFscCompilerPath, so that path must
    not contain spaces -> we expose the SDK's FSharp folder through a junction.
  * The F# compiler of FSharp.Compiler.Tools is too old (rejects `10f` float32
    literals), so it is only used to emit the tiny satellite assemblies.

Usage:
    python tools/build.py            # 脚本在仓库内的 tools/ 目录时
    python build-local/build.py      # 脚本放在仓库同级目录时
"""

import os
import shutil
import subprocess
import sys
import zipfile

PY_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(PY_DIR)
# 脚本既可以放在仓库内的 tools/ 下，也可以放在仓库同级的目录里，两种都支持。
if os.path.exists(os.path.join(PARENT, "WtProgram", "WtProgram.fsproj")):
    REPO = PARENT
else:
    REPO = os.path.join(PARENT, "WindowTabs")
WORKSPACE = os.path.dirname(REPO)
CACHE = os.path.join(PY_DIR, "cache")
PROJECT = os.path.join(REPO, "WtProgram", "WtProgram.fsproj")
OUT_DIR = os.path.join(REPO, "WtProgram", "bin", "Release")
OBJ_DIR = os.path.join(REPO, "WtProgram", "obj", "Release")

REF_FW = os.path.join(CACHE, "fw")                 # .NET Framework reference assemblies
FCT_TOOLS = os.path.join(CACHE, "fct", "tools")    # standalone F# compiler (satellites only)
SDK_LINK = os.path.join(CACHE, "fsharp-sdk")       # junction -> <dotnet sdk>/FSharp

DOTNET = shutil.which("dotnet") or r"C:\Program Files\dotnet\dotnet.exe"
SDK_ROOT = os.path.join(os.path.dirname(DOTNET), "sdk")

REF_PACKAGES = [
    # (nuget id, version, framework folder inside build/.NETFramework)
    ("Microsoft.NETFramework.ReferenceAssemblies.net20", "1.0.3", "v2.0"),
    ("Microsoft.NETFramework.ReferenceAssemblies.net40", "1.0.3", "v4.0"),
]
FCT_PACKAGE = ("FSharp.Compiler.Tools", "10.2.3")


def log(msg):
    print("[build] " + msg, flush=True)


def run(args, tolerate=False, **kw):
    log("$ " + " ".join(args))
    p = subprocess.run(args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", **kw)
    out = (p.stdout or "") + (p.stderr or "")
    if p.returncode != 0 and not tolerate:
        print(out)
        raise SystemExit("命令失败, 退出码 %d" % p.returncode)
    return out


def download_nupkg(pkg_id, version):
    os.makedirs(CACHE, exist_ok=True)
    dst = os.path.join(CACHE, "%s.%s.nupkg" % (pkg_id, version))
    if os.path.exists(dst) and os.path.getsize(dst) > 1024:
        return dst
    url = "https://www.nuget.org/api/v2/package/%s/%s" % (pkg_id, version)
    log("下载 %s %s" % (pkg_id, version))
    run(["curl", "-sSL", "-o", dst, url])
    return dst


def ensure_reference_assemblies():
    """Put *.dll for every needed TargetFrameworkVersion under CACHE/fw/.NETFramework/<ver>."""
    for pkg_id, version, fw in REF_PACKAGES:
        target = os.path.join(REF_FW, ".NETFramework", fw)
        probe = os.path.join(target, "mscorlib.dll")
        if os.path.exists(probe):
            continue
        nupkg = download_nupkg(pkg_id, version)
        # 直接把包里的参考程序集解到目标目录，避免整目录删除（更安全，也更快）
        prefix = "build/.NETFramework/%s/" % fw
        os.makedirs(target, exist_ok=True)
        count = 0
        with zipfile.ZipFile(nupkg) as z:
            for name in z.namelist():
                if not name.startswith(prefix) or name.endswith("/"):
                    continue
                rel = name[len(prefix):]
                dst = os.path.join(target, rel.replace("/", os.sep))
                d = os.path.dirname(dst)
                if d:
                    os.makedirs(d, exist_ok=True)
                with z.open(name) as src, open(dst, "wb") as out:
                    shutil.copyfileobj(src, out)
                count += 1
        if count == 0:
            raise SystemExit("包结构异常，缺少 " + prefix)
        log("参考程序集就绪: %s (%d 个文件)" % (target, count))


def ensure_compiler_tools():
    """Standalone F# compiler (FSharp.Compiler.Tools) - used for satellite assemblies only."""
    global FCT_TOOLS
    probe = os.path.join(FCT_TOOLS, "fsc.exe")
    if not os.path.exists(probe):
        pkg_id, version = FCT_PACKAGE
        nupkg = download_nupkg(pkg_id, version)
        root = os.path.join(CACHE, "fct")
        os.makedirs(root, exist_ok=True)
        with zipfile.ZipFile(nupkg) as z:
            z.extractall(root)          # 增量覆盖，不预先删除目录
    if not os.path.exists(FCT_TOOLS):
        # 兼容大小写不同的解包结果
        for name in os.listdir(os.path.join(CACHE, "fct")):
            cand = os.path.join(CACHE, "fct", name, "tools")
            if os.path.isdir(cand):
                FCT_TOOLS = cand
                break
    if not os.path.exists(os.path.join(FCT_TOOLS, "fsc.exe")):
        raise SystemExit("找不到 fsc.exe")
    log("独立 F# 编译器就绪: %s" % FCT_TOOLS)


def sdk_fsharp_dir():
    root = SDK_ROOT
    if not os.path.isdir(root):
        raise SystemExit("没有找到 .NET SDK: " + root)
    versions = sorted(os.listdir(root), reverse=True)
    for v in versions:
        cand = os.path.join(root, v, "FSharp")
        if os.path.exists(os.path.join(cand, "fsc.dll")):
            return cand
    raise SystemExit("SDK 里找不到 FSharp/fsc.dll")


def ensure_fsharp_link():
    """junction with no spaces, because the Fsc MSBuild task doesn't quote the path."""
    real = sdk_fsharp_dir()
    if os.path.exists(os.path.join(SDK_LINK, "fsc.dll")):
        return real
    os.makedirs(CACHE, exist_ok=True)
    if os.path.exists(SDK_LINK):
        # 只删掉目录联接本身（rmdir 不会跟进目标），不要用 rmtree
        subprocess.run(["cmd", "/c", "rmdir", SDK_LINK],
                       capture_output=True, text=True, errors="replace")
    p = subprocess.run(["cmd", "/c", "mklink", "/J", SDK_LINK, real],
                       capture_output=True, text=True, errors="replace")
    if not os.path.exists(os.path.join(SDK_LINK, "fsc.dll")):
        print(p.stdout or "", p.stderr or "")
        raise SystemExit("无法创建 junction（路径含空格会破坏编译）；请手动执行:\n"
                         '  mklink /J "%s" "%s"' % (SDK_LINK, real))
    log("编译器无空格路径: %s -> %s" % (SDK_LINK, real))
    return real


def msbuild_props(real_fsharp_dir):
    return [
        "-p:Configuration=Release",
        "-p:ResGenExecuteAsTool=false",
        "-p:GenerateSatelliteAssembliesForCore=true",
        "-p:FscToolPath=" + os.path.dirname(DOTNET),
        "-p:FscToolExe=dotnet.exe",
        "-p:DotnetFscCompilerPath=" + os.path.join(SDK_LINK, "fsc.dll"),
        "-p:TargetFrameworkRootPath=" + REF_FW + os.sep,
        "-p:FSharpTargetsPath=" + os.path.join(real_fsharp_dir, "Microsoft.FSharp.Targets"),
    ]


def build_once(tolerate=False):
    out = run([DOTNET, "build", PROJECT, "-nologo", "-v:m"] + msbuild_props(sdk_fsharp_dir()),
              tolerate=tolerate)
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("WtProgram ->") or "已成功生成" in s or ("error" in s.lower() and "MSB" in s):
            print("    " + s)
    return out


def make_satellite(culture):
    """资源附属程序集 WindowTabs.resources.dll（.NET Framework 的标准本地化机制）"""
    res = os.path.join(OBJ_DIR, "Properties.Resources.%s.resources" % culture)
    if not os.path.exists(res):
        raise SystemExit("缺少资源文件 " + res + "（应先执行 msbuild）")
    outdir = os.path.join(OBJ_DIR, culture)
    os.makedirs(outdir, exist_ok=True)
    src = os.path.join(outdir, "satellite.fs")
    with open(src, "w", encoding="utf-8", newline="\r\n") as f:
        f.write('module WindowTabsSatellite\n\n'
                'open System.Reflection\n\n'
                '[<assembly: AssemblyCulture("%s")>]\n'
                'do ()\n' % culture)
    fw = os.path.join(REF_FW, ".NETFramework", "v4.0")
    fscore = os.path.join(REPO, "packages", "FSharp.Core.4.3.0.0.Microsoft.Signed.3.0.0.1",
                          "lib", "net40", "FSharp.Core.dll")
    outdll = os.path.join(outdir, "WindowTabs.resources.dll")
    # 两种资源逻辑名都写入：不同 .NET 版本的 ResourceManager 查找名不同，双写可保证命中
    args = [os.path.join(FCT_TOOLS, "fsc.exe"), "--nologo", "--noframework",
            "--target:library", "--out:" + outdll,
            "-r:" + os.path.join(fw, "mscorlib.dll"),
            "-r:" + os.path.join(fw, "System.dll"),
            "-r:" + fscore,
            "--resource:%s,Properties.Resources.resources" % res,
            "--resource:%s,Properties.Resources.%s.resources" % (res, culture),
            src]
    run(args)
    log("附属程序集: %s" % outdll)
    return outdll


def copy_satellites():
    for culture in ("zh-CN", "ja-JP"):
        dll = make_satellite(culture)
        dst = os.path.join(OUT_DIR, culture)
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(dll, os.path.join(dst, "WindowTabs.resources.dll"))


def main():
    if not os.path.isdir(os.path.join(REPO, ".git")):
        raise SystemExit("找不到仓库目录: " + REPO)
    log("工作区: " + WORKSPACE)
    ensure_reference_assemblies()
    ensure_compiler_tools()
    real = ensure_fsharp_link()

    # 第一遍：编译主程序并生成 obj 下的 .resources
    # 首次全新构建时，MSBuild 会因为附属程序集尚未生成而在“复制”这一步报错，属预期
    log("第一遍编译（旨在产出 exe 与 obj/*.resources）")
    build_once(tolerate=True)
    # 生成中/日文附属程序集（.NET Core 的 MSBuild 不支持老式 AL 任务，故自行生成）
    copy_satellites()
    # 第二遍：把附属程序集复制到 bin，校验整体成功
    log("第二遍编译（复制附属程序集并确认成功）")
    out = build_once()
    if "已成功生成" not in out and "Build succeeded" not in out:
        raise SystemExit("构建未确认成功，请检查上面的输出")

    exe = os.path.join(OUT_DIR, "WindowTabs.exe")
    if not os.path.exists(exe):
        raise SystemExit("构建产物不存在: " + exe)
    print()
    log("构建完成:")
    print("    可执行文件: " + exe)
    print("    中文资源  : " + os.path.join(OUT_DIR, "zh-CN", "WindowTabs.resources.dll"))
    print()
    print("    直接双击 WindowTabs.exe 即可运行；中文系统会自动显示中文，")
    print("    其它语言系统可设 WINDOWTABS_LANG=zh-CN 后启动。")


if __name__ == "__main__":
    main()
