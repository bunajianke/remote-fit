# Remote Fit

免费使用的 Windows / macOS 远程操作辅助工具，让手机和平板操作电脑更顺手。配合你已有的远程软件使用。

- 按手机、折叠屏和平板模板计算目标尺寸，选择系统或驱动支持的显示模式。
- 远程会话开始时切换，结束时还原；提供手动会话入口。
- 悬浮工具条提供复制、粘贴、Enter、最小化与全屏等快捷操作。
- 支持四边停靠、自由拖动、浅色／深色／跟随系统、窄屏导航。
- 软件内检查更新，保留设置，远程会话期间推迟安装。

## 下载

Windows：前往 [Windows 0.3.0 下载页](https://github.com/bunajianke/remote-fit/releases/tag/v0.3.0)，选择对应架构的 **Setup.exe**，便携使用请选择完整的 **Portable.zip**。

Mac：前往 [macOS 0.1.3 下载页](https://github.com/bunajianke/remote-fit/releases/tag/mac-v0.1.3)，下载 **RemoteFit-mac-universal.dmg**，将应用拖入“应用程序”。现有版本也可在软件内检查更新。

Windows 10/11，x64 或 ARM64。Mac 需要 macOS 14 或更新版本，支持 Apple 芯片与 Intel。

旧版尚无在线更新器，需要手动安装新版一次。Windows 更新器依赖完整安装结构，不能只拷贝单个 EXE。配置与显示恢复记录保存在用户目录，升级保留现有设置。Mac 不要从只读 DMG 中直接运行，否则不能就地更新。

当前安装包尚未取得 Windows 代码签名或 Apple Developer ID 公证，首次启动请按系统提示核对来源。每个包提供 SHA-256 校验；Mac 在线更新包与更新信息另有 Ed25519 签名。

## 当前兼容范围

Mac 已接入 UU 被控会话检测；向日葵、ToDesk 自动检测仍待适配。Windows 内置 RDP/WTS 检测，第三方远控目前使用手动会话、日志或回调接入。无法识别的远控软件可使用手动会话。

仅使用系统或驱动提供的显示模式；Windows 可尝试驱动接受的自定义模式。没有创建任意尺寸虚拟屏的功能。Mac 版仍处于测试阶段。

此公开仓库仅分发安装包和更新信息，应用源码保存在私有仓库。
