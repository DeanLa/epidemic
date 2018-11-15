from bokeh.models import HoverTool, RangeTool

DEFAULT_TOOLS = 'pan,wheel_zoom,xbox_select,reset'

def create_hover_tool():
    pass


def make_range_tool(chart):
    ranger = RangeTool(x_range=chart.x_range)
    ranger.overlay.fill_color = "navy"
    ranger.overlay.fill_alpha = 0.2
    return ranger