import { writable } from "svelte/store";
import { browser } from "$app/environment";

const storedLanguage = browser ? localStorage.getItem('language') ?? 'en' : 'en';
export const language = writable(storedLanguage);
language.subscribe(value => { if (browser) localStorage.setItem('language', value == 'fr' ? 'fr' : 'en') });
