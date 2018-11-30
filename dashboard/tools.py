from bokeh.models import HoverTool, RangeTool, PanTool
from dashboard.models import get_heb_info_by_name, get_heb_name

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


# Basic Divs
def data_tooltip(hover='', inside='I'):
    html = f'''<button type="button" class="btn btn-secondary" data-toggle="tooltip" data-placement="top" title="{hover}">
    <i class="fas fa-info-circle"></i>{inside}
    </button>'''
    return html


def disease_information(disease):
    info, wiki = get_heb_info_by_name(disease)
    html = f'''<h3 class="heb">{get_heb_name(disease)}</h3>
        <hr>'''
    if info is not None:
        html+=f'<p class="heb">{info}</p>'
    if wiki is not None:
        html+=f'<a href="{wiki}" class="heb">מידע נוסף</a>'
    return html
