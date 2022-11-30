import type { Translation, Trailer } from "./Translation"
import type { Actor } from "./Actor"

export interface Movie {

  title: Translation
  desc: Translation
  shortDesc: Translation
  poster: Translation
  backdrop: Translation
  genres: string[]
  dateAdded: Date
  dateUpdated: Date

  progress: number
  available: boolean
  tmdbId: number
  streamOn: string[]
  actors: Actor[]
  duration: number
  releaseDate: string
  rating: number
  popularity: number
  vo: string
  trailers: Trailer

}

export function isMovie(item: any): boolean {
  if (item == null) return false
  return 'title' in item && 'desc' in item && 'shortDesc' in item && 'poster' in item && 'backdrop' in item && 'genres' in item && 'dateAdded' in item && 'dateUpdated' in item
    && 'progress' in item && 'available' in item && 'tmdbId' in item && 'streamOn' in item && 'actors' in item && 'duration' in item && 'releaseDate' in item && 'rating' in item && 'popularity' in item && 'vo' in item && 'trailers' in item
}
