import sys
from cx_Freeze import setup, Executable


data_files = [
    "templates/",
    "static/"
]

build_exe_options = {
    "excludes": ["tkinter", "unittest"],
    "zip_include_packages": ["encodings", "PySide6"],
    "includes": ["pandas", "flask", "jinja2.ext", "jinja2", "pathlib"],
    "include_files": data_files
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Mocean Billing",
    version="0.1",
    description="Mocean GUI App",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", base=base)],
)
