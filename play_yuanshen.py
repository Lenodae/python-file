#!/usr/bin/env python3
"""
双击运行 — 原神一键启动 / 下载安装，Windows / macOS 通用。
优先级：已有游戏 → 直接启动 → 已有启动器 → 打开启动器 → 都没有 → 下载安装
"""
import sys
import os
import subprocess
import webbrowser
import platform
from configparser import ConfigParser
import urllib.request

# 米哈游启动器（Windows）官方 CDN 直链
WIN_LAUNCHER_URL = "https://hyp-webstatic.mihoyo.com/hyp-client/hyp_cn_setup_1.4.5.exe"
WEB_URL = "https://launcher.mihoyo.com/"

# 原神游戏可能所在的路径模式（按盘符展开）
GAME_PATH_PATTERNS = [
    r"{drive}:\Program Files\Genshin Impact\Genshin Impact Game\YuanShen.exe",
    r"{drive}:\Genshin Impact\Genshin Impact Game\YuanShen.exe",
    r"{drive}:\Program Files (x86)\Genshin Impact\Genshin Impact Game\YuanShen.exe",
]

# 启动器可能所在的路径
LAUNCHER_PATHS = [
    r"C:\Program Files\miHoYo Launcher\launcher.exe",
    r"C:\Program Files (x86)\miHoYo Launcher\launcher.exe",
    r"C:\Program Files\Genshin Impact\launcher.exe",
]

# config.ini 可能所在路径（用于读取游戏安装位置）
CONFIG_PATHS = [
    r"{drive}:\Program Files\miHoYo Launcher\config.ini",
    r"{drive}:\Program Files\Genshin Impact\config.ini",
]


def find_yuanshen():
    """查找原神游戏主程序，返回路径或 None"""
    # 1. 直接搜索常见路径
    drives = ["C", "D", "E", "F", "G", "H"]
    for drive in drives:
        for pattern in GAME_PATH_PATTERNS:
            path = pattern.format(drive=drive)
            if os.path.exists(path):
                return path

    # 2. 从启动器 config.ini 中读取游戏安装路径
    for drive in drives:
        for cfg_pattern in CONFIG_PATHS:
            cfg_path = cfg_pattern.format(drive=drive)
            if os.path.exists(cfg_path):
                try:
                    cp = ConfigParser()
                    cp.read(cfg_path, encoding="utf-8")
                    game_path = cp.get("launcher", "game_install_path", fallback=None)
                    if game_path:
                        game_path = game_path.strip().strip('"')
                        exe_path = os.path.join(game_path, "YuanShen.exe")
                        if os.path.exists(exe_path):
                            return exe_path
                except Exception:
                    pass

    # 3. 尝试 Windows 注册表
    if platform.system() == "Windows":
        try:
            import winreg
            for subkey in [r"SOFTWARE\miHoYo\原神", r"SOFTWARE\miHoYo\Genshin Impact"]:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey)
                    try:
                        val, _ = winreg.QueryValueEx(key, "GameInstallPath")
                        exe_path = os.path.join(val.strip(), "YuanShen.exe")
                        if os.path.exists(exe_path):
                            winreg.CloseKey(key)
                            return exe_path
                    except FileNotFoundError:
                        pass
                    winreg.CloseKey(key)
                except FileNotFoundError:
                    pass
        except ImportError:
            pass

    return None


def find_launcher():
    """查找启动器，返回路径或 None"""
    for p in LAUNCHER_PATHS:
        if os.path.exists(p):
            return p
    return None


def download_with_progress(url, dest):
    """下载文件并显示进度条"""
    print(f"下载地址: {url}")
    print(f"保存位置: {dest}")
    print(f"文件大小: 约 169 MB")
    print("正在下载，请耐心等待...\n")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            block_size = 8192
            with open(dest, "wb") as f:
                while True:
                    block = resp.read(block_size)
                    if not block:
                        break
                    f.write(block)
                    downloaded += len(block)
                    if total > 0:
                        pct = downloaded / total * 100
                        bar_len = 40
                        filled = int(bar_len * downloaded / total)
                        bar = "#" * filled + "-" * (bar_len - filled)
                        size_mb = downloaded / (1024 * 1024)
                        total_mb = total / (1024 * 1024)
                        print(
                            f"\r[{bar}] {pct:.1f}%  {size_mb:.0f}/{total_mb:.0f} MB",
                            end="",
                        )
        print("\n\n下载完成！")
        return True
    except Exception as e:
        print(f"\n下载失败: {e}")
        return False


