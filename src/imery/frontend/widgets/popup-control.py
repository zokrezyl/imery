"""
Popup control widgets - OpenPopup, CloseCurrentPopup
"""

from imgui_bundle import imgui
from imery.frontend.widget import Widget
from imery.frontend.decorators import widget
from imery.result import Result, Ok


@widget
class OpenPopup(Widget):
    """Open popup widget"""

    def _prepare_render(self) -> Result[None]:
        # OpenPopup doesn't need data path
        return Ok(None)

    def _pre_render_head(self) -> Result[None]:
        popup_id = None
        res = self._handle_error(self._data_bag.get("id", popup_id))
        if res:
            popup_id = res.unwrapped
        if not popup_id:
            return Result.error("OpenPopup requires 'id' parameter")

        imgui.open_popup(popup_id)
        return Ok(None)


@widget
class CloseCurrentPopup(Widget):
    """Close current popup widget"""

    def _prepare_render(self) -> Result[None]:
        # CloseCurrentPopup doesn't need data path
        return Ok(None)

    def _pre_render_head(self) -> Result[None]:
        imgui.close_current_popup()
        return Ok(None)
