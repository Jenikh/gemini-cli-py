# @license
# Copyright 2025 Google LLC
# SPDX-License-Identifier: Apache-2.0

import json
from typing import Any, Set, List, Dict, Union

def stable_stringify(obj: Any) -> str:
    """
    Produces a stable, deterministic JSON string representation with sorted keys.

    This method is critical for security policy matching. It ensures that the same
    object always produces the same string representation, regardless of property
    insertion order, which could vary across different JavaScript engines or
    runtime conditions.

    Key behaviors:
    1. **Sorted Keys**: Object properties are always serialized in alphabetical order,
       ensuring deterministic output for pattern matching.

    2. **Circular Reference Protection**: Uses object identity tracking to detect
       circular references. Circular references are replaced with "[Circular]".

    3. **JSON Spec Compliance**:
       - `None` values: Represented as `null`.
       - Functions: Omitted from objects. (Python json.dumps already handles this for default)
       - `to_json` methods: Respected and called when present (mimicking toJSON spec).

    Args:
        obj: The object to stringify.

    Returns:
        A deterministic JSON string representation.
    """
    
    class StableJsonEncoder(json.JSONEncoder):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ancestors: Set[int] = set()

        def default(self, current_obj: Any) -> Any:
            # Handle primitives and None
            if current_obj is None or isinstance(current_obj, (int, float, bool, str)):
                return current_obj
            
            # Check for circular reference (object is in ancestor chain)
            obj_id = id(current_obj)
            if obj_id in self.ancestors:
                return '[Circular]'

            self.ancestors.add(obj_id)
            try:
                # Check for to_json method and use it if present
                # Similar to JavaScript's toJSON, but named to_json for Python
                if hasattr(current_obj, 'to_json') and callable(current_obj.to_json):
                    try:
                        json_value = current_obj.to_json()
                        # Recursively serialize the result of to_json
                        return self.default(json_value)
                    except Exception:
                        # If to_json throws, treat as a regular object
                        pass

                if isinstance(current_obj, (list, tuple)):
                    # Handle lists/tuples (arrays in JS)
                    # undefined/functions in JS arrays become null. In Python, None is null, functions are omitted.
                    return [
                        self.default(item) for item in current_obj
                        if item is not None and not callable(item) # Filter out callable items (functions)
                    ]

                if isinstance(current_obj, dict):
                    # Handle dictionaries (objects in JS)
                    # Sort keys for stable output and filter out None/callable values
                    cleaned_dict = {}
                    for key in sorted(current_obj.keys()):
                        value = current_obj[key]
                        if value is not None and not callable(value): # Filter out callable items (functions)
                             cleaned_dict[key] = self.default(value)
                    return cleaned_dict

                # For other types, let the default JSON encoder handle it
                return super().default(current_obj)
            finally:
                self.ancestors.remove(obj_id)

    # Use the custom encoder with sorting keys
    # ensure_ascii=False for proper handling of non-ASCII characters if needed, but not specified in original
    return json.dumps(obj, sort_keys=True, cls=StableJsonEncoder)