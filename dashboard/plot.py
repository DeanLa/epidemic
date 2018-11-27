import pandas as pd
from bokeh.plotting import figure

from dashboard import tools
from dashboard.models import get_heb_name
from dashboard.tools import DEFAULT_TOOLS


def make_plot(source, disease):
    now = pd.Timestamp('now', tz='UTC')
    chart = figure(
        tools=DEFAULT_TOOLS,
        x_axis_type='datetime',
        x_range=(pd.Timestamp('2018-1-1'), now.date()),
        toolbar_location='above',
    )
    chart.toolbar.logo=None
    chart.background_fill_alpha=1
    chart.css_classes = ['bk-h-100']
    chart.title.text = disease + ' | ' + get_heb_name(disease)
    l1 = chart.line('date', 'total', source=source, line_width=0.5, line_dash='dashed', legend='Cases')
    l2 = chart.line('date', 'total_smooth', source=source, line_width=2, legend='Smoothed')
    l3 = chart.line('date', 'total_smooth', source=source, line_width=0, line_alpha=0)
    hover = tools.make_hover_tool()
    chart.add_tools(hover)
    hover.renderers = [l3]
    chart.legend.location='top_left'
    chart.legend.click_policy='hide'

    return chart


def make_range_plot(source, range_tool):
    chart_range = figure(title=None,
                         y_axis_type=None,
                         x_axis_type='datetime',
                         tools='', toolbar_location=None,
                         background_fill_color="#efefef",
                         )
    chart_range.css_classes = ['bk-h-100']
    chart_range.line('date', 'total', source=source)
    chart_range.ygrid.grid_line_color = None
    chart_range.add_tools(range_tool)
    chart_range.toolbar.active_multi = range_tool
    return chart_range
