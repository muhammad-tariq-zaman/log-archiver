"""Log archiver: gzip-compress log files older than N days."""
import argparse
import gzip
import os
import shutil
import sys
import time


def find_old(directory, days, pattern=".log"):
    cutoff = time.time() - days * 86400
    found = []
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if os.path.isfile(path) and name.endswith(pattern) and os.path.getmtime(path) < cutoff:
            found.append(path)
    return found


def archive(paths, delete_original=False, dry_run=True):
    done = []
    for path in paths:
        dest = path + ".gz"
        if dry_run:
            done.append((path, dest, "would-archive"))
            continue
        with open(path, "rb") as src, gzip.open(dest, "wb") as out:
            shutil.copyfileobj(src, out)
        if delete_original:
            os.remove(path)
        done.append((path, dest, "archived"))
    return done


def main(argv=None):
    p = argparse.ArgumentParser(description="Gzip logs older than N days.")
    p.add_argument("--dir", required=True)
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--delete-original", action="store_true")
    p.add_argument("--apply", action="store_true", help="actually archive (default is dry-run)")
    args = p.parse_args(argv)
    for src, dest, action in archive(find_old(args.dir, args.days),
                                     args.delete_original, dry_run=not args.apply):
        print(f"{action}: {src} -> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
