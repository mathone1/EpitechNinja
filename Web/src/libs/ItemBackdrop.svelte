<script lang="ts">

  import { onMount } from "svelte";

  import type { Movie } from "./interfaces/Movie";

  import { currentLocale, localized } from "./functions/localized";

  export let openItem: (item: Movie) => void;
  export let item: Movie;

  let posterNotAvailable = false;

  function formatSeconds(seconds: number) {
    let date = new Date(0);
    date.setSeconds(seconds);
    return date.toISOString().substring(11, 19)
  }

  $: watched = (item as Movie).progress == -1
  $: progress = item.progress == 0 ? 0 : item.progress == -1 ? 100 : (item.progress / item.duration) * 100;

</script>

<div class="p-2 select-none sm:hover:scale-105">
  <div
    on:click={() => openItem(item)}
    on:keypress={() => openItem(item)}
    class="flex items-center justify-center text-center cursor-pointer transition-all duration-300 ease-in-out "
  >
    <div class="relative rounded-lg overflow-hidden">
      {#if item.tmdbId != null && posterNotAvailable == false}
        <img
          alt={localized(item.title)}
          src="{import.meta.env.VITE_API_URL}/images/movie/{item.tmdbId}/backdrop/{currentLocale()}"
          on:error={() => { posterNotAvailable = true }}
          class="w-auto h-auto object-cover {watched ? "grayscale" : ""}"
        />
      {:else}
        <div class="w-full h-full flex items-center justify-center bg-slate-800">{localized(item.title)}</div>
      {/if}

      <div class="absolute bottom-0 left-0 right-0">
        <div
          class="rounded-r-md h-2 bg-indigo-700"
          style="width: {progress}%"
        />
      </div>

    </div>

  </div>

  <div class="flex justify-end text-neutral-400 pt-2 pr-3 text-sm gap-1">
    <div class="font-bold">{formatSeconds(item.progress)}</div>
    <div class="font-semibold">/</div>
    <div class="font-bold">{formatSeconds(item.duration)}</div>
  </div>

</div>
