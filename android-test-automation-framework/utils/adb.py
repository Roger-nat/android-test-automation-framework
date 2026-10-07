from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass
class ADBResult:
    returncode: int
    stdout: str
    stderr: str


def run_adb(*args: str, timeout: int = 30) -> ADBResult:
    completed = subprocess.run(
        ["adb", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return ADBResult(
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def devices() -> list[str]:
    result = run_adb("devices")
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "ADB command failed.")

    lines = result.stdout.splitlines()[1:]
    return [line.split("\t")[0] for line in lines if "\tdevice" in line]


def install_apk(apk_path: str) -> ADBResult:
    return run_adb("install", "-r", apk_path, timeout=90)


def uninstall_package(package_name: str) -> ADBResult:
    return run_adb("uninstall", package_name, timeout=60)


def clear_app_data(package_name: str) -> ADBResult:
    return run_adb("shell", "pm", "clear", package_name, timeout=30)


def force_stop(package_name: str) -> ADBResult:
    return run_adb("shell", "am", "force-stop", package_name, timeout=30)


def device_model() -> str:
    result = run_adb("shell", "getprop", "ro.product.model")
    return result.stdout


def android_version() -> str:
    result = run_adb("shell", "getprop", "ro.build.version.release")
    return result.stdout


if __name__ == "__main__":
    print("Connected devices:", devices())
    print("Model:", device_model())
    print("Android:", android_version())
