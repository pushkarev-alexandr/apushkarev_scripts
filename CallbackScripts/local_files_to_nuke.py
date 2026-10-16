# Copies local Read files and sequences to _local_files near the network script,
# preferring the precomp folder, then materials, then the script directory.

# v1.1.0
# created by: Pushkarev Aleksandr

# changelog:
# v1.1.0 collect on script save; log per-copy duration and total save callback delay; warn once per session for missing sources, without tracebacks
# v1.0.0 initial release: copies files and all sequence frames on Read creation and file changes; skips local/unsaved scripts; writes rotating per-user logs

from datetime import datetime
import getpass
import logging
from logging.handlers import RotatingFileHandler
import ntpath
import os
import re
import shutil
import socket
import tempfile
import time

import nuke


_installed = False
_processing = False
_warned_missing = set()
IMPORT_FOLDER = "_local_files"
FRAME_TOKEN = re.compile(r"#+|%\d*d")
logger = logging.getLogger("local_files_to_nuke")
logger.propagate = False
logger.addHandler(logging.NullHandler())
LOG_PATH = None


class MissingSourceError(FileNotFoundError):
    """An unavailable source, distinct from a missing destination directory."""


class DiagnosticFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(record.created).astimezone().isoformat(timespec="seconds")


class DiagnosticFileHandler(RotatingFileHandler):
    def handleError(self, record):
        # Logging failures must not print to the console or interrupt Nuke.
        pass


