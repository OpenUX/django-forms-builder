
from django.core.exceptions import ImproperlyConfigured
from django import forms
from django.forms.extras import SelectDateWidget
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _

from forms_builder.forms.settings import USE_HTML5, EXTRA_FIELDS


# Constants for all available field types.
TEXT = 1
TEXTAREA = 2
EMAIL = 3
CHECKBOX = 4
CHECKBOX_MULTIPLE = 5
SELECT = 6
SELECT_MULTIPLE = 7
RADIO_MULTIPLE = 8
FILE = 9
DATE = 10
DATE_TIME = 11
HIDDEN = 12
NUMBER = 13
URL = 14
DOB = 15

# Names for all available field types.
NAMES = (
    (TEXT, _("Single line text")),
    (TEXTAREA, _("Multi line text")),
    (EMAIL, _("Email")),
    (NUMBER, _("Number")),
    (URL, _("URL")),
    (CHECKBOX, _("Check box")),
    (CHECKBOX_MULTIPLE, _("Check boxes")),
    (SELECT, _("Drop down")),
    (SELECT_MULTIPLE, _("Multi select")),
    (RADIO_MULTIPLE, _("Radio buttons")),
    (FILE, _("File upload")),
    (DATE, _("Date")),
    (DATE_TIME, _("Date/time")),
    (DOB, _("Date of birth")),
    (HIDDEN, _("Hidden")),
)

# Field classes for all available field types.
CLASSES = {
    TEXT: forms.CharField,
    TEXTAREA: forms.CharField,
    EMAIL: forms.EmailField,
    CHECKBOX: forms.BooleanField,
    CHECKBOX_MULTIPLE: forms.MultipleChoiceField,
    SELECT: forms.ChoiceField,
    SELECT_MULTIPLE: forms.MultipleChoiceField,
    RADIO_MULTIPLE: forms.ChoiceField,
    FILE: forms.FileField,
    DATE: forms.DateField,
    DATE_TIME: forms.DateTimeField,
    DOB: forms.DateField,
    HIDDEN: forms.CharField,
    NUMBER: forms.FloatField,
    URL: forms.URLField,
}

# Widgets for field types where a specialised widget is required.
WIDGETS = {
    TEXTAREA: forms.Textarea,
    CHECKBOX_MULTIPLE: forms.CheckboxSelectMultiple,
    RADIO_MULTIPLE: forms.RadioSelect,
    DATE: SelectDateWidget,
    DOB: SelectDateWidget,
    HIDDEN: forms.HiddenInput,
}

# Some helper groupings of field types.
CHOICES = (CHECKBOX, SELECT, RADIO_MULTIPLE)
DATES = (DATE, DATE_TIME, DOB)
MULTIPLE = (CHECKBOX_MULTIPLE, SELECT_MULTIPLE)

# HTML5 Widgets
if USE_HTML5:
    html5_field = lambda name, base: type("", (base,), {"input_type": name})
    WIDGETS.update({
        DATE: html5_field("date", forms.DateInput),
        DATE_TIME: html5_field("datetime", forms.DateTimeInput),
        DOB: html5_field("date", forms.DateInput),
        EMAIL: html5_field("email", forms.TextInput),
        NUMBER: html5_field("number", forms.TextInput),
        URL: html5_field("url", forms.TextInput),
    })

# Add any custom fields defined.
for field_id, field_path, field_name in EXTRA_FIELDS:
    if field_id in CLASSES:
        err = "ID %s for field %s in FORMS_EXTRA_FIELDS already exists"
        raise ImproperlyConfigured(err % (field_id, field_name))
    module_path, member_name = field_path.rsplit(".", 1)
    CLASSES[field_id] = getattr(import_module(module_path), member_name)
    NAMES += ((field_id, _(field_name)),)
