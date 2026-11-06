import minecraft_launcher_lib
import os
import subprocess
import sys

MINECRAFT_DIRECTORY = minecraft_launcher_lib.utils.get_minecraft_directory()


def cj_splash():
    """Display the CJ Launcher splash screen."""
    os.system("cls" if os.name == "nt" else "clear")
    cyan = "\033[96m"
    reset = "\033[0m"
    print(cyan + "=" * 50 + reset)
    print(cyan + "   _____ _   _     _                    _               " + reset)
    print(cyan + "  / ____| | | |   | |                  | |              " + reset)
    print(cyan + " | |    | |_| |__ | |     __ _ _   _  _| |_ ___  _ __   " + reset)
    print(cyan + " | |    | __| '_ \\| |    / _` | | | |/ _` |/ _ \\| '__|  " + reset)
    print(cyan + " | |____| |_| | | | |___| (_| | |_| | (_| | (_) | |     " + reset)
    print(cyan + "  \\_____|\\__|_| |_|______\\__,_|\\__,_|\\__,_|\\___/|_|     " + reset)
    print(cyan + "=" * 50 + reset)
    print(f"  [ Game Directory: {MINECRAFT_DIRECTORY} ]")
    print(cyan + "=" * 50 + "\n" + reset)


def get_release_versions():
    """Return the ten newest Minecraft releases from the version manifest."""
    print("Fetching available versions from Mojang...")
    versions = minecraft_launcher_lib.utils.get_available_versions()
    releases = versions.get("release", [])
    return [entry["id"] for entry in releases if isinstance(entry, dict) and "id" in entry][:10]


def show_progress(current, total):
    """Display download progress; callbacks provide current and max separately."""
    if total <= 0:
        return
    percent = min(100, int(current * 100 / total))
    filled = percent // 2
    bar = "█" * filled + "-" * (50 - filled)
    sys.stdout.write(f"\r[{bar}] {percent}%")
    sys.stdout.flush()


def install_and_launch(version_id, username):
    """Install or repair a Minecraft version and then launch it."""
    print(f"\n[+] Installing/checking Minecraft {version_id} and its required files...")
    try:
        # This verifies/repairs existing installs and also installs the JVM
        # component specified by the selected version's metadata.
        minecraft_launcher_lib.install.install_minecraft_version(
            version_id,
            MINECRAFT_DIRECTORY,
            callback={
                "setStatus": lambda status: print(f"\n[Status] {status}"),
                "setProgress": show_progress,
                "setMax": lambda total: None,
            },
        )
        print("\n[+] Minecraft files and required runtime are ready.")
    except Exception as exc:
        print(f"\n[!] Installation/check failed: {exc}")
        return

    options = {
        "username": username,
        # Offline identity is suitable for local play only. It does not
        # authenticate access to online-mode servers or Minecraft Realms.
        "uuid": "",
        "token": "",
        "jvmArguments": ["-Xms1G", "-Xmx4G"],
        "launcherName": "CJ Launcher",
        "launcherVersion": "1.0",
    }

    try:
        command = minecraft_launcher_lib.command.get_minecraft_command(
            version_id,
            MINECRAFT_DIRECTORY,
            options,
        )
        print(f"\n[+] Launching Minecraft {version_id}...\n")
        result = subprocess.run(command, cwd=MINECRAFT_DIRECTORY, check=False)
        if result.returncode != 0:
            print(f"[!] Minecraft exited with code {result.returncode}.")
    except Exception as exc:
        print(f"\n[!] Failed to launch: {exc}")
        print("Check the Java/runtime installation and available memory.")


def main():
    cj_splash()

    username = input("Enter your username (Offline Mode): ").strip() or "CJ_Player"
    if not username.replace("_", "").isalnum() or not 3 <= len(username) <= 16:
        print("Username must be 3–16 characters and contain only letters, numbers, or underscores.")
        return

    try:
        versions = get_release_versions()
    except Exception as exc:
        print(f"Could not fetch Minecraft versions: {exc}")
        input("Press Enter to exit CJ Launcher...")
        return

    if not versions:
        print("Could not find any Minecraft release versions. Please try again later.")
        input("Press Enter to exit CJ Launcher...")
        return

    print("\nSelect a Minecraft version to launch:")
    for index, version_id in enumerate(versions, start=1):
        print(f"  [{index}] {version_id}")

    choice = input(f"\nEnter choice (1-{len(versions)}) or press Enter for latest: ").strip()
    version_id = versions[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= len(versions) else versions[0]

    install_and_launch(version_id, username)
    input("\nPress Enter to exit CJ Launcher...")


if __name__ == "__main__":
    main()
