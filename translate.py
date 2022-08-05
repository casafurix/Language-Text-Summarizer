from googletrans import Translator

translator = Translator()

out = translator.translate("Messi is the greatest of all time.", dest="hi")

print(out.text)