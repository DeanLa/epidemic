import pandas as pd
from bokeh.plotting import figure

from dashboard.config import WIDTH
from dashboard.tools import DEFAULT_TOOLS


def make_plot(source, disease):
    now = pd.Timestamp('now', tz='UTC')
    chart = figure(
        plot_width=WIDTH, plot_height=768,
        sizing_mode="scale_width",
        tools=DEFAULT_TOOLS,
        x_axis_type='datetime',
        x_range=(pd.Timestamp('2018-1-1'), now.date()))
    chart.title.text = disease
    chart.line('date', 'total', source=source)
    chart.sizing_mode = "scale_both"

    return chart


def make_range_plot(source, range_tool):
    chart_range = figure(title=None,
                         plot_height=150, plot_width=WIDTH, y_axis_type=None,
                         x_axis_type='datetime',
                         tools='', toolbar_location=None, background_fill_color="#efefef")
    chart_range.line('date', 'total', source=source)
    chart_range.ygrid.grid_line_color = None
    chart_range.add_tools(range_tool)
    chart_range.toolbar.active_multi = range_tool
    return chart_range