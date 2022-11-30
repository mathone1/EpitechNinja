<script lang="ts">

  import { onMount } from "svelte";
  import { openDB } from 'idb';

  import { liveQuery } from "dexie";
  import { db, type DBProgress } from "../db";
  import { browser } from "$app/environment";
  import { userId } from "../userStore";

  import type { Movie } from "../../libs/interfaces/Movie";

  import PlayIcon from "../icons/PlayIcon.svelte";
	import Replay from "../icons/Replay.svelte";
	import WatchedIcon from "../icons/WatchedIcon.svelte";
  import Checkmark from "../icons/Checkmark.svelte";
  import Xmark from "../icons/Xmark.svelte";
	import Loading from "../icons/Loading.svelte";

  import { currentLocale, localized } from "../functions/localized";

  import ActorsView from "./ActorsView.svelte";

  export let movie: Movie;

  let currentUserId: number = 0;
  userId.subscribe(value => { currentUserId = parseInt(value) });

  let progress = liveQuery(() => browser ? db.progress.filter(prog => prog.id == movie.tmdbId).toArray() : []);
  let playTrailer = false;

  // onMount(async () => {
  //   const res = await fetch(`${import.meta.env.VITE_API_URL}/progress/movie/` + movie?.tmdbId)
  //   let jsonResult = await res.json();
  //   movie.progress = jsonResult.progress;
  // });

  async function setAsWatched() {
    if (movieProgressWaitingSync) return;

    if ('serviceWorker' in navigator && 'SyncManager' in window) {

      console.log('Offline sync available, initiating sync request..')

      try {
        await db.progress.put({
          id: movie.tmdbId,
          userId: currentUserId,
          progress: movie.progress == -1 ? 0 : -1,
          synced: false
        }, { id: movie.tmdbId })

        const registration = await navigator.serviceWorker.ready;
        await registration.sync.register('syncProgress');

      } catch (error) { console.error(error) }

    } else {

      console.log('Offline sync not available, fallback to fetch.')

      fetch(`${import.meta.env.VITE_API_URL}/progress/movie/${movie.tmdbId}/${browser ? localStorage.getItem('user') : 1}`, {
				method: 'POST',
				headers: {'Content-Type': 'application/json'},
				body: JSON.stringify({progress: movie.tmdbId})
			})
      .then(result => result.json())
			.then(data => {
				if (data.status == 1) {
          db.progress.put({
            id: movie.tmdbId,
            userId: currentUserId,
            progress: movie.progress == -1 ? 0 : -1,
            synced: true
          }, { id: movie.tmdbId })
        }
      })
    }

  }

  $: percent = movieProgress == 0 ? 0 : movieProgress == -1 ? 100 : (movieProgress / movie.duration) * 100;
  $: formattedProgress = movieProgress < 3600 ? new Date(movieProgress * 1000).toISOString().substring(14, 19) : new Date(movieProgress * 1000).toISOString().substring(11, 19);
  $: movieProgress = $progress ? $progress.length > 0 ? $progress[0].synced == true ? $progress[0].progress : movie.progress : 0 : 0;
  $: movieProgressWaitingSync = $progress ? $progress.length > 0 ? $progress[0].synced == false : false : false;
  $: trailerUrl = currentLocale() == 'en' ? movie.trailers.en.length > 0 ? movie.trailers.en[0] : null : movie.trailers.fr.length > 0 ? movie.trailers.fr[0] : null

</script>