def setup_logging():
    """One rotating file per user, accepting rare concurrent rotation conflicts."""
    global LOG_PATH
    if LOG_PATH is not None:
        return
    user = getpass.getuser()
    computer = socket.gethostname()
    filename = "{}.log".format(user)
    filename = re.sub(r'[^\w.\-]', '_', filename)
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    try:
        os.makedirs(directory, exist_ok=True)
        log_path = os.path.join(directory, filename)
        handler = DiagnosticFileHandler(
            log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
    except OSError:
        # Keep the plugin usable if its log directory cannot be written.
        return
    handler.setFormatter(DiagnosticFormatter(
        "%(asctime)s %(levelname)s user=%(user)s computer=%(computer)s pid=%(process)d %(message)s"
    ))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    LOG_PATH = log_path
    # Include identity on every record, including exception records.
    handler.addFilter(IdentityFilter(user, computer))


class IdentityFilter(logging.Filter):
    def __init__(self, user, computer):
        super().__init__()
        self.user = user
        self.computer = computer

    def filter(self, record):
        record.user = self.user
        record.computer = self.computer
        return True


def classify_path(path):
    """Classify the raw path without evaluating expressions or accessing files.

    Frame placeholders such as #### and %04d are ordinary path components.
    C/D/E are local; X/Y/Z are network drives. Other letters remain unclassified.
    """
    if not path:
        return "empty"
    if "[" in path or "]" in path or "$" in path or re.search(r"%[A-Za-z_][A-Za-z0-9_]*%", path):
        return "expression"

    normalized = path.replace("\\", "/")
    # Windows device paths are not ordinary UNC shares.
    if normalized.startswith(("//?/", "//./")):
        return "other_absolute"
    drive, tail = ntpath.splitdrive(normalized)
    if drive.startswith("//") and tail.startswith("/"):
        return "network"
    if drive and tail.startswith("/"):
        if drive.upper() in ("C:", "D:", "E:"):
            return "local"
        if drive.upper() in ("X:", "Y:", "Z:"):
            return "network"
        return "other_absolute"
    if normalized.startswith("/"):
        return "other_absolute"
    return "relative"


def get_destination_root(script_path):
    """Prefer precomp, then materials beside the script directory."""
    script_directory = ntpath.dirname(script_path)
    parent_directory = ntpath.dirname(script_directory)
    for name in ("precomp", "materials"):
        candidate = ntpath.join(parent_directory, name)
        if os.path.isdir(candidate):
            return ntpath.join(candidate, IMPORT_FOLDER)
    return ntpath.join(script_directory, IMPORT_FOLDER)


def copy_single_file(source, destination_root):
    """Use a unique folder to avoid overwriting files with the same name."""
    if not os.path.isfile(source):
        raise MissingSourceError("Source file does not exist: {}".format(source))
    folder = tempfile.mkdtemp(prefix="import_", dir=destination_root)
    destination = os.path.join(folder, ntpath.basename(source))
    shutil.copyfile(source, destination)
    return destination.replace("\\", "/")


def find_sequence_files(source):
    """Find every frame matching the basename, without using the Read range."""
    directory, basename = ntpath.split(source)
    tokens = list(FRAME_TOKEN.finditer(basename))
    if len(tokens) != 1:
        raise ValueError("Expected one frame placeholder in the filename")
    token = tokens[0]
    digits = r"[0-9]+"
    pattern = re.compile(
        re.escape(basename[:token.start()]) + digits
        + re.escape(basename[token.end():]), re.IGNORECASE
    )
    try:
        with os.scandir(directory) as entries:
            files = sorted(
                entry.path for entry in entries
                if entry.is_file() and pattern.fullmatch(entry.name)
            )
    except FileNotFoundError as exc:
        raise MissingSourceError("Sequence directory does not exist: {}".format(directory)) from exc
    if not files:
        raise MissingSourceError("No sequence frames found: {}".format(source))
    return files


def copy_sequence(source, destination_root, files=None):
    """Copy all matching frames to one folder and retain the original template."""
    if files is None:
        files = find_sequence_files(source)
    folder = tempfile.mkdtemp(prefix="import_", dir=destination_root)
    for file in files:
        shutil.copyfile(file, os.path.join(folder, ntpath.basename(file)))
    logger.info("Sequence copied: frames=%s source=%r destination=%r", len(files), source, folder)
    return os.path.join(folder, ntpath.basename(source)).replace("\\", "/")


def inspect_read(node, reason):
    """Copy local files/sequences; leave other paths unchanged."""
    global _processing
    if _processing:
        return "skipped"
    path = node["file"].value()
    path_type = classify_path(path)
    if path_type != "local":
        return "skipped"
    setup_logging()
    script_path = nuke.root().name()
    if classify_path(script_path) != "network":
        logger.info("Skipped: script is not saved on network; event=%s script=%r node=%s source=%r",
                    reason, script_path, node.fullName(), path)
        return "skipped"
    missing_key = (ntpath.normcase(ntpath.normpath(script_path)), node.fullName(),
                   ntpath.normcase(ntpath.normpath(path)))
    _processing = True
    started = time.perf_counter()
    try:
        # Validate before logging a copy attempt or touching the destination.
        is_sequence = bool(FRAME_TOKEN.search(ntpath.basename(path)))
        files = find_sequence_files(path) if is_sequence else None
        if not is_sequence:
            try:
                os.stat(path)
            except FileNotFoundError as exc:
                raise MissingSourceError("Source file does not exist: {}".format(path)) from exc
        logger.info("Copy started: event=%s script=%r node=%s source=%r",
                    reason, script_path, node.fullName(), path)
        destination_root = get_destination_root(script_path)
        os.makedirs(destination_root, exist_ok=True)
        if is_sequence:
            destination = copy_sequence(path, destination_root, files=files)
        else:
            destination = copy_single_file(path, destination_root)
        node["file"].setValue(destination)
        _warned_missing.discard(missing_key)
        logger.info("Copied: event=%s script=%r node=%s source=%r destination=%r duration_s=%.6f",
                    reason, script_path, node.fullName(), path, destination,
                    time.perf_counter() - started)
        return "copied"
    except MissingSourceError:
        if missing_key not in _warned_missing:
            logger.warning("Skipped: source missing; event=%s script=%r node=%s source=%r",
                           reason, script_path, node.fullName(), path)
            _warned_missing.add(missing_key)
        return "skipped"
    except Exception:
        logger.exception("Copy failed: event=%s script=%r node=%s source=%r duration_s=%.6f",
                         reason, script_path, node.fullName(), path,
                         time.perf_counter() - started)
        return "failed"
    finally:
        _processing = False


def on_script_save():
    """Collect local Reads and measure plugin delay, excluding .nk serialization."""
    if _processing:
        return
    started = time.perf_counter()
    counts = {"copied": 0, "skipped": 0, "failed": 0}
    scanned = 0
    scan_failed = False
    setup_logging()
    script_path = nuke.root().name()
    try:
        logger.info("Save scan started: event=script_save script=%r", script_path)
        for node in nuke.allNodes("Read"):
            scanned += 1
            try:
                result = inspect_read(node, "script_save")
            except Exception:
                # A malformed/deleted node must not prevent the remaining scan or save.
                counts["failed"] += 1
                logger.exception("Read inspection failed: event=script_save script=%r read_index=%s",
                                 script_path, scanned)
            else:
                counts[result] += 1
    except Exception:
        scan_failed = True
        logger.exception("Save scan failed: event=script_save script=%r", script_path)
    finally:
        logger.info(
            "Save scan finished: event=script_save script=%r duration_s=%.6f "
            "scanned=%s copied=%s skipped=%s failed=%s scan_failed=%s",
            script_path, time.perf_counter() - started, scanned,
            counts["copied"], counts["skipped"], counts["failed"], scan_failed,
        )


def on_read_on_create():
    """Observe Read creation, including imports, pastes and script loading."""
    inspect_read(nuke.thisNode(), "read_on_create")


def on_read_knob_changed():
    """Observe file selection, including the drag-and-drop path to test."""
    if nuke.thisKnob().name() == "file":
        inspect_read(nuke.thisNode(), "read_file_changed")


def install_callbacks():
    """Called by init.py; repeated calls do not duplicate callbacks."""
    global _installed
    if _installed:
        return
    nuke.addOnScriptSave(on_script_save)
    nuke.addOnCreate(on_read_on_create, nodeClass="Read")
    nuke.addKnobChanged(on_read_knob_changed, nodeClass="Read")
    _installed = True


def uninstall_callbacks():
    """Allow callbacks to be disabled during local testing."""
    global _installed
    if not _installed:
        return
    nuke.removeOnScriptSave(on_script_save)
    nuke.removeOnCreate(on_read_on_create, nodeClass="Read")
    nuke.removeKnobChanged(on_read_knob_changed, nodeClass="Read")
    _installed = False
