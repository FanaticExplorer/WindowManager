from pywinauto import Desktop, Application
import psutil
import argparse
import sys
from prettytable import PrettyTable
from pathlib import Path


def get_process_name(pid):
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def is_valid_window(window):
    return (
            window.is_visible()
            and window.window_text()
            and window.control_count()
    )


def find_window(title=None, process_name=None, pid=None):
    if not title and not process_name and not pid:
        return None

    for window in Desktop(backend="uia").windows():
        if not is_valid_window(window):
            continue

        current_pid = window.process_id()
        current_process = get_process_name(current_pid)

        # Check matches
        title_match = title and title.lower() in window.window_text().lower()
        process_match = process_name and current_process and process_name.lower() in current_process.lower()
        pid_match = pid and pid == current_pid

        if title_match or process_match or pid_match:
            return window
    return None


def check_window_state(title=None, process_name=None, pid=None, check_exists=False, check_minimized=False,
                       verbose=False):
    window = find_window(title, process_name, pid)
    if window:
        if verbose:
            print(f"Window - Title: '{window.window_text()}'")
            print(f"Process: {get_process_name(window.process_id()) or 'Unknown'} (PID: {window.process_id()})")
        if check_minimized:
            print(f"Minimized: {'Yes' if window.is_minimized() else 'No'}")

        if check_exists:
            return True
        elif check_minimized:
            return window.is_minimized()
    return False


def get_window(title=None, process_name=None, pid=None, verbose=False):
    window = find_window(title, process_name, pid)
    if not window:
        print(f"No matching window found (Title: '{title}', Process: '{process_name}', PID: {pid})")
        return None

    window_text = window.window_text()
    process = get_process_name(window.process_id()) or "Unknown Process"

    if verbose:
        print(f"Found window: '{window_text}'")
        print(f"Process: {process} (PID: {window.process_id()})")

    return window


def close_window(title=None, process_name=None, pid=None, verbose=False):
    window = get_window(title, process_name, pid, verbose)
    if window:
        print(f"Closing: '{window.window_text()}'...")
        window.close()
        return True
    return False


def minimize_window(title=None, process_name=None, pid=None, verbose=False):
    window = get_window(title, process_name, pid, verbose)
    if window:
        print(f"Minimizing: '{window.window_text()}'...")
        try:
            # Try multiple methods to ensure minimization works
            if not window.is_minimized():
                # Method 1: Direct minimize
                try:
                    window.minimize()
                    if window.is_minimized():
                        return True
                except:
                    pass

                # Method 2: Use Application object
                try:
                    app = Application(backend="uia").connect(process=window.process_id())
                    top_window = app.window(title=window.window_text())
                    top_window.minimize()
                    if window.is_minimized():
                        return True
                except:
                    pass

                # Method 3: Use win32 API as fallback
                try:
                    import win32gui
                    win32gui.ShowWindow(window.handle, 6)  # SW_MINIMIZE = 6
                    if window.is_minimized():
                        return True
                except:
                    pass

            return window.is_minimized()
        except Exception as e:
            print(f"Failed to minimize window: {e}")
            return False
    return False


def focus_window(title=None, process_name=None, pid=None, verbose=False):
    window = get_window(title, process_name, pid, verbose)
    if window:
        print(f"Focusing: '{window.window_text()}'...")
        try:
            if window.is_minimized():
                window.restore()
            window.set_focus()
            return True
        except Exception as e:
            print(f"Failed to focus window: {e}")
    return False


def list_windows():
    print("\nActive windows:")

    # Create a PrettyTable with appropriate columns
    table = PrettyTable()
    table.field_names = ["PID", "Process", "Window Title", "Minimized"]

    # Set alignment for each column
    table.align["PID"] = "r"
    table.align["Process"] = "l"
    table.align["Window Title"] = "l"
    table.align["Minimized"] = "c"

    # Add rows for each valid window
    for i, window in enumerate(Desktop(backend="uia").windows()):
        if not is_valid_window(window):
            continue

        process = get_process_name(window.process_id()) or "Unknown"
        table.add_row([
            window.process_id(),
            process,
            window.window_text()[:70] + ("..." if len(window.window_text()) > 70 else ""),
            "Yes" if window.is_minimized() else "No"
        ])

    # Print the table
    print(table)


def main():
    filename = Path(sys.argv[0]).name
    parser = argparse.ArgumentParser(
        description="WindowManager - Manage your windows user-like",
        epilog="Examples:\n"
               f"  {filename} -t 'Notepad'\n"
               f"  {filename} --pid 1234\n"
               f"  {filename} -e -p 'chrome'\n"
               f"  {filename} -m -t 'Calculator'\n"
               f"  {filename} -z -t 'Calculator'\n"
               f"  {filename} -f -t 'Document'",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Search parameters
    parser.add_argument("-t", "--title", help="Partial window title to match")
    parser.add_argument("-p", "--process", help="Partial process name to match")
    parser.add_argument("--pid", type=int, help="Process ID to match")

    # Actions
    parser.add_argument("-l", "--list", action="store_true", help="List all open windows")
    parser.add_argument("-m", "--minimize", action="store_true",
                        help="Minimize the window")
    parser.add_argument("-e", "--exists", action="store_true",
                        help="Check if window exists")
    parser.add_argument("-z", "--minimized", action="store_true",
                        help="Check if window is minimized")
    parser.add_argument("-f", "--focus", action="store_true",
                        help="Focus the window (bring to front and restore if minimized)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed info")

    args = parser.parse_args()

    if args.list:
        list_windows()
    elif args.exists:
        exists = check_window_state(args.title, args.process, args.pid, check_exists=True, verbose=args.verbose)
        sys.exit(0 if exists else 1)
    elif args.minimized:
        is_min = check_window_state(args.title, args.process, args.pid, check_minimized=True, verbose=args.verbose)
        sys.exit(0 if is_min else 1)
    elif args.minimize:
        success = minimize_window(args.title, args.process, args.pid, args.verbose)
        sys.exit(0 if success else 1)
    elif args.focus:
        success = focus_window(args.title, args.process, args.pid, args.verbose)
        sys.exit(0 if success else 1)
    elif args.title or args.process or args.pid:
        success = close_window(args.title, args.process, args.pid, args.verbose)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()