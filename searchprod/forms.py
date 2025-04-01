from django import forms

class RatingForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'placeholder': 'Rate between 1 and 5'}),
        label="Your Rating"
    )
