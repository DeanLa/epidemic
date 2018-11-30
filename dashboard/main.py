import logging

import dotenv

dotenv.load_dotenv()
from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.models import Div, Slider, CustomJS
from bokeh.models.widgets import Dropdown, RadioButtonGroup

from dashboard import models
from dashboard.config import DEFAULT_DISEASE
from dashboard.models import DISEASES
from dashboard.plot import make_plot, make_range_plot, make_total_bars
from dashboard.tools import make_range_tool,data_tooltip,disease_information

logger = logging.getLogger(__name__)


def update_plot(attrname, old_value, new_value):
    disease = disease_selector.value
    smooth = int(smooth_selector.value)
    # Main Chart
    src = models.get_disease_totals_by_name(disease, smooth)
    source_line.data.update(src.data)
    heb = models.get_heb_name(disease)
    chart.title.text = disease + ' | ' + heb
    chart.title.text = f'{disease} | {heb}'

    # Selector
    disease_selector.label = disease

    # Bars
    src = models.get_disease_sums_by_name(disease)
    source_sums.data.update(src.data)
    bars.title.text = f'Annual amount by regions for {disease}'

    heb_name.text=disease_information(disease)
    curdoc().title = "Epidemic - {}".format(disease)
    curdoc().template_variables.update(disease=disease)


# request
args = curdoc().session_context.request.arguments
get_param = lambda param, default: args.get(param, [bytes(str(default), encoding='utf')])[0].decode('utf-8')
disease = get_param('disease', DEFAULT_DISEASE)
heb = models.get_heb_name(disease)
smooth = int(get_param('smooth', 2))
## Components

# Widgets
disease_info = Div(text=data_tooltip('More Instructions', 'Select Disease`'))
disease_selector = Dropdown(label=disease, value=disease, menu=list(zip(DISEASES, DISEASES)))
smooth_selector = Slider(title='Smoothing', value=int(smooth), start=1, step=1, end=8)
heb_name = Div(text=disease_information(disease))
# picker = RadioButtonGroup(labels=['Total Cases', 'Cases by Region'], width=300)
control_list = widgetbox(disease_info, disease_selector, smooth_selector, heb_name)
controls = column(control_list, name='controls')

# JS Callback
js_history = CustomJS(args={'ds': disease_selector, 'ss': smooth_selector}, code='''
    var d=ds.value;
    var s=ss.value;
    history.pushState({},
     'Epidemic  - ' + d,
      '/dashboard?disease=' + d + '&smooth='+s)
''')

# Sources
source_line = models.get_disease_totals_by_name(disease, smooth)
source_sums = models.get_disease_sums_by_name(disease)

# Events
for selector in [disease_selector, smooth_selector]:
    selector.on_change('value', update_plot)
    selector.js_on_change('value', js_history)

# Figures
chart = make_plot(source_line, disease)
ranger = make_range_tool(chart)
chart_range = make_range_plot(source_line, ranger)
bars = make_total_bars(source_sums, disease)

#

# controls.css_classes = ['cbk-controls']
# charts_col = column(chart_range, chart)

for element in [controls, chart_range, chart, bars]:
    element.sizing_mode = "stretch_both"
    curdoc().add_root(element)
curdoc().title = "Epidemic"
if 'disease' in args.keys():
    curdoc().title = "Epidemic - {}".format(disease)
    update_plot(None, None, None)
