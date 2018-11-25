import logging

import dotenv

dotenv.load_dotenv()
from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource, Div, Slider
from bokeh.models.widgets import Dropdown, RadioButtonGroup

from dashboard import models
from dashboard.config import DEFAULT_DISEASE
from dashboard.models import DISEASES
from dashboard.plot import make_plot, make_range_plot
from dashboard.tools import make_range_tool

logger = logging.getLogger(__name__)


def update_plot(attrname, old_value, new_value):
    disease = disease_selector.value
    smooth = int(smooth_selector.value)
    src = models.get_disease_totals_by_name(disease, smooth)
    source.data.update(src.data)
    chart.title.text = disease
    disease_selector.label = disease
    heb = models.get_heb_name(disease)
    heb_name.text = f'<h1>{heb}</h1'
    curdoc().title = "Epidemic - {}".format(disease)


# request
args = curdoc().session_context.request.arguments
get_param = lambda param, default: args.get(param, [bytes(str(default), encoding='utf')])[0].decode('utf-8')
disease = get_param('disease', DEFAULT_DISEASE)
smooth = get_param('smooth', 2)
## Components

# Widgets
disease_selector = Dropdown(label=disease, value=disease, menu=list(zip(DISEASES, DISEASES)))
# smooth_selector = Slider(title=smooth, value=smooth, menu=[(str(i), str(i)) for i in range(1, 9)])
smooth_selector = Slider(title='Smoothing', value=int(smooth), start=1, step=1,end=8)
heb_name = Div(text=f'<h1>{disease}</h1')
picker = RadioButtonGroup(labels=['Total Cases', 'Cases by Region'], width=300)

# Sources

source = ColumnDataSource()  # models.get_disease_data_by_name(disease,smooth)
# Events
disease_selector.on_change('value', update_plot)
smooth_selector.on_change('value', update_plot)

# Figures
chart = make_plot(source, disease)
ranger = make_range_tool(chart)
chart_range = make_range_plot(source, ranger)

#
controls = column(widgetbox(disease_selector, smooth_selector, heb_name), height=280, name='dean')
charts_col = column(chart, chart_range, width=1024)

curdoc().add_root(row(charts_col, controls))
curdoc().title = "Epidemic - {}".format(disease)
update_plot(None, None, None)
