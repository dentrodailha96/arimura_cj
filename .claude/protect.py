import json
import sys

input_data = json.load(sys.stdin)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Files to protect
protected = [".env", ".gitignore", ".env.dev", ".env.prod"]

# Check all input values for protected filenames
input_str = json.dumps(tool_input)
for f in protected:
    if f in input_str:
        print(json.dumps({
            "action": "block",
            "message": f"🚫 Blocked: Claude is not allowed to access {f}"
        }))
        sys.exit(0)

# Allow everything else
print(json.dumps({"action": "allow"}))
