import logging
import os

import dotenv

dotenv.load_dotenv()
from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.models import Div, Slider, CustomJS, Button, Dropdown, RadioButtonGroup, Spacer

from dashboard import models
from dashboard.config import (DEFAULT_DISEASE, smooth_selector_more, disease_selector_more, download_button_more,
                              picker_more)
from dashboard.models import DISEASE_DROPDOWN
from dashboard.plot import make_plot, make_range_plot, make_total_bars, make_split_plot
from dashboard.tools import make_range_tool, data_tooltip, disease_information

logger = logging.getLogger(__name__)

read_js = lambda fn: open(os.path.join(os.path.dirname(__file__), 'static', 'js', fn)).read()


def update_plot(attrname, old_value, new_value):
    disease = disease_selector.value
    smooth = int(smooth_selector.value)
    # Main Chart
    src = models.get_disease_totals_by_name(disease, smooth)
    source_line.data.update(src.data)
    src = models.get_disease_split_by_name(disease, smooth)
    source_split.data.update(src.data)
    heb = models.get_heb_name(disease)
    for p in [chart, chart_split]:
        p.title.text = disease + ' | ' + heb
        p.title.text = f'{disease} | {heb}'

    # Selector
    disease_selector.label = models.get_heb_name(disease)

    # Smooth Tooltip
    smooth_info.text = data_tooltip(smooth_selector_more, 'החלקה: {} שבועות'.format(smooth))

    # Download Button
    download_button.label = db_label.format(disease_selector.label)
    # Bars
    src = models.get_disease_sums_by_name(disease)
    source_sums.data.update(src.data)

    heb_info.text = disease_information(disease)
    curdoc().title = "Epidemic - {}".format(disease)
    curdoc().template_variables.update(disease=disease)
    curdoc().template_variables.update(disease_heb=models.get_heb_name(disease))


# request
args = curdoc().session_context.request.arguments
# request = make_request(args)
get_param = lambda param, default: args.get(param, [bytes(str(default), encoding='utf')])[0].decode('utf-8')
disease = get_param('disease', DEFAULT_DISEASE)
heb = models.get_heb_name(disease)
smooth = int(get_param('smooth', 2))
chart_type = int(get_param('split', 0))
min_date = get_param('min_date', '')
max_date = get_param('max_date', '')
## Components

# Widgets
disease_info = Div(text=data_tooltip(disease_selector_more, 'מחלה'), css_classes=['heb'])
disease_selector = Dropdown(label=models.get_heb_name(disease), value=disease, menu=DISEASE_DROPDOWN,
                            css_classes=['heb', 'disease_selector'])
smooth_info = Div(text=data_tooltip(smooth_selector_more, 'החלקה: {} שבועות'.format(smooth)), css_classes=['heb'])
smooth_selector = Slider(title=None, value=int(smooth), start=1, step=1, end=8, css_classes=['heb'])
heb_info = Div(text=disease_information(disease))
picker = RadioButtonGroup(labels=['סה"כ דיווחים', 'חלוקה לפי איזורים'], active=chart_type,
                          css_classes=['heb', 'w-100', 'picker'])
picker_info = Div(text=data_tooltip(picker_more, 'חלוקה'.format(smooth)), css_classes=['heb'])

db_label = 'להורדת CSV עם נתוני {}'
download_button = Button(label=db_label.format(disease_selector.label), css_classes=['heb'], button_type='primary')
download_button_info = Div(text=data_tooltip(download_button_more, 'הורדת המידע למחשב'.format(smooth)),
                           css_classes=['heb'])
control_list = widgetbox(disease_info, disease_selector,
                         picker_info, picker,
                         smooth_info, smooth_selector,
                         download_button_info, download_button,
                         heb_info)
controls = column(control_list, name='controls')

# Sources
source_line = models.get_disease_totals_by_name(disease, smooth)
source_split = models.get_disease_split_by_name(disease, smooth)
source_sums = models.get_disease_sums_by_name(disease)

# Figures
chart = make_plot(source_line, disease, min_date, max_date)
chart_split = make_split_plot(source_split, disease)
chart_split.x_range = chart.x_range
ranger = make_range_tool(chart)
chart_range = make_range_plot(source_line, ranger)
bars = make_total_bars(source_sums, disease)

# Callbacks
request = {'ds': disease_selector,
           'ss': smooth_selector,
           'pick': picker,
           'xr': chart.x_range,
           'translate':dict([(x[1], x[0]) for x in DISEASE_DROPDOWN])}
js_history = CustomJS(args=request, code=read_js('history_push.js'))
js_toggle_split = CustomJS(args={'pick': picker}, code=read_js('toggle_split.js'))

# Events
for selector in [disease_selector, smooth_selector]:
    selector.on_change('value', update_plot)
    selector.js_on_change('value', js_history)
picker.js_on_change('active', js_toggle_split)
picker.js_on_change('active', js_history)
picker.active = chart_type
chart.x_range.callback = js_history
download_button.callback = CustomJS(args=dict(source=source_split,
                                              save_path='epidemic_co_il_{}.csv'.format(
                                                  disease_selector.value.lower().replace(' ', '_'))),
                                    code=read_js('save_data.js'))

# Document
for element in [controls, chart_range, chart, chart_split, bars]:
    element.sizing_mode = "stretch_both"
    curdoc().add_root(element)
curdoc().title = "Epidemic"
curdoc().template_variables.update(p=picker.active)
if 'disease' in args.keys():
    curdoc().title = "Epidemic - {}".format(disease)
update_plot(None, None, None)
