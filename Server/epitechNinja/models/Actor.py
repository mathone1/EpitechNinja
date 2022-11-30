class Actor:
  def __init__(self, name: str, character: str, profilePath: str):

    self.name = name
    self.character = character
    self.profilePath = profilePath


  def toDict(self):

    return {'name': self.name, 'character': self.character, 'profilePath': self.profilePath}


  @classmethod
  def fromDict(cls, dict):

    return cls(
      name = dict.get('name'),
      character = dict.get('character'),
      profilePath = dict.get('profilePath'),
    )
