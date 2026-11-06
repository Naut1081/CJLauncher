import minecraft_launcher_lib
import subprocess
import os
import sys

MINECRAFT_DIRECTORY = minecraft_launcher_lib.utils.get_minecraft_directory()


def cj_splash():
    """Display the CJ Launcher splash screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[96m" + "=" * 50 + "\033[0m")
    print("\033[96m" + "   _____ _   _     _                    _               " + "\033[0m")
    print("\033[96m" + "  / ____| | | |   | |                  | |              " + "\033[0m")
    print("\033[96m" + " | |    | |_| |__ | |     __ _ _   _  _| |_ ___  _ __   " + "\033[0m")
    print("\033[96m" + " | |    | __| '_ \\| |    / _` | | | |/ _` |/ _ \\| '__|  " + "\033[0m")
    print("\033[96m" + " | |____| |_| | | | |___| (_| | |_| | (_| | (_) | |     " + "\033[0m")
    print("\033[96m" + "  \\_____|\\__|_| |_|______\\__,_|\\__,_|\\__,_|\\___/|_|     " + "\033[0m")
    print("\033[96m" + "=" * 50 + "\033[0m")
    print(f"  [ Game Directory: {MINECRAFT_DIRECTORY} ]")
    print("\033[96m" + "=" * 50 + "\n" + "\033[0m")


def get_release_versions():
    """Fetch the newest release versions from Mojang."""
    print("Fetching available versions from Mojang...")
    versions = minecraft_launcher_lib.utils.get_available_versions()
    releases = versions.get("release", [])
    release_ids = [entry["id"] for entry in releases if isinstance(entry, dict) and "id" in entry]
    return release_ids[:10]


def safe_install_jvm_runtime(minecraft_dir, version_id):
    """Attempt JVM install with the current call signature."""
    methods = [
        (minecraft_launcher_lib.runtime.install_jvm_runtime, (minecraft_dir, version_id)),
        (minecraft_launcher_lib.runtime.install_jvm_runtime, (version_id, minecraft_dir)),
    ]

    for func, args in methods:
        try:
            func(*args)
            return True
        except TypeError:
            continue
        except Exception:
            continue
    return False


def install_and_launch(version_id, username):
    """Download the selected Minecraft version and launch it."""
    installed_versions = minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIRECTORY)
    installed_ids = [entry["id"] for entry in installed_versions if isinstance(entry, dict) and "id" in entry]

    if version_id not in installed_ids:
        print(f"\n[!] Version {version_id} is not installed. Downloading now...")
        try:
            def download_progress(current, total):
                if total <= 0:
                    return
                percent = int((current / total) * 100)
                bar = "█" * (percent // 2) + "-" * (50 - (percent // 2))
                sys.stdout.write(f"\r[{bar}] {percent}%")
                sys.stdout.flush()

            minecraft_launcher_lib.install.install_minecraft_version(
                version_id,
                MINECRAFT_DIRECTORY,
                callback={
                    "setStatus": lambda status: sys.stdout.write(f"\r[Status] {status}..."),
                    "setProgress": download_progress,
                },
            )
            print("\n[+] Game download complete!")
        except Exception as exc:
            print(f"\n[!] Installation failed: {exc}")
            return
    else:
        print(f"\n[+] Version {version_id} is already installed.")

    print("\n[+] Checking Java Runtime...")
    try:
        if not safe_install_jvm_runtime(MINECRAFT_DIRECTORY, version_id):
            print("[!] JVM install was not available through the expected API.")
            print("Will try to use the system Java runtime if available.")
        else:
            print("[+] Java is ready!")
    except Exception as exc:
        print(f"[!] Java download failed: {exc}")
        print("Will try to use system Java instead.")

    print(f"\n[+] Preparing to launch Minecraft {version_id}...")
    options = {
        "username": username,
        "uuid": "",
        "token": "",
        "jvmArguments": ["-Xmx4G", "-Xms2G"],
        "launcherName": "CJ Launcher",
        "launcherVersion": "1.0",
    }

    try:
        command = minecraft_launcher_lib.command.get_minecraft_command(
            version_id,
            MINECRAFT_DIRECTORY,
            options,
        )

        if not command:
            raise RuntimeError("Minecraft command generation returned an empty command list.")

        print("[+] CJ Launcher is launching the game! Have fun!\n")
        subprocess.run(command, cwd=MINECRAFT_DIRECTORY, check=False)
    except Exception as exc:
        print(f"\n[!] Failed to launch: {exc}")
        print("Make sure Java is installed and that you have enough RAM.")


def main():
    cj_splash()

    username = input("Enter your username (Offline Mode): ").strip()
    if not username:
        username = "CJ_Player"
        print(f"Using default username: {username}")

    versions = get_release_versions()
    if not versions:
        print("Could not fetch Minecraft versions. Please try again later.")
        return

    print("\nSelect a Minecraft version to launch:")
    for index, version_id in enumerate(versions):
        print(f"  [{index + 1}] {version_id}")

    choice = input(f"\nEnter choice (1-{len(versions)}) or press Enter for latest: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(versions):
        version_id = versions[int(choice) - 1]
    else:
        version_id = versions[0]

    install_and_launch(version_id, username)
    input("\nPress Enter to exit CJ Launcher...")


if __name__ == "__main__":
    main()
