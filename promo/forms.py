from django import forms
import base64
import json
import os


class PromoGenerationForm(forms.Form):

    group = forms.CharField()
    count = forms.IntegerField(widget=forms.NumberInput)

    @staticmethod
    def json_add(ser_data):

        i = 0
        s = {"promo": []}
        exact = False
        ser_key = list(ser_data.keys())

        if os.path.isfile('promo/result/result.json'):

            with open('promo/result/result.json', 'r+') as r:

                json_old = json.load(r)

                while i in range(len(json_old["promo"])):

                    if list(json_old["promo"][i].keys()) == ser_key:

                        for key in json_old["promo"][i]:

                            if ser_data[key] not in json_old["promo"][i][key]:
                                same = False
                            else:
                                same = True

                            exact = True

                        if not same:
                            json_old["promo"][i][key].extend(ser_data[key])

                    i += 1

                if not exact:
                    json_old["promo"].append(dict.fromkeys(ser_key, ser_data[ser_key[0]]))

                r.seek(0)
                json.dump(json_old, r)
        else:

            with open('promo/result/result.json', 'w+') as f:

                z = json.loads(json.dumps(s))
                z["promo"].append(ser_data)
                json.dump(z, f)

    def generate(self):
        codes = []
        i = 0

        if PromoGenerationForm.is_valid(self):
            while i in range(self.cleaned_data['count']):
                token = os.urandom(16)
                codes.append(base64.b64encode(token).decode())
                i += 1
            promos = dict.fromkeys([self.cleaned_data['group']], codes)
        else:
            while i in range(PromoGenerationForm['count'].data):
                token = os.urandom(16)
                codes.append(base64.b64encode(token).decode())
                i += 1
            promos = dict.fromkeys(PromoGenerationForm['group'].data, codes)
        self.json_add(promos)
