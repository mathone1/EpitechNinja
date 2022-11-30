import { writable } from "svelte/store";
import { browser } from "$app/environment";

const storedUser = browser ? localStorage.getItem('user') ?? '1' : '1';
export const userId = writable(storedUser);
userId.subscribe(value => { if (browser) localStorage.setItem('user', value) });
