import pandas as pd
from bokeh.plotting import figure

from dashboard import tools
from dashboard.models import get_heb_name
from dashboard.tools import DEFAULT_TOOLS
from dashboard.config import COLORS, REGIONS


def _make_times(min_date, max_date):
    now = pd.Timestamp('now', tz='UTC')
    if not max_date:
        max_date = now
    else:
        max_date = pd.to_datetime(max_date, unit='s').tz_localize('UTC')
    max_date = min(max_date, now - pd.DateOffset(weeks=2))
    if not min_date:
        min_date = max_date - pd.DateOffset(days=14)
    else:
        min_date = pd.to_datetime(min_date, unit='s').tz_localize('UTC')
    min_date = min(min_date, max_date - pd.DateOffset(weeks=30))

    return min_date, max_date


def make_plot(source, disease, min_date, max_date):
    min_date, max_date = _make_times(min_date, max_date)
    p = figure(
        tools=DEFAULT_TOOLS,
        x_axis_type='datetime',
        x_range=(min_date, max_date),
        toolbar_location='above',
        name='main_chart'

    )
    p.toolbar.logo = None
    p.toolbar_location = None
    p.background_fill_alpha = 1
    p.css_classes = ['bk-h-100']
    p.title.text = disease + ' | ' + get_heb_name(disease)
    p.title.text_font_size = '18pt'
    l1 = p.line('date', 'total', source=source, line_width=0.5, line_dash='dashed', legend='דיווחים')
    l2 = p.line('date', 'total_smooth', source=source, line_width=2, legend='החלקה')
    l3 = p.line('date', 'total_smooth', source=source, line_width=0, line_alpha=0)
    hover = tools.make_hover_tool()
    p.add_tools(hover)
    hover.renderers = [l3]
    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'

    return p


def make_split_plot(source, disease):
    now = pd.Timestamp('now', tz='UTC')
    p = figure(
        tools=DEFAULT_TOOLS,
        x_axis_type='datetime',
        # x_range=(pd.Timestamp('2018-1-1'), now.date()),
        toolbar_location='above',
        name='main_chart_split'

    )
    p.toolbar.logo = None
    p.toolbar_location = None
    p.background_fill_alpha = 1
    p.css_classes = ['bk-h-100']
    p.title.text = disease + ' | ' + get_heb_name(disease)
    p.title.text_font_size = '18pt'
    for i, region in enumerate(REGIONS[::1]):
        l = p.line('date', region, source=source,
                   line_color=COLORS[i],
                   line_width=5,
                   legend=region.replace('_', ' ').capitalize())
        hover = tools.make_split_hover_tool(region)
        hover.renderers = [l]
        p.add_tools(hover)
    z = tools.make_zoom_tool()
    p.add_tools(z)
    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'
    # p.legend.orientation = "horizontal"
    # p.legend.label_text_font_size = '4pt'
    p.legend.label_height = 10
    return p


def make_range_plot(source, range_tool, name='ranger'):
    p = figure(title='Select the time period you would like to view',
               y_axis_type=None,
               x_axis_type='datetime',
               tools='', toolbar_location=None,
               background_fill_color="#efefef",
               name=name
               )
    p.css_classes = ['bk-h-100']
    p.line('date', 'total', source=source)
    p.ygrid.grid_line_color = None
    p.add_tools(range_tool)
    p.toolbar.active_multi = range_tool
    return p


def make_total_bars(source, disease):
    p = figure(toolbar_location=None,
               tools='hover',
               tooltips='$name: @$name Cases (of @Total)',
               name='bars')
    regions = sorted(list(set(source.data.keys()) - {'Year', 'Total', 'index'}))
    p.vbar_stack(regions, x='Year', width=0.9, source=source, color=COLORS[:len(regions)])

    p.xgrid.grid_line_color = None
    p.title.text = f'Annual amount by regions for {disease}'
    return p
