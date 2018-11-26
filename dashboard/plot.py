import pandas as pd
from bokeh.plotting import figure
from bokeh.models import Range1d

from . import tools
from .config import WIDTH
from .tools import DEFAULT_TOOLS


def make_plot(source, disease):
    now = pd.Timestamp('now', tz='UTC')
    chart = figure(
        plot_width=WIDTH,
        plot_height=600,
        sizing_mode="scale_width",
        tools=DEFAULT_TOOLS,
        x_axis_type='datetime',
        x_range=(pd.Timestamp('2018-1-1'), now.date()),
    )
    chart.title.text = disease
    chart.line('date', 'total', source=source, line_width=0.5, line_dash='dashed', legend='Cases')
    chart.line('date', 'total_smooth', source=source, line_width=2, legend='Smoothed')
    hover = tools.make_hover_tool()
    chart.add_tools(hover)
    chart.legend.location='top_left'
    chart.legend.click_policy='hide'

    return chart


def make_range_plot(source, range_tool):
    chart_range = figure(title=None,
                         plot_height=100,
                         plot_width=WIDTH,
                         y_axis_type=None,
                         sizing_mode="stretch_both",
                         x_axis_type='datetime',
                         tools='', toolbar_location=None, background_fill_color="#efefef")
    chart_range.line('date', 'total', source=source)
    chart_range.ygrid.grid_line_color = None
    chart_range.add_tools(range_tool)
    chart_range.toolbar.active_multi = range_tool
    return chart_range
