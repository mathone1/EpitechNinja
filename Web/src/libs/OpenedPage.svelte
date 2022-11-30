<script lang="ts">

  import { scale } from "svelte/transition";

  import type { Movie } from "./interfaces/Movie";

	import OpenedMovie from "./OpenedPage/OpenedMovie.svelte";

  export let item: Movie | null;

  $: movie = item as Movie;

</script>

<div
  transition:scale={{duration: 300}}
  class="fixed top-0 bottom-0 left-0 right-0 z-50 w-full h-full bg-neutral-900"
>
  {#if movie != null}
    <OpenedMovie
      bind:movie={movie}
    />
  {/if}

  <div class="absolute top-0 right-0 topSafeMargin">
    <div
      on:click={() => { item = null }}
      on:keydown={() => {}}
      class="text-white rounded-lg p-2 z-10 bg-red-700 cursor-pointer m-4"
    >
      Close
    </div>
  </div>

</div>
