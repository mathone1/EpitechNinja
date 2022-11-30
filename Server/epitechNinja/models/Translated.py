from typing import Union


class Translated:
  def __init__(self, en: Union[str, list], fr: Union[str, list]):

    self.en = en
    self.fr = fr


  def toDict(self):

    return {'en': self.en, 'fr': self.fr}


  @classmethod
  def fromDict(cls, dict):

    return cls(
      en = dict.get('en'),
      fr = dict.get('fr')
    )
