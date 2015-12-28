from django import forms


class TachyControlForm(forms.Form):
    sensor = forms.ChoiceField(choices=(
        ('1', 'TPS15'),
        ('2', 'TCRP1102'),
        ('3', 'TM50')
    ))
    command = forms.ChoiceField(choices=(
        ('l1', 'Lage I'),
        ('l2', 'Lage II'),
        ('r1', 'Laser AN'),
        ('r0', 'Laser AUS'),
        ('snr', 'Zeige SNR')
    ))

    def execute(self):
        """
        Run command with tachy
        Returns:

        """
        pass