<div class="w-full h-full flex flex-col relative">
  <div class="relative h-full overflow-hidden select-none">

    <img
      alt=""
      src="{import.meta.env.VITE_API_URL}/images/movie/{movie.tmdbId}/backdrop/{currentLocale()}"
      draggable="false"
      class="w-full h-full object-top object-cover rounded-b-lg transition-all duration-300 ease-in-out {movieProgress == -1 ? "grayscale blur-[2px]" : ""}"
    />

    <div class="absolute bottom-0 left-0 right-0">
      <div class="{movieProgress == -1 ? "rounded-b-xl" : "rounded-bl-xl"} h-2 bg-indigo-700" style="width: {percent}%"/>
    </div>

    {#if trailerUrl != null}
      <div class="absolute top-0 bottom-0 right-0 left-0 flex items-center justify-center p-2">
        <div
          on:click={() => { playTrailer = true }}
          on:keypress={() => { playTrailer = true }}
          class="flex items-center justify-center bg-slate-700 rounded-lg bg-opacity-30 p-2 transition ease-in-out hover:scale-150 hover:p-4 group cursor-pointer"
        >
          {#if movieProgress == -1}
            <PlayIcon class="w-16 h-16 stroke-neutral-800 fill-neutral-800 transition ease-in-out group-hover:scale-0 group-hover:w-0 group-hover:h-0"/>
            <Replay class="w-0 h-0 scale-0 transition ease-in-out group-hover:scale-110 group-hover:w-16 group-hover:h-16 group-hover:fill-indigo-600 group-hover:stroke-indigo-600"/>
          {:else}
            <PlayIcon class="w-16 h-16 stroke-neutral-800 fill-neutral-800 transition ease-in-out group-hover:scale-110 group-hover:fill-indigo-600 group-hover:stroke-indigo-600"/>
          {/if}
        </div>
      </div>
    {/if}

    <div
      on:click={setAsWatched}
      on:keydown={setAsWatched}
      class="
        absolute bottom-0 right-0 m-6 w-14 h-12 bg-neutral-900 rounded-lg shadow-lg cursor-pointer
        flex flex-col items-center justify-center
        transition-all duration-300 ease-in-out hover:scale-105 group
      "
    >
      {#if movieProgressWaitingSync}
        <Loading class="stroke-neutral-400 h-8 w-8 cursor-not-allowed"/>
      {:else}
        <WatchedIcon class="w-8 h-8 {movieProgress == -1 ? 'stroke-neutral-400' : 'stroke-indigo-400'} transition-all duration-300 ease-in-out group-hover:opacity-0 group-hover:w-0 group-hover:h-0 group-hover:scale-0" />
        {#if movieProgress == -1}
          <Xmark class="fill-red-500 opacity-0 w-0 h-0 scale-0 transition-all duration-300 ease-in-out group-hover:opacity-100 group-hover:w-6 group-hover:h-6 group-hover:scale-100"/>
        {:else}
          <Checkmark class="fill-emerald-500 opacity-0 w-0 h-0 scale-0 transition-all duration-300 ease-in-out group-hover:opacity-100 group-hover:w-6 group-hover:h-6 group-hover:scale-100"/>
        {/if}
      {/if}
      <!-- <div class="
        text-white text-sm font-semibold
        opacity-0 w-0 h-0 group-hover:pl-3 group-hover:opacity-100 group-hover:w-full group-hover:h-full
      ">Mark as Watched</div> -->
    </div>

  </div>

  <!-- <div class="absolute w-full h-1/2 overflow-hidden p-2"> -->
    <!-- <img alt="" src="{import.meta.env.VITE_API_URL}/images/movie/{movie.tmdbId}/backdrop/{currentLocale()}" class="w-full h-full object-top object-cover rounded-lg"/> -->
    <!-- <div class="absolute text-white top-0 right-0 rounded-lg shadow-lg p-2 m-4 z-10 bg-red-700">Close</div> -->
  <!-- </div> -->

  <div class="flex px-5 items-top justify-between select-none">
    <div>
      <div class="text-neutral-200 text-2xl pt-5 font-bold">{localized(movie.title)}</div>
      <div class="text-neutral-500 text-sm pt-2 pl-1 font-semibold">{localized(movie.shortDesc)}</div>
    </div>
    <div class="flex pt-2 pr-2 gap-1">
      {#if movieProgress > 0}
        <div class="text-indigo-700 text-sm font-semibold">{formattedProgress}</div>
        <div class="text-neutral-400 text-sm font-semibold">/</div>
      {/if}
      <div class="{movieProgress == -1 ? "text-indigo-700" : "text-zinc-500"} text-sm font-semibold">{new Date(movie.duration * 1000).toISOString().substring(11, 19)}</div>
    </div>
  </div>

  <div class="w-full pl-5 pr-6 py-5 text-neutral-400 text-sm font-semibold">{localized(movie.desc)}</div>

  <!-- {#if movie.trailers.en.length > 0}
    <div class="h-[25%] px-4 pb-4 flex items-center justify-leading gap-4 overflow-x-auto">
      {#each movie.trailers.en as trailer, index}
        <iframe class="h-full rounded-xl aspect-video" src="https://www.youtube.com/embed/{trailer}" title={localized(movie.title)} frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      {/each}
    </div>
  {/if} -->
  <ActorsView
    actors={movie.actors}
  />

  <!-- <div class="w-full h-full select-none flex items-top justify-center">

    <div class="relative h-96 p-4 overflow-hidden flex items-center justify-center cursor-pointer transition group">
      <img
        alt=""
        src="{import.meta.env.VITE_API_URL}/images/movie/{movie.tmdbId}/poster/{currentLocale()}"
        draggable="false"
        class="w-auto max-h-96 object-top object-cover rounded-2xl group-hover:blur-[1px] transition ease-in-out group-hover:scale-105"
      />
      <div
        class="absolute flex items-center justify-center bg-slate-700 rounded-lg bg-opacity-30 p-2 transition ease-in-out
              group-hover:scale-150"
      >
        <PlayIcon
          class="w-16 h-16 stroke-neutral-800 fill-neutral-800 transition ease-in-out
                group-hover:scale-110 group-hover:fill-indigo-600 group-hover:stroke-indigo-600"
        />
      </div>
    </div>

    <div class="w-full flex pt-8 pl-4">

      <div class="w-full">
        c
      </div>
    </div>

  </div> -->
  {#if playTrailer && trailerUrl != null}
    <div class="absolute w-full h-full z-20">
      <iframe
        class="w-full h-full"
        src="https://www.youtube.com/embed/{trailerUrl}?rel=0&autoplay=1&vq=hd1080"
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen/>
    </div>

    <div class="absolute top-0 right-0 topSafeMargin z-50">
      <div
        on:click={() => { playTrailer = false }}
        on:keydown={() => { playTrailer = false }}
        class="text-white rounded-lg p-2 z-10 bg-red-700 cursor-pointer m-4"
      >
        Close
      </div>
    </div>
  {/if}

</div>