def install_launcher_silent(installer_path):
    """静默安装启动器（NSIS 格式支持 /S）"""
    print("正在静默安装启动器（请勿关闭此窗口）...")
    try:
        subprocess.run([installer_path, "/S"], check=True, timeout=120)
        print("安装完成！")
        return True
    except subprocess.TimeoutExpired:
        print("安装超时，请手动运行安装包。")
        return False
    except Exception as e:
        print(f"安装出错: {e}")
        return False


def main():
    print("=" * 50)
    print("  原神 — 一键启动 / 下载安装")
    print("=" * 50)
    print()

    system = platform.system()

    if system == "Windows":
        # ---- 第零步：查找原神游戏 ----
        game_path = find_yuanshen()
        if game_path:
            print(f"[√] 检测到原神已安装！")
            print(f"    路径: {game_path}")
            print()
            print("正在启动原神，祝你游戏愉快！")
            os.startfile(game_path)
            input("按回车键退出...")
            return

        # ---- 第一步：查找启动器 ----
        launcher = find_launcher()
        if launcher:
            print(f"[√] 未找到原神游戏，但启动器已安装")
            print(f"    路径: {launcher}")
            print()
            skip = input("是否打开启动器下载原神？(Y/n): ").strip().lower()
            if skip != "n":
                print("正在打开启动器...")
                os.startfile(launcher)
                print("请在启动器中登录并下载原神（约 70GB+）。")
            input("按回车键退出...")
            return

        # ---- 第二步：下载安装启动器 ----
        print("[!] 未检测到原神或启动器，开始下载安装...\n")

        dest = os.path.join(
            os.path.expanduser("~"), "Downloads", "mihoyo_launcher_setup.exe"
        )
        if not download_with_progress(WIN_LAUNCHER_URL, dest):
            print("正在打开官方下载页面作为备用...")
            webbrowser.open(WEB_URL)
            input("按回车键退出...")
            return

        print()
        input("按回车键开始静默安装（或 Ctrl+C 取消）...")

        if install_launcher_silent(dest):
            launcher = find_launcher()
            if launcher:
                print(f"\n启动器路径: {launcher}")
                print()
                print("=" * 50)
                print("  正在打开米哈游启动器...")
                print("=" * 50)
                print()
                print("请在启动器中：")
                print("  1. 登录你的米哈游账号")
                print("  2. 在原神右侧点击「下载」")
                print("  3. 等待游戏下载完成（约 70GB+）")
                os.startfile(launcher)
            else:
                print("\n启动器可能已安装到其他位置，请检查开始菜单。")

            cleanup = input("\n是否删除安装包以释放空间？(Y/n): ").strip().lower()
            if cleanup != "n":
                try:
                    os.remove(dest)
                    print("已删除安装包。")
                except Exception:
                    pass
        else:
            print("静默安装失败，正在手动打开安装包...")
            os.startfile(dest)

    else:
        # macOS: 检查是否已安装
        mac_paths = [
            "/Applications/Genshin Impact.app",
            "/Applications/YuanShen.app",
            os.path.expanduser("~/Applications/Genshin Impact.app"),
        ]
        found = False
        for p in mac_paths:
            if os.path.exists(p):
                print(f"[√] 检测到原神已安装: {p}")
                print("正在启动原神...")
                subprocess.run(["open", p])
                found = True
                break

        if not found:
            print("未检测到原神，正在打开官方下载页面...")
            webbrowser.open("https://ys.mihoyo.com/main/")
            print("macOS 用户推荐使用「云·原神」或 Mac App Store 版本。")

    print()
    input("按回车键退出...")
    sys.exit(0)


if __name__ == "__main__":
    main()
