import os
import sys
import traceback
import uvicorn

try:
    from server.app import app as fastapi_app
except Exception as _e:
    fastapi_app = None


def _app_root() -> str:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    root = os.path.join(base, "library-management-system")
    os.makedirs(root, exist_ok=True)
    return root


def _log_exception(e: Exception) -> None:
    try:
        root = _app_root()
        log_path = os.path.join(root, "run.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"Unhandled Exception: {traceback.format_exc()}")
    except Exception:
        print("Failed to write log:", traceback.format_exc())


def main():
    is_frozen = getattr(sys, "frozen", False)

    if fastapi_app is None:
        _log_exception(RuntimeError("Failed to import server.app:app"))
        print("Failed to import FastAPI app (server.app:app).")
        if is_frozen:
            input("Press Enter to exit...")
        sys.exit(1)

    for port in (8000, 8001, 8002, 8003, 8004, 8005):
        try:
            print(f"Starting server on http://127.0.0.1:{port}")
            uvicorn.run(fastapi_app, host="127.0.0.1", port=port, reload=not is_frozen)
            return
        except OSError as e:
            if getattr(e, "errno", None) is not None:
                print(f"Port {port} failed: {e}")
                continue
            else:
                _log_exception(e)
                if is_frozen:
                    input("An error occurred. Press Enter to exit...")
                raise
        except Exception as e:
            _log_exception(e)
            if is_frozen:
                input("An error occurred. Press Enter to exit...")
            raise
    print("Unable to start server on ports 8000-8005.")
    if is_frozen:
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
