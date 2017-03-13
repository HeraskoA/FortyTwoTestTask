from django import forms


class DatePicker(forms.DateInput):
    class Media:
        js = ('http://cdnjs.cloudflare.com/ajax/libs/'
              'moment.js/2.9.0/moment.min.js',
              'http://cdnjs.cloudflare.com/ajax/libs/'
              'bootstrap-datetimepicker/'
              '4.0.0/js/bootstrap-datetimepicker.min.js',
              'js/datepicker.js')
        css = {
            'all': (
                'http://cdnjs.cloudflare.com/ajax/libs/'
                'bootstrap-datetimepicker/4.0.0/css'
                '/bootstrap-datetimepicker.min.css',
            )
        }

    def __init__(self):
        self.attrs = {'class': 'datepicker form-control'}
        super(DatePicker, self).__init__(attrs=self.attrs)
