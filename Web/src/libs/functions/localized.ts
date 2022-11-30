import type { Translation } from "../interfaces/Translation";
import { language } from "../languageStore";
import { get } from "svelte/store";

export function localized(item: Translation): string {
  return get(language) == 'en' ? item.en : item.fr == undefined ? item.en : item.fr
}

export function currentLocale(): string {
  return get(language);
}
