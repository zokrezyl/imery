"""
ListBox widget
"""

from imgui_bundle import imgui
from imery.frontend.widget import Widget
from imery.frontend.decorators import widget
from imery.result import Result, Ok


@widget
class Listbox(Widget):
    """Listbox widget"""

    def _pre_render_head(self) -> Result[None]:
        if not self._data_path:
            return Result.error("Listbox requires path (id)")

        # Get value using field_values
        value_res = self._field_values.get("label")
        if not value_res:
            return Result.error(f"Listbox: failed to get value", value_res)
        current_value = value_res.unwrapped

        if not isinstance(self._params, dict):
            return Result.error(f"Listbox params must be dict, got {type(self._params)}")

        items = self._params.get("items", [])
        height = self._params.get("height", 4)

        try:
            idx = items.index(str(current_value))
        except ValueError:
            idx = 0

        imgui_id = f"###{self.uid}"
        changed, idx = imgui.list_box(imgui_id, idx, items, height)
        if changed and 0 <= idx < len(items):
            set_res = self._field_values.set("label", items[idx])
            if not set_res:
                return Result.error(f"Listbox: failed to set value", set_res)

        return Ok(None)
