from django.forms import ModelForm, NumberInput, Textarea, TextInput
from django.core.exceptions import NON_FIELD_ERRORS 
from .models import Auction, Bid, Comment


class AddNewAuction(ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'minimum_bid', 'description', 'image', 'category']
        widgets = {
            'description': Textarea(attrs={'cols': 100, 'rows': 10})
        }
        
    def __init__(self, *args, **kwargs):
        super(AddNewAuction, self).__init__(*args, **kwargs)
        self.fields['minimum_bid'].widget.attrs['min'] = 0.01


class AddNewBid(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            'bid': NumberInput(attrs={'placeholder': 'Add your bid'})
        }

    def __init__(self, *args, **kwargs):
        super(AddNewBid, self).__init__(*args, **kwargs)
        self.fields['bid'].widget.attrs['min'] = 0.01


class AddNewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': Textarea(attrs={'cols': 50, 'rows': 5, 'placeholder': 'Add your comment'})
        }

    
