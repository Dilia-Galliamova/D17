from django import template


register = template.Library()

forbidden_words = ['дрянь', 'тварь']


@register.filter()
def censor(txt):
   words = txt.split()
   result = []
   for word in words:
      word_lowcase = word.lower()
      if word_lowcase in forbidden_words:
         result.append(word[0] + "*" * (len(word) - 2) + word[-1])
      else:
         result.append(word)
   return " ".join(result)
