<script lang="ts">

  import type { Movie } from "../libs/interfaces/Movie";

  import { currentLocale, localized } from "./functions/localized";

  export let openItem: (item: Movie) => void;
  export let item: Movie;

  let posterNotAvailable = false;

  $: watched = (item as Movie).progress == -1

</script>

<div
  on:click={() => openItem(item)}
  on:keydown={() => openItem(item)}
  class="p-2 flex items-center justify-center text-center cursor-pointer transition-all duration-300 ease-in-out sm:hover:scale-105 active:scale-95 aspect-poster"
>

  <div class="relative rounded-lg overflow-hidden">
    {#if item.tmdbId != null && posterNotAvailable == false}
      <img
        alt={localized(item.title)}
        src="{import.meta.env.VITE_API_URL}/images/movie/{item.tmdbId}/poster/{currentLocale()}"
        on:error={() => { posterNotAvailable = true }}
        class="w-auto h-auto object-cover {watched ? "grayscale" : ""}"
      />
    {:else}
      <div class="w-full h-full flex items-center justify-center bg-slate-800">{localized(item.title)}</div>
    {/if}

  </div>

</div>
