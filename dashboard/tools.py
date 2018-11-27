from bokeh.models import HoverTool, RangeTool, PanTool

DEFAULT_TOOLS = 'save'


def make_hover_tool():
    hover = HoverTool(tooltips=[('Cases', '@total'),
                                ('Cases Smoothed', '@total_smooth'),
                                ('Date', '@date{%F}')],
                      formatters={'date': 'datetime'},
                      mode='vline',
                      line_policy='nearest'
                      )
    return hover

def make_pan_tool():
    pan = PanTool()

def make_range_tool(chart):
    ranger = RangeTool(x_range=chart.x_range)
    ranger.overlay.fill_color = "navy"
    ranger.overlay.fill_alpha = 0.2
    return ranger
