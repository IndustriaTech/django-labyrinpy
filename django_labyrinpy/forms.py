# from django import forms


# class SendMessageForm(forms.Form):
#     destination = forms.CharField(max_length=16)
#     message_type = forms.CharField(max_length=7)

#     def clean_message_type(self):
#         message_type = self.cleaned_data['message_type']
#         if message_type not in ['text', 'wap_url', 'binary']:
#             raise forms.ValidationError("Choose text/wap_url/binary")
#         return message_type
