import datetime
from typing import Dict, List, Any

from epitechNinja.models.Translated import Translated
from epitechNinja.models.Actor import Actor

from epitechNinja.utils.safeGet import safeGet

# Available Genres:

# Action          28
# Adventure       12
# Animation       16
# Comedy          35
# Crime           80
# Documentary     99
# Drama           18
# Family          10751
# Fantasy         14
# History         36
# Horror          27
# Music           10402
# Mystery         9648
# Romance         10749
# Science Fiction 878
# TV Movie        10770
# Thriller        53
# War             10752
# Western         37

class Movie:
  def __init__(
    self,
    localTitle: str, year: str, path: str, dateAdded = datetime.datetime.utcnow(), dateUpdated = datetime.datetime.utcnow(),
    tmdbId: int = None, duration: int = None, vo: str = None, releaseDate: str = None, rating: float = None, popularity: float = None, collection: int = None,
    streamOn: List[str] = None, actors: List[Actor] = None, genres: List[str] = None,
    poster: Translated = None, backdrop: Translated = None, title: Translated = None, shortDesc: Translated = None, desc: Translated = None, trailer: Translated = None
  ):

    self.localTitle = localTitle
    self.year = year
    self.path = path
    self.dateAdded = dateAdded
    self.dateUpdated = dateUpdated

    self.tmdbId = tmdbId
    self.duration = duration
    self.vo = vo
    self.releaseDate = releaseDate
    self.rating = rating
    self.popularity = popularity
    self.collection = collection

    self.streamOn = streamOn
    self.actors =  actors
    self.genres = genres

    # Localized
    self.poster = poster
    self.backdrop = backdrop
    self.title = title
    self.shortDesc = shortDesc
    self.desc = desc
    self.trailer = trailer #array


  def toDict(self):

    return {
      'localTitle': self.localTitle,
      'year': self.year,
      'path': self.path,
      'dateAdded': self.dateAdded,
      'dateUpdated': self.dateUpdated,

      'tmdbId': self.tmdbId,
      'duration': self.duration,
      'vo': self.vo,
      'releaseDate': self.releaseDate,
      'rating': self.rating,
      'popularity': self.popularity,
      'collection': self.collection,

      'streamOn': self.streamOn,
      'actors': [x.toDict() for x in self.actors] if self.actors != None else None,
      'genres': self.genres,

      'poster': self.poster.toDict() if self.poster != None else None,
      'backdrop': self.backdrop.toDict() if self.backdrop != None else None,
      'title': self.title.toDict() if self.title != None else None,
      'shortDesc': self.shortDesc.toDict() if self.shortDesc != None else None,
      'desc': self.desc.toDict() if self.desc != None else None,
      'trailer': self.trailer.toDict() if self.trailer != None else None
    }


  def toFrontEnd(self):

    return {
      'title': (self.title.toDict() if self.title != None else None) if self.tmdbId is not None else Translated(en=self.localTitle, fr=self.localTitle).toDict(),
      'desc': self.desc.toDict() if self.desc != None else None,
      'shortDesc': self.shortDesc.toDict() if self.shortDesc != None else None,
      'poster': self.poster.toDict() if self.poster != None else None,
      'backdrop': self.backdrop.toDict() if self.backdrop != None else None,
      'genres': self.genres,
      'dateAdded': self.dateAdded,
      'dateUpdated': self.dateUpdated,

      'available': self.path is not None,
      'tmdbId': self.tmdbId,
      'streamOn': self.streamOn,
      'actors': [x.toDict() for x in self.actors] if self.actors != None else None,
      'duration': self.duration,
      'releaseDate': self.releaseDate,
      'rating': self.rating,
      'popularity': self.popularity,
      'vo': self.vo,
      'trailers': self.trailer.toDict() if self.trailer != None else None
    }


  @classmethod
  def fromDict(cls, dict: Dict[str, Any]):

    return cls(
      localTitle = dict.get('localTitle'),
      year = dict.get('year'),
      path = dict.get('path'),
      dateAdded = dict.get('dateAdded'),
      dateUpdated = dict.get('dateUpdated'),

      tmdbId = dict.get('tmdbId'),
      duration = dict.get('duration'),
      vo = dict.get('vo'),
      releaseDate = dict.get('releaseDate'),
      rating = dict.get('rating'),
      popularity = dict.get('popularity'),
      collection = dict.get('collection'),

      streamOn = dict.get('streamOn', []),
      actors = [Actor.fromDict(x) for x in safeGet(dict, 'actors')],
      genres = dict.get('genres', []),

      poster = Translated.fromDict(safeGet(dict, 'poster')),
      backdrop = Translated.fromDict(safeGet(dict, 'backdrop')),
      title = Translated.fromDict(safeGet(dict, 'title')),
      shortDesc = Translated.fromDict(safeGet(dict, 'shortDesc')),
      desc = Translated.fromDict(safeGet(dict, 'desc')),
      trailer = Translated.fromDict(safeGet(dict, 'trailer'))
    )
