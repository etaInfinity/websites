from django import forms

GALAXY_SIZE_GROUPS = [
    ("dwarf", "Dwarf (1,000-10,000 ly radius)"),
    ("small", "Small (10,000-25,000 ly radius)"),
    ("mw", "Milky Way-ish (25,000-60,000 ly radius)"),
    ("large", "Large (60,000-120,000 ly radius)"),
    ("giant", "Giant (120,000-250,000 ly radius)"),
]

class GalaxyGeneratorForm(forms.Form):
    size_group = forms.ChoiceField(choices=GALAXY_SIZE_GROUPS)
    systems_count = forms.IntegerField(min_value=1, max_value=50, initial=10)
    seed = forms.IntegerField(required=False, help_text="Leave blank for random")