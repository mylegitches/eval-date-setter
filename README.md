# `update_eval_date.py` — Daily Evaluation Date Environment Manager

This script manages two persistent Windows environment variables:

- **`date_map`** — A semicolon-delimited list of `YYYYMMDD=YYYYMMDD` mappings.
- **`evaluation_date`** — A single `YYYYMMDD` date used by your automations.

It supports automatic daily updates, manual overrides, and replacing the entire date map using a JSON file.

---

## 🚀 Purpose

The script updates the environment variable **`evaluation_date`** based on a lookup table stored in the environment variable **`date_map`**.

It works in three modes:

1. **Normal mode** — get today’s date → look it up in `date_map` → update `evaluation_date`.
2. **Override mode** — manually set `evaluation_date` to any `YYYYMMDD` value.
3. **Map update mode** — read a JSON file (your original format) and replace `date_map`.

---

## 📦 Format of `date_map`

`date_map` must be a **single environment variable** with the format:

```
YYYYMMDD=YYYYMMDD;YYYYMMDD=YYYYMMDD;YYYYMMDD=YYYYMMDD
```

Example:

```
setx date_map "20251121=20251120;20251122=20251121;20251123=20251121"
```

- No spaces
- Semicolons separate pairs
- Keys and values are always `YYYYMMDD`

---

## 📄 JSON Format for Updating `date_map`

When using `--update-date-map`, your JSON file must match the format:

```json
{
  "20251121": "20251120",
  "20251122": "20251121",
  "20251123": "20251121"
}
```

This is the same structure as the JSON file you originally uploaded.

---

## 🧠 Script Usage

### ✅ A) Normal operation (daily)

Reads today’s date → looks it up in `date_map` → updates `evaluation_date`:

```
python update_eval_date.py
```

Example result:

```
evaluation_date = 20251126
```

---

### ✳️ B) Manual override (skip date_map completely)

```
python update_eval_date.py --date 20251124
```

Directly sets:

```
evaluation_date = 20251124
```

---

### 🔄 C) Replace the entire `date_map` using a JSON file

```
python update_eval_date.py --update-date-map my_new_dates.json
```

This will:

1. Load `my_new_dates.json`
2. Validate each `YYYYMMDD: YYYYMMDD`
3. Convert it into `k=v;k=v;...` format
4. Update the persistent environment variable:

```
date_map="20251121=20251120;20251122=20251121;20251123=20251121"
```

---

## 🧪 Verifying Values (IMPORTANT)

After running any update command, open a **NEW CMD window** before checking:

```
echo %date_map%
echo %evaluation_date%
```

Windows does not update env vars in existing terminals.

---

## ⏱️ Scheduling (Optional but Recommended)

You can make this automatic with Task Scheduler:

1. Open **Task Scheduler**
2. Create a task
3. Trigger: **Daily**
4. Action:
   ```
   Program: python
   Arguments: "C:\path\to\update_eval_date.py"
   ```

Now `evaluation_date` always stays current.

---

## 📝 Summary

- `date_map` holds all date relationships.
- `evaluation_date` holds the resolved date for today.
- The script supports:
  - Daily updates
  - Manual overrides
  - Replacing the map via JSON
- Everything stays in strict `YYYYMMDD` format.
- No external dependencies beyond Python.
