export interface Progress {

  tmdbId: string
  progress: number

}

export function isProgress(item: any): boolean {
  if (item == null) return false
  return 'tmdbId' in item && 'progress' in item
}
