<script lang="ts">

  import { onMount } from "svelte";

  import type { Movie } from "../libs/interfaces/Movie";
  import type { Progress } from "../libs/interfaces/Progress";

  import { liveQuery } from "dexie";
  import { db, type DBProgress, type DBUser } from "../libs/db";
  import { browser } from "$app/environment";
  import { language } from "../libs/languageStore";
  import { userId } from "../libs/userStore";

  import OpenedPage from "../libs/OpenedPage.svelte";
  import ItemPoster from "../libs/ItemPoster.svelte";
  import ItemBackdrop from "../libs/ItemBackdrop.svelte";
	import UserIcon from "../libs/icons/UserIcon.svelte";
	import FilterIcon from "../libs/icons/FilterIcon.svelte";
  import SearchIcon from "../libs/icons/SearchIcon.svelte";
	import Xmark from "../libs/icons/Xmark.svelte";

  import { localized } from "../libs/functions/localized";

  let movies: Movie[] = [];

  let availableMovies: Movie[] = [];
  let filteredMovies: Movie[] = [];

  let currentLanguage: String = 'en';
  language.subscribe(value => { currentLanguage = value });
  let currentUserId: number = 0;
  userId.subscribe(value => { currentUserId = parseInt(value) });

  let opened: Movie | null = null;
  let newSearch: string | null;

  let openPersonnalPanel = false;

  let currentSearch = '';
  let isScrolled = false;
  let isOnlyAnime = "A";

  let progress = liveQuery(() => browser ? db.progress.toArray() : []);

  function urlB64ToUint8Array(base64String: any) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  function updateSubscriptionOnServer(subscription: PushSubscription) {
    console.log(subscription);
    return fetch(`${import.meta.env.VITE_API_URL}/push/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        subscription: JSON.stringify(subscription)
      })
    });

  }

  async function subscribeUser() {

    const reg = await navigator.serviceWorker.ready;
    let applicationServerPublicKey = urlB64ToUint8Array('BDdh4KdRY-PEd1X2wpDLDPRyOw7eZE3OSveTDnT7vTcJsANJe2qy5ocEijtYEcg-wNXAcULJjClzPSioJvM3yNc');
    reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: applicationServerPublicKey})
    .then(subscription => {
      console.log('User is subscribed.');
      return updateSubscriptionOnServer(subscription);
    })
    .then(response => {
      if (!response.ok) throw new Error('Bad status code from server.');
      return response.json();
    })
    .then(responseData => {
      console.log(responseData);
      if (responseData.status !== 1) throw new Error('Bad response from server.');
    })
    .catch(err => {
      console.log('Failed to subscribe the user: ', err);
      console.log(err.stack);
    })

    const status = await Notification.requestPermission();
    if (status !== 'granted') alert('Please allow notifications to witness the full potential of this EpitechNinja demo.')
  }

  onMount(async () => {

    subscribeUser();

    try {

      const res = await fetch(`${import.meta.env.VITE_API_URL}/movies/`)
      let jsonResult = await res.json()
      if (jsonResult.movies.length > 0) movies = jsonResult.movies;

      const progressRes = await fetch(`${import.meta.env.VITE_API_URL}/progress/${currentUserId}`)
      let jsonProgressResult = await progressRes.json()

      await db.currentUser.put({
        id: 0,
        userId: currentUserId
      }, { id: 0 })

      db.progress.clear();
      for (let index in (jsonProgressResult.movies as Progress)) {
        let id = parseInt(jsonProgressResult.movies[index].tmdbId);
        let progress = jsonProgressResult.movies[index].progress;
        await db.progress.put({
          id: id,
          userId: currentUserId,
          progress: progress,
          synced: true
        }, { id: id })
      }

      movies = movies.sort((a, b) => { return a.popularity > b.popularity ? -1 : 1 });

      availableMovies = movies;
      filteredMovies = availableMovies;

    } catch(error) { console.log(error)}

  });

  function setIsScrolled(e: any) {
    isScrolled = e.target.scrollTop > 50
  }

  function toggleAnimeOnly() {
    // A = All | N = Regular | M = Anime
    if (isOnlyAnime == 'N') {
      availableMovies = movies
      filterMovies()
      isOnlyAnime = 'A'
    } else if (isOnlyAnime == 'A') {
      availableMovies = movies.filter((item) => {
        return item.vo == 'ja' && item.genres.includes('Animation')
      })
      filterMovies();
      isOnlyAnime = 'M'
    } else {
      availableMovies = movies.filter((item) => {
        return !item.genres.includes('Animation')
      })
      filterMovies();
      isOnlyAnime = 'N'
    }
  }

  function filterMovies() {
    filteredMovies = availableMovies.filter(item => localized(item.title).toLowerCase().includes(currentSearch.toLowerCase()));
  }

  // $: filteredItems = filterMovies(availableItems, currentSearch);
  $: currentSearch, filterMovies();

  function updateMovies(movies: Movie[]) {
    availableMovies = movies
    filterMovies();
  }

  // function updateItem(item: Movie | null) {
  //   if (item == null) return
  //   const index = availableMovies.findIndex(x => x.tmdbId == item.tmdbId)
  //   if (index >= 0) availableMovies[index] = item;
  //   filterMovies();

  //   // save on indexedDB
  // }

  function updateProgress(progress: DBProgress[]) {
    let moviesCPY = movies;
    for (let index in moviesCPY) {
      const movieProgress = progress.find(element => element.id == moviesCPY[index].tmdbId && element.synced);
      if (movieProgress != undefined) moviesCPY[index].progress = movieProgress.progress
      else moviesCPY[index].progress = 0  // moviesCPY[index].progress != undefined ? moviesCPY[index].progress : 0
    }
    movies = moviesCPY;
    updateMovies(movies);
  }

  function clickSearch() {
    if (newSearch == currentSearch) { currentSearch = ''; newSearch = null }
    else if (newSearch) { newSearch = null ; setTimeout(() => {newSearch = currentSearch}, 120)}
    else newSearch = currentSearch;
    filterMovies()
  }

  // $: opened, updateItem(opened);
  $: movies, updateMovies(movies);
  $: $progress, updateProgress($progress);

  async function fetchUserProgress(newId: number) {

    if (browser) {

      try {
        await db.currentUser.put({
          id: 0,
          userId: newId
        }, { id: 0 })

      } catch(error) { console.log(error)}

      try {
        const progressRes = await fetch(`${import.meta.env.VITE_API_URL}/progress/${newId}`)
        let jsonProgressResult = await progressRes.json()

        db.progress.clear();
        for (let index in (jsonProgressResult.movies as Progress)) {
          let id = parseInt(jsonProgressResult.movies[index].tmdbId);
          let progress = jsonProgressResult.movies[index].progress;
          await db.progress.put({
            id: id,
            userId: currentUserId,
            progress: progress,
            synced: true
          }, { id: id })
        }

        updateProgress($progress)
      } catch(error) { console.error(error) }
    }
  }

  $: currentUserId, fetchUserProgress(currentUserId);

</script>

<main class="w-screen h-screen flex items-center bg-slate-900 relative">
  <div on:scroll={setIsScrolled} class="w-full h-full overflow-y-auto" style="-webkit-overflow-scrolling: touch;">

    <div class="fixed w-full flex items-center justify-end z-40 my-4 pl-5 pr-5 sm:pr-10 topSafePadding">

      <div
        on:click={toggleAnimeOnly}
        on:keydown={toggleAnimeOnly}
        class="p-[10px] bg-violet-100 rounded-lg shadow sm:hover:scale-105 active:scale-[0.8] cursor-pointer transition-all duration-300 select-none dark:bg-slate-800"
      >
        {#if isOnlyAnime == 'A'}
				  <FilterIcon class="stroke-violet-700 dark:stroke-violet-200" />
        {:else}
          <div class="w-6 h-6 flex items-center justify-center text-white font-semibold text-xl">{isOnlyAnime == 'M' ? 'A' : 'N'}</div>
        {/if}
			</div>

      {#if isScrolled}
        <div class="flex-grow"/>
      {/if}

      <input
        id="searchInput"
        bind:value={currentSearch}
        on:keypress={(e) => {e.key == 'Enter' && newSearch != currentSearch ? clickSearch() : null}}
        placeholder="Filter"
        style="-webkit-appearance: none"
        class="border-none focus:border-none focus:ring-0
          text-lg font-semibold min-w-0 {isScrolled ? "" : "w-full"} mx-3 antialiased shadow-lg rounded-lg py-2 px-3 bg-violet-100 placeholder-slate-300
          transition-all duration-300 ease-in-out text-indigo-500 dark:bg-slate-800"
			/>

      <div
        on:click={clickSearch}
        on:keypress={clickSearch}
        class="bg-violet-100 rounded-lg shadow sm:hover:scale-105 active:scale-[0.8] cursor-pointer transition-all duration-300 ease-in-out select-none dark:bg-slate-800
          {currentSearch.length > 0 ? 'w-11 h-11 p-[10px] mr-3 flex items-center justify-center' : 'w-0 h-0 scale-0'}"
      >
				<SearchIcon class="stroke-violet-700 dark:stroke-violet-200 {newSearch == currentSearch ? 'w-0 h-0 scale-0' : ''} transition-all duration-300 ease-in-out" />
        <Xmark class="fill-red-500 {newSearch == currentSearch ? '' : 'w-0 h-0 scale-0'} transition-all duration-300 ease-in-out" />
			</div>

      <div
        on:click={() => { openPersonnalPanel = true}}
        on:keypress={() => { openPersonnalPanel = true}}
        class="p-[10px] bg-violet-100 rounded-lg shadow sm:hover:scale-105 active:scale-[0.8] cursor-pointer transition-all duration-300 select-none dark:bg-slate-800"
      >
				<UserIcon class="stroke-violet-700 dark:stroke-violet-200" />
			</div>

    </div>

    {#if availableMovies.length > 0}
      <div class="pl-2 pr-3 pt-[74px] {opened != null ? "h-0" : ""} topSafeMargin">
        {#if filteredMovies.filter(x => x.progress > 0).length > 0}
          <div class="grid grid-cols-watchingMobileGrid sm:grid-cols-watchingWebGrid w-full h-content {opened ? 'pointer-events-none' : ''}">
            {#each filteredMovies.filter(x => x.progress > 0) as show}
              <ItemBackdrop
                openItem={() => {opened = show}}
                item={show}
              />
            {/each}
          </div>
        {/if}

        {#if filteredMovies.filter(x => x.progress == 0).length > 0}
          <div class="text-3xl dark:text-gray-200 font-bold pl-3 py-4 antialiased">{currentLanguage == 'en' ? 'Not watched' : 'Non regardés'}</div>
          <div class="grid grid-cols-mobileGrid sm:grid-cols-WebGrid w-full h-content {opened ? 'pointer-events-none' : ''}">
            {#each filteredMovies.filter(x => x.progress == 0) as show}
              <ItemPoster
                openItem={() => {opened = show}}
                item={show}
              />
            {/each}
          </div>
        {/if}

        {#if filteredMovies.filter(x => x.progress == -1).length > 0}
          <div class="text-3xl dark:text-gray-200 font-bold pl-3 py-4 antialiased">{currentLanguage == 'en' ? 'Watched' : 'Regardés'}</div>
          <div class="grid grid-cols-mobileGrid sm:grid-cols-WebGrid w-full h-content {opened ? 'pointer-events-none' : ''}">
            {#each filteredMovies.filter(x => x.progress == -1) as show}
              <ItemPoster
                openItem={() => {opened = show}}
                item={show}
              />
            {/each}
          </div>
        {/if}
      </div>

    {:else}
      <div class="w-full h-full flex items-center justify-center text-3xl text-white font-bold topSafeMargin">Loading..</div>
    {/if}

  </div>

  {#if opened != null}
    <OpenedPage
      bind:item={opened}
    />
  {/if}

  <div
    id="personalBarBackground"
    on:click={(e) => { if (e.target?.id == 'personalBarBackground') openPersonnalPanel = false }}
    on:keypress={() => console.log('close')}
    class="fixed z-[60] top-0 bottom-0 right-0 left-0 bg-neutral-900/40 flex items-end justify-end transition-all duration-300 ease-in-out {openPersonnalPanel ? '' : 'select-none opacity-0 w-0'}"
  >
    <div class="h-full {openPersonnalPanel ? 'w-[80%] sm:w-[440px]' : 'w-0'} rounded-l-xl shadow-xl shadow-neutral-900 bg-neutral-900 overflow-clip transition-all duration-300 ease-in-out flex flex-col items-center">

      <div class="w-full flex items-center justify-between px-4 pt-4">
        <div class="text-xl text-white font-semibold">Epitech Ninja</div>

        <div
          on:click={() => { language.update(value => { return value == 'en' ? 'fr' : 'en' }) }}
          on:keypress={() => { }}
          class="w-10 h-10 flex items-center justify-center bg-neutral-800 cursor-pointer rounded-md select-none hover:scale-105 active:scale-75"
        >
          <div class="text-indigo-300 font-bold">{currentLanguage.toUpperCase()}</div>
        </div>
      </div>

      <div class="w-full p-4">
        <div
          on:click={() => { userId.set("0") }}
          on:keypress={() => { userId.set("0") }}
          class="w-full h-32 rounded-lg flex items-center justify-center text-white font-semibold select-none
          {currentUserId == 0 ? 'bg-indigo-400' : 'bg-neutral-800 hover:scale-105 hover:bg-neutral-700 cursor-pointer active:scale-95'}"
        >
          Admin
        </div>
      </div>

      <div class="w-full flex justify-evenly gap-4 px-4">
        <div
          on:click={() => { userId.set("1") }}
          on:keypress={() => { userId.set("1") }}
          class="w-full aspect-square rounded-lg flex items-center justify-center text-white font-semibold select-none
          {currentUserId == 1 ? 'bg-indigo-400' : 'bg-neutral-800 hover:scale-105 hover:bg-neutral-700 cursor-pointer active:scale-95'}"
        >
          Mathieu
        </div>

        <div
          on:click={() => { userId.set("2") }}
          on:keypress={() => { userId.set("2") }}
          class="w-full aspect-square rounded-lg flex items-center justify-center text-white font-semibold select-none
          {currentUserId == 2 ? 'bg-indigo-400' : 'bg-neutral-800 hover:scale-105 hover:bg-neutral-700 cursor-pointer active:scale-95'}"
        >
          Thomas
        </div>
      </div>

    </div>
  </div>

</main>
