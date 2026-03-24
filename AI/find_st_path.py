import os
import streamlit

# Get the path to the streamlit package
st_path = os.path.dirname(streamlit.__file__)
print(f"Searching for 'get_script_run_context' in: {st_path}")

matches = []
for root, dirs, files in os.walk(st_path):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "get_script_run_context" in content:
                        # Convert full path to streamlit.module relative path
                        rel = os.path.relpath(full_path, st_path)
                        mod = "streamlit." + rel.replace(os.sep, ".").replace(".py", "").replace(".__init__", "")
                        matches.append(mod)
            except Exception:
                pass

if matches:
    print("\nMatches found in:")
    for m in matches:
        print(f" - {m}")
else:
    print("\nNo matches' found.")
