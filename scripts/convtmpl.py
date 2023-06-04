"""Convert this template repo to a named Python project.

This file deletes itself after it has successfully executed.

Requires a single argument, the name of the Python project we will use.
This name must be a valid Python symbol.

Put any value as a second argument to stop this file from self deleting.
"""


import re
import os
import sys


try:
    NEW_NAME = sys.argv[1]
except IndexError:
    print("Must specify a project name (make sure the name is a valid python symbol)!")
    sys.exit(1)

NAME_RE = re.compile(r"\{\{NAME\}\}")
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def delete_self():
    """Delete this file."""

    os.remove(os.path.abspath(__file__))


def rename_package():
    """Rename the folder `src/{{NAME}}`."""

    old_dir_name = "src/{{NAME}}"
    old_dir = os.path.join(PARENT_DIR, old_dir_name)
    new_dir_name = NAME_RE.sub(NEW_NAME, old_dir_name)
    new_dir = os.path.join(PARENT_DIR, new_dir_name)

    try:
        os.rename(old_dir, new_dir)
    except OSError as e:
        print(f"Unable to rename the src dir: {e}")
        sys.exit(1)

def replace_names():
    """Walk __file__'s parent dir and replace all instances of `{{NAME}}`.

    Uses this script's loaded `NEW_NAME` variable for the replacement.
    """

    for dpath, _, fnames in os.walk(PARENT_DIR):
        if (".git" not in dpath) or ("scripts" not in dpath):
            for fname in fnames:
                fullpath = os.path.join(dpath, fname)
                try:
                    with open(fname, "r") as fd:
                        fdata = fd.read()
                    with open(fname, "w") as fd:
                        fd.write(NAME_RE.sub(NEW_NAME, fdata))
                except (IOError, re.error) as e:
                    print(
                        f"Unable to rename values in {fullpath}: {e}"
                    )

if __name__ == "__main__":
    try:
        rename_package()
        replace_names()
    except Exception as err:
        raise err

    # If everything went well, delete this script if there was no 2nd arg.
    try:
        sys.argv[2]
    except KeyError:
        delete_self()
