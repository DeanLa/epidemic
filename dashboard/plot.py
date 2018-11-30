import pandas as pd
from bokeh.plotting import figure

from dashboard import tools
from dashboard.models import get_heb_name
from dashboard.tools import DEFAULT_TOOLS
from dashboard.config import COLORS

myReds = [
    '#000000',
    '#080000',
    '#100000',
    '#180000',
    '#200000',
    '#280000',
    '#300000',
    '#380000',
    '#400000',
    '#480000',
    '#500000',
    '#580000',
    '#600000',
    '#680000',
    '#700000',
    '#780000',
    '#800000',
    '#880000',
    '#900000',
    '#980000',
    '#A00000',
    '#A80000',
    '#B00000',
    '#B80000',
    '#C00000',
    '#C80000',
    '#D00000',
    '#D80000',
    '#E00000',
    '#E80000',
    '#F00000',
    '#F80000',
    '#FF0000']


def make_plot(source, disease):
    now = pd.Timestamp('now', tz='UTC')
    p = figure(
        tools=DEFAULT_TOOLS,
        x_axis_type='datetime',
        x_range=(pd.Timestamp('2018-1-1'), now.date()),
        toolbar_location='above',
        name='main_chart'

    )
    p.toolbar.logo = None
    p.background_fill_alpha = 1
    p.css_classes = ['bk-h-100']
    p.title.text = disease + ' | ' + get_heb_name(disease)
    l1 = p.line('date', 'total', source=source, line_width=0.5, line_dash='dashed', legend='Cases')
    l2 = p.line('date', 'total_smooth', source=source, line_width=2, legend='Smoothed')
    l3 = p.line('date', 'total_smooth', source=source, line_width=0, line_alpha=0)
    hover = tools.make_hover_tool()
    p.add_tools(hover)
    hover.renderers = [l3]
    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'

    return p


def make_range_plot(source, range_tool):
    p = figure(title='Select the time period you would like to view',
               y_axis_type=None,
               x_axis_type='datetime',
               tools='', toolbar_location=None,
               background_fill_color="#efefef",
               name='ranger'
               )
    p.css_classes = ['bk-h-100']
    p.line('date', 'total', source=source)
    p.ygrid.grid_line_color = None
    p.add_tools(range_tool)
    p.toolbar.active_multi = range_tool
    return p


def make_total_bars(source):
    p = figure(toolbar_location=None,
               tools='hover',
               tooltips='$name: @$name Cases (of @Total)',
               name='bars')
    regions = sorted(list(set(source.data.keys()) - {'Year', 'Total', 'index'}))
    p.vbar_stack(regions, x='Year', width=0.9, source=source, color=COLORS[:len(regions)])

    p.xgrid.grid_line_color = None
    p.title.text = 'Annual amount by regions for {disease}'
    return p
