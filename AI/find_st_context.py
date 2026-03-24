import streamlit
import pkgutil
import warnings
import importlib

# Suppress warnings
warnings.filterwarnings("ignore")

found = False

for loader, name, ispkg in pkgutil.walk_packages(streamlit.__path__, "streamlit."):
    try:
        module = importlib.import_module(name)
        if hasattr(module, "get_script_run_context"):
            print(f"Found get_script_run_context in: {name}")
            found = True
    except Exception:
        pass

if not found:
    print("Could not find get_script_run_context in any streamlit submodules.")