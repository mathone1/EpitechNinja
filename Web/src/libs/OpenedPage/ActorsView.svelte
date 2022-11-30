<script lang="ts">

  import type { Actor } from '../interfaces/Actor';

  export let actors: Actor[];

</script>

<div class="pt-3 pb-2 select-none">
  <div class="pl-4 text-neutral-300 font-semibold pb-3">Actors</div>
  <div class="flex px-6 overflow-x-auto hideScroll gap-5">
    {#each actors as actor, index}
      <div class="flex flex-col h-40 gap-1">
        {#if actor.profilePath != null}
          <img
            alt=""
            src="{import.meta.env.VITE_API_URL}/images/actor{actor.profilePath}"
            draggable="false"
            class="w-12 h-12 sm:w-16 sm:h-16 object-cover rounded-md transition-all duration-300 ease-in-out pb-1 cursor-pointer hover:opacity-60"
          />
        {:else}
          <div class="w-12 h-12 sm:w-16 sm:h-16 bg-neutral-600/10 rounded-md"/>
        {/if}
        <div class="text-white text-xs w-12 sm:w-16 max-h-8 overflow-hidden">{actor.character.replace(/ *\([^)]*\) */g, "")}</div>
        <div class="text-neutral-400 text-xs w-12 sm:w-16 max-h-8 overflow-hidden">{actor.name}</div>
      </div>
    {/each}
  </div>
</div>

<style>
	.hideScroll::-webkit-scrollbar { display: none; }
  /* .hidescroll {
  	-ms-overflow-style: none;
  	scrollbar-width: none;
	} */
</style>
