export interface Actor {

  name: string
  character: string
  profilePath: string

}

export function isActor(item: any): boolean {
  if (item == null) return false
  return 'name' in item && 'character' in item && 'profilePath' in item
}
