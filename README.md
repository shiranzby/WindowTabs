<img src="https://raw.githubusercontent.com/leafOfTree/leafOfTree.github.io/master/windowtabs.png" width="60" height="60" alt="icon" align="left"/>

# WindowTabs 简体中文汉化版

[简体中文](README.md) | [English](README_EN.md)

本项目是 [leafOfTree/WindowTabs](https://github.com/leafOfTree/WindowTabs) 的**完整简体中文汉化**分支。

原项目界面全部为英文（仅自带一份不完整的日语翻译），本分支在不改变任何功能行为的前提下，
把**所有用户可见文本**接入了 .NET 标准的资源本地化机制，并补全了简体中文（`zh-CN`）翻译。

<p>
<img alt="screenshot" src="https://raw.githubusercontent.com/leafOfTree/leafOfTree.github.io/master/WindowTabs-example.png" width="560" style="border-radius: 8px" />
</p>

---

## 下载

<a href="https://github.com/shiranzby/WindowTabs/releases">![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/shiranzby/windowtabs/total)</a>

从 [Releases](https://github.com/shiranzby/WindowTabs/releases) 页面下载：

| 文件 | 说明 |
| --- | --- |
| `WindowTabs-2025.06.30-zh-CN-portable.zip` | **免安装绿色版**。解压到任意目录，双击 `WindowTabs.exe` 即可 |
| `WindowTabs-2025.06.30-zh-CN-installer.msi` | 安装包（如需） |
| `Source code (zip)` | GitHub 自动生成，对应本汉化版的源码 |

## 直接运行

已经编译好了，直接跑这个文件：

```
WindowTabs\WtProgram\bin\Release\WindowTabs.exe
```

注意事项：

- **整个 `bin\Release` 目录要一起保留**：`WindowTabs.exe`、`WindowTabs.exe.config`、`Win32.dll`、
  `FSharp*.dll`、`Aga.Controls.dll`、`Newtonsoft.Json.dll`、`System.ValueTuple.dll`，
  以及 `zh-CN\`、`ja-JP\` 两个子目录。
- 其中 `zh-CN\WindowTabs.resources.dll` 就是简体中文资源；**删掉它，界面会退回英文。**
- 启动后程序常驻托盘（右下角图标）。右键托盘图标 →「设置…」打开设置窗口；
  在任意已被合并的窗口标签上右键，就是标签页菜单。
- 中文版 Windows 自动显示中文。非中文系统想强制中文，先 `set WINDOWTABS_LANG=zh-CN` 再启动。
- WindowTabs 要管理别的窗口，如果某个程序（尤其是以管理员权限跑的）没出现标签页，
  请以管理员身份运行 `WindowTabs.exe`。

---

## 汉化覆盖范围

| 界面位置 | 汉化内容 |
| --- | --- |
| 托盘图标右键菜单 | 「设置…」「退出 WindowTabs」 |
| 托盘气泡提示 | 新版本提示文案 |
| 标签页右键菜单 | 新建窗口、展开/收起标签页、标签页对齐（靠左/居中/靠右）、最大化时自动隐藏、合并任务栏图标、重命名标签页、恢复标签页名称、移除/合并某程序的标签页、关闭/关闭其他/关闭所有 `xxx` 窗口/全部关闭、设置… |
| 设置窗口标题 | `WindowTabs 设置 (版本 x)` |
| 设置 · 程序 | 列头（名称、标签页、自动分组）、刷新、就绪 |
| 设置 · 外观 | 高度、最大宽度、重叠、颜色、背景(普通/高亮/活动/闪烁)、边框、缩进(普通/翻转)、重置、深色模式、深色模式(蓝)、颜色值校验提示 |
| 设置 · 行为 | 分组标题（基础 / 任务 / 标签页切换）与全部选项、对齐方式下拉（靠左/居中/靠右） |
| 设置 · 工作区 | 列头（名称、匹配方式、标题）、新建/还原/编辑/移除、匹配方式（精确匹配/开头为/结尾为/包含/正则表达式）、编辑对话框标签、默认名称（工作区 N / 分组 N） |
| 设置 · 诊断 | 扫描、复制到剪贴板、复制设置文件到 exe 目录、工具栏与状态栏文案、提示与报错弹窗 |
| 设置 · 许可证 | 许可证密钥、激活、离线激活及全部提示/结果弹窗 |
| 通用弹窗 | 确定 / 取消、设置文件解析错误提示、重复运行提示 |
| 拖放菜单 | 复制 / 移动 / 取消 |
| 安装包 | MSI 语言标记改为简体中文（`2052`） |

> 说明：`.msi` 是无界面的静默安装包，本身没有向导文字；产品名保持品牌名 `WindowTabs` 不变。

---

## 语言是如何选择的

字体与文案都存放在资源文件里，运行时按**当前 UI 语言**自动匹配：

1. `WtProgram/Properties/Resources.resx` —— 中性资源（英文原文，作为兜底）
2. `WtProgram/Properties/Resources.zh-CN.resx` —— 简体中文（本次新增）
3. `WtProgram/Properties/Resources.ja-JP.resx` —— 日语（原项目自带，本次顺手补齐了缺失的 2 个键）

因此：

- **中文版 Windows**：直接显示中文，无需任何操作。
- **非中文版 Windows**：默认跟随系统语言；如需强制中文，设置环境变量即可：

  ```cmd
  set WINDOWTABS_LANG=zh-CN
  WindowTabs.exe
  ```

  也可以长期设置（用户级）：

  ```cmd
  setx WINDOWTABS_LANG zh-CN
  ```

- 想临时切回英文：`set WINDOWTABS_LANG=en`；切日语：`set WINDOWTABS_LANG=ja-JP`。

---

## 汉化实现

### 新增文件

| 文件 | 作用 |
| --- | --- |
| `WtProgram/Shared/Res.fs` | 统一的取词入口 `Res.get "Key"`：读取当前 UI 语言的资源，找不到时回退为键名本身（不会出现空标题）；并提供 `WINDOWTABS_LANG` 覆盖逻辑 |
| `WtProgram/Properties/Resources.zh-CN.resx` | 简体中文翻译，111 个键，与中性资源**逐键一一对应** |

### 修改的源文件

| 文件 | 改动 |
| --- | --- |
| `WtProgram/WtProgram.fsproj` | 注册 `Shared/Res.fs`（放在 `Shared/Operators.fs` 之后）与 `Resources.zh-CN.resx` 为 `EmbeddedResource` |
| `WtProgram/Properties/Resources.resx` | 新增 65 个键（原本硬编码在代码里的文案），英文原文作为兜底 |
| `WtProgram/Properties/Resources.ja-JP.resx` | 补齐原项目遗漏的 `DarkMode` / `DarkModeBlue` |
| `WtProgram/TabStripDecorator.fs` | 标签页右键菜单 15 处文案 |
| `WtProgram/ManagerViewService/Views/DiagnosticsView.fs` | 9 处 |
| `WtProgram/ManagerViewService/Views/BehaviorView.fs` | 分组标题 + 对齐下拉（**存储值仍为英文规范值，仅显示本地化**，老配置不失效） |
| `WtProgram/ManagerViewService/Views/LicenseView.fs` | 11 处 |
| `WtProgram/ManagerViewService/Views/ProgramView.fs` | 3 处 |
| `WtProgram/ManagerViewService/DesktopManagerForm.fs` | 窗口标题 |
| `WtProgram/Workspace/WorkspaceModel.fs` | 编辑对话框标签、默认工作区/分组名称（同时兼容中英两种已有名称的解析） |
| `WtProgram/Workspace/WorkspaceView.fs` | 匹配方式显示本地化 |
| `WtProgram/DesktopPlugins/NotifyIconPlugin.fs` | 托盘提示与气泡 |
| `WtProgram/Shared/UIHelper.fs` | 确定/取消、颜色校验提示；`EnumEditor` 改为「枚举值不变、只本地化显示文本」 |
| `WtProgram/Settings.fs` | 设置文件与外观设置的两处错误弹窗 |
| `WtProgram/OleDropTarget.fs` | 拖放菜单 |
| `WtProgram/TaskSwitch.fs` | 任务切换器列头 |
| `WtProgram/Program.fs` | 重复运行提示；启动时应用 `WINDOWTABS_LANG` |
| `WtSetup/WtSetup.wxs` | `Language="1033"` → `Language="2052"`；并把 `zh-CN\WindowTabs.resources.dll` 加入安装清单（上游原来的安装包只装 `WindowTabs.exe`，装完仍是英文界面） |

### 几个刻意的设计取舍

- **持久化数据一律保持英文规范值。** 「对齐方式」在 `WindowTabsSettings.txt` 里仍存 `Left/Center/Right`，
  匹配方式仍存枚举名，只有**显示**被翻译。这样升级后原有配置文件不会失效。
- **日语的显示效果不变。** 原本硬编码的英文文案在日语环境下也是英文，现在改成资源查找后会回退到中性（英文）资源，行为一致。
- **`Res.get` 找不到键时返回键名本身**，因此即使某个翻译漏了，界面上也只会出现键名，而不是空白或崩溃。

---

## 编译

### 方式一：Visual Studio（项目原本的方式）

- Visual Studio 2019 / 2022，安装时勾选 `.NET desktop development`
- WiX Toolset build tools v3.14.1 + VS 扩展（仅编译安装包需要）

打开 `WindowTabs.sln`，选择 `Release` 后生成即可：

```
WindowTabs\WtProgram\bin\Release\WindowTabs.exe
```

生成后 `bin\Release\zh-CN\WindowTabs.resources.dll` 就是简体中文附属程序集，缺了它界面会回退成英文。

### 方式二：只有 .NET SDK，没有 Visual Studio（本机已实测通过）

在仓库外层执行一条命令即可：

```cmd
python build-local\build.py
```

（脚本在 `github项目\build-local\`，不在本仓库内，所以不会污染本分支的改动。）

脚本会自动完成：下载 .NET Framework v2.0 / v4.0 参考程序集与一个独立 F# 编译器到
`build-local\cache\` → 用 .NET SDK 编译 `Win32` 与 `WtProgram` → 生成 `zh-CN` / `ja-JP`
附属程序集 → 输出到 `WtProgram\bin\Release\`。

这条路要绕开三个坑，脚本里都已经处理：

1. **.NET Core 版 MSBuild 没有 `ResGen.exe`** → 必须传 `ResGenExecuteAsTool=false`。
2. **老式附属程序集目标依赖 `AL` 任务，而 .NET Core 版 MSBuild 的 `AL` 任务不支持
   `EnvironmentVariables` 参数**（报 `MSB4064`）→ 跳过该目标，改用独立 F# 编译器手写
   `WindowTabs.resources.dll`（脚本里的 `make_satellite()`）。
3. **`Fsc` 任务不给 `DotnetFscCompilerPath` 加引号**，路径带空格会被拆成
   `dotnet-C:\Program` 直接失败 → 用目录联接（junction）把 SDK 的 `FSharp` 目录映射到一个
   无空格的路径上。

另外：这条工具链用的是 **.NET SDK 自带的 F# 8 编译器**（它才认 `10f` 这种 float32 写法）；
`FSharp.Compiler.Tools` 那份独立编译器版本偏老，所以只用来生成附属程序集。

### 生成安装包与发布产物（可选）

```cmd
python build-local\build_msi.py       :: 生成 WtSetup\bin\Release\WtSetup.msi
python build-local\make_release.py    :: 打包到 release\ 目录
```

`build_msi.py` 用仓库里自带的 WiX Toolset 3.11.1（`packages/` 目录）直接调用 `candle` + `light`，
不需要安装 WiX 的 VS 扩展。`make_release.py` 会产出：

```
release\WindowTabs-2025.06.30-zh-CN-portable.zip
release\WindowTabs-2025.06.30-zh-CN-installer.msi
```

> 关于绿色版为什么只有 3 个文件：主程序是用 `--standalone --staticlink:` 编译的，
> `Win32.dll` / `FSharp.PowerPack.dll` / `Aga.Controls.dll` / `Newtonsoft.Json.dll` 都已经静态链接进
> `WindowTabs.exe`（已用反射确认：它的引用只有 .NET Framework 自身的程序集）。
> 所以随包真正需要分发的只有 `WindowTabs.exe`、`WindowTabs.exe.config` 和 `zh-CN\WindowTabs.resources.dll`。

---

## 如何补充或修改翻译

1. 打开 `WtProgram/Properties/Resources.zh-CN.resx`；
2. 只改 `<value>`，**不要改 `name`**（`name` 必须与 `Resources.resx` 中的键完全一致）；
3. 含 `%s` / `%d` / `%x` / `{0}` 的条目请保留占位符；
4. 重新生成即可生效。

新增界面文案时，请同时在 `Resources.resx`（英文）与 `Resources.zh-CN.resx`（中文）里各加一条同名键，
代码中通过 `Res.get "键名"` 取用。

---

## 已知限制

- 本机没有 Visual Studio，因此改为用 .NET SDK 编译：**主程序与安装包都已完整生成（0 错误）**，
  并做了运行时校验（用 .NET Framework 的 `ResourceManager` 在隔离目录里读取构建产物，
  `zh-CN` 能取到「外观 / 行为 / 诊断 / 设置…」等中文，中性资源仍回退英文）。
  仍建议在有 VS 的机器上再跑一次 Release 生成做交叉验证。
- `Win32/HotKeyControl2.cs`（一个未被项目引用的备用快捷键控件）内部仍有英文常量，未处理。
- `Settings/` 目录下的 WinForms 工程不在 `WindowTabs.sln` 中，属于历史遗留代码，未处理。
- 附属程序集里同一份资源写了两个逻辑名（`Properties.Resources.resources` 与
  `Properties.Resources.zh-CN.resources`），以兼容不同版本 `ResourceManager` 的查找名；
  文件只有十几 KB，不影响使用。
- MSI 的产品版本号仍是上游的 `0.0.70`（MSI 的版本字段上限为 255.255.65535，
  写不进 `2025.06.30`），没有改动，以免影响升级判断。

---

## 上游与历史

- 最初由 Maurice Flanagan 于 2009 年开发，曾分免费版与付费版；作者无暇维护后开源。
- 本仓库 fork 自 [leafOfTree/WindowTabs](https://github.com/leafOfTree/WindowTabs)，
  它又来自 [payaneco/WindowTabs](https://github.com/payaneco/WindowTabs) → [redgis/WindowTabs](https://github.com/redgis/WindowTabs)。
- 上游项目地址：[mauricef/WindowTabs](https://github.com/mauricef/WindowTabs)（原始仓库）。

英文说明请见 [README_EN.md](README_EN.md)。
