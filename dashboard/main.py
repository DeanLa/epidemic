import dotenv

from dashboard.plot import make_plot, make_range_plot
from dashboard.tools import make_range_tool

dotenv.load_dotenv()
import logging

from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models.widgets import Dropdown, RadioButtonGroup

from dashboard import models
from dashboard.config import DEFAULT_DISEASE
from dashboard.models import DISEASES

logger = logging.getLogger(__name__)


def update_plot(attrname, old_value, new_value):
    disease = disease_selector.value
    smooth = int(smooth_selector.value)
    src = models.get_disease_data_by_name(disease, smooth)
    source.data.update(src.data)
    chart.title.text = disease
    disease_selector.label = disease
    smooth_selector.label = str(smooth)
    print(picker.value)


# callbacks

## Components
# Sources
source = models.get_disease_data_by_name(DEFAULT_DISEASE)

# Figures
chart = make_plot(source, DEFAULT_DISEASE)
ranger = make_range_tool(chart)
chart_range = make_range_plot(source, ranger)

# Widgets
disease_selector = Dropdown(label=DEFAULT_DISEASE, value=DEFAULT_DISEASE, menu=list(zip(DISEASES, DISEASES)))
smooth_selector = Dropdown(label='2', value=('2'), menu=[(str(i), str(i)) for i in range(1, 9)])
picker = RadioButtonGroup(labels=['Total Cases','Cases by Region'])

# Events
disease_selector.on_change('value', update_plot)
smooth_selector.on_change('value', update_plot)

#
controls = column(disease_selector, smooth_selector, widgetbox(picker))
curdoc().add_root(row(column(chart, chart_range), controls))
curdoc().title = "Epidemic"
