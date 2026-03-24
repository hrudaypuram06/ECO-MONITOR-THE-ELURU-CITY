import os
import streamlit

st_path = os.path.dirname(streamlit.__file__)
print(f"Searching in: {st_path}")

for root, dirs, files in os.walk(st_path):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    if "def get_script_run_context" in f.read():
                        relative_path = os.path.relpath(path, st_path)
                        print(f"Found definition in: streamlit.{relative_path.replace(os.sep, '.')[:-3]}")
            except Exception:
                pass
