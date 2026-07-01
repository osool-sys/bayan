\
# Auto-selected native loader shim (no third-party deps)
import importlib.machinery, importlib.util, os, sys, pathlib, platform

_pkg_dir = pathlib.Path(__file__).parent
_cached = None
_DEBUG = os.environ.get("SITR_DEBUG", "")

def _log(msg):
    if _DEBUG:
        print(f"[sitr] {msg}", file=sys.stderr)

def _py_tag():
    v = sys.version_info
    return f"cp{v.major}{v.minor}"

def _arch_token():
    m = (platform.machine() or "").lower()
    if m in ("x86_64","amd64","x64"): return "x86_64"
    if m in ("aarch64","arm64"): return "aarch64"
    if m in ("i386","i686","x86"): return "i686"
    return m or "unknown"

def _windows_bits():
    return "win_amd64" if platform.architecture()[0].startswith("64") else "win32"

def _candidate_keys_for_this_runtime():
    py = _py_tag(); arch = _arch_token(); sysname = sys.platform
    if sysname.startswith("win"):
        yield f"{py}-{_windows_bits()}"; yield py; return
    if sysname == "darwin":
        for v in ("13_0","12_0","11_0","10_15","10_14","10_13","10_12","10_11","10_10","10_9"):
            yield f"{py}-macosx_{v}_{'arm64' if arch=='aarch64' else arch}"
        yield py; return
    if sysname.startswith("linux"):
        yield f"{py}-manylinux_{arch}"; yield f"{py}-musllinux_{arch}"; yield py; return
    yield py

def _pick_best_file(name_for_tag):
    py = _py_tag(); arch = _arch_token()
    for key in _candidate_keys_for_this_runtime():
        f = name_for_tag.get(key)
        if f: return f
    for k, f in name_for_tag.items():
        if k.startswith(f"{py}-manylinux_") and k.endswith(f"_{arch}"): return f
    for k, f in name_for_tag.items():
        if k.startswith(f"{py}-musllinux_") and k.endswith(f"_{arch}"): return f
    for k, f in name_for_tag.items():
        if k.startswith(f"{py}-macosx_") and k.split("_")[-1] in (arch, "arm64" if arch=="aarch64" else arch): return f
    return name_for_tag.get(py)

def _load_native():
    global _cached
    if _cached is not None: return _cached
    files = list(_pkg_dir.glob("sitry-*.*"))
    name_for_tag = {f.name.split("sitry-")[1].rsplit(".", 1)[0]: f for f in files}
    if _DEBUG: _log("available: " + ", ".join(sorted(name_for_tag.keys())))
    picked = _pick_best_file(name_for_tag)
    if not picked:
        raise ImportError("sitr: no compatible native loader found for this Python/OS/arch")
    if _DEBUG: _log(f"using {picked.name}")
    loader = importlib.machinery.ExtensionFileLoader("sitry", str(picked))
    spec = importlib.util.spec_from_file_location("sitry", str(picked), loader=loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    _cached = mod
    return mod

_native = _load_native()
install_encrypted_importer = getattr(_native, "install_encrypted_importer")
