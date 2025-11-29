import json
import os
import sys
import subprocess
from datetime import date

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------


def parse_map_string(env_string: str) -> dict:
    """Convert '20251128=20251126;20251129=20251126' into a dict."""
    mapping = {}
    pairs = env_string.split(";")

    for p in pairs:
        p = p.strip()
        if not p or "=" not in p:
            continue
        key, val = p.split("=", 1)
        key = key.strip()
        val = val.strip()

        if len(key) == 8 and key.isdigit() and len(val) == 8 and val.isdigit():
            mapping[key] = val

    return mapping


def dict_to_env_string(mapping: dict) -> str:
    """Convert dict back to 'k=v;k=v;k=v'."""
    parts = []
    for k, v in mapping.items():
        parts.append(f"{k}={v}")
    return ";".join(parts)


def load_json_as_dict(path: str) -> dict:
    """Load a JSON of YYYYMMDD: YYYYMMDD pairs."""
    if not os.path.isfile(path):
        print(f"[ERROR] JSON file not found: {path}")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Invalid JSON: {e}")
        sys.exit(1)

    # Validate structure
    final = {}
    for k, v in data.items():
        if (isinstance(k, str) and len(k) == 8 and k.isdigit()
                and isinstance(v, str) and len(v) == 8 and v.isdigit()):
            final[k] = v
        else:
            print(f"[WARN] Skipping invalid pair: {k}: {v}")

    return final


def set_env(name: str, value: str):
    """Persist an env var via setx."""
    result = subprocess.run(
        ["setx", name, value],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[ERROR] setx {name} failed:")
        print(result.stderr.strip())
        sys.exit(result.returncode)


# -------------------------------------------------------
# Main Logic
# -------------------------------------------------------


def main():
    args = sys.argv[1:]

    # --------------------------------------------
    # MODE 1: Update the date_map env var
    # --------------------------------------------
    if len(args) == 2 and args[0] == "--update-date-map":
        new_json = args[1]

        print(f"[INFO] Loading new date map from: {new_json}")
        mapping = load_json_as_dict(new_json)

        env_string = dict_to_env_string(mapping)
        print(f"[INFO] New date_map value:\n{env_string}")

        set_env("date_map", env_string)
        print("[INFO] date_map updated successfully.")
        print("[INFO] Open a NEW CMD window to see updated vars.")
        return

    # --------------------------------------------
    # MODE 2: Manual override
    # --------------------------------------------
    if len(args) == 2 and args[0] == "--date":
        override = args[1]

        if len(override) != 8 or not override.isdigit():
            print("[ERROR] --date must be YYYYMMDD")
            sys.exit(2)

        print(f"[INFO] Setting evaluation_date = {override}")
        set_env("evaluation_date", override)
        print("[INFO] Done.")
        return

    # --------------------------------------------
    # MODE 3: Standard daily lookup
    # --------------------------------------------
    raw_map = os.environ.get("date_map")
    if not raw_map:
        print("[ERROR] Env var 'date_map' is not set.")
        sys.exit(1)

    mapping = parse_map_string(raw_map)

    today = date.today().strftime("%Y%m%d")

    if today not in mapping:
        print(f"[ERROR] No mapping for today's date: {today}")
        sys.exit(3)

    final_value = mapping[today]

    print(f"[INFO] Today: {today}, evaluation_date → {final_value}")
    set_env("evaluation_date", final_value)
    print("[INFO] Done.")
    print("[INFO] Open a NEW CMD to see evaluation_date.")


if __name__ == "__main__":
    main()
