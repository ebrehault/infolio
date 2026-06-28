<script lang="ts">
  import { onMount } from 'svelte';
  import { getPath, getState } from './lib/store.svelte';
  import TopNav from './lib/TopNav.svelte';
  import { initNavigation } from './navigation';
  import { API } from './lib/api';
  import {
    addPage,
    createAccount,
    deletePage,
    editPage,
    getPage,
    initLogin,
    loadPages,
    publishPage,
  } from './core.svelte';

  let hasAccount = $state(false);
  let body = $state('');
  let viewLink = $state('');
  let mastodons = $derived(getState().mastodons);
  let pages = $derived(getState().pages);
  let currentPage = $derived(getState().currentPage);
  $effect(() => {
    if (getState().username) {
      API.getAccount().then((res) => {
        hasAccount = res.success;
      });
      loadPages();
    }
  });
  $effect(() => {
    if (getPath() !== '') {
      getPage(getPath());
    }
  });
  $effect(() => {
    body = currentPage?.body || '';
    viewLink = currentPage?.['@id'] || '';
  });
  onMount(() => {
    initNavigation();
    initLogin();
  });

  function login(instance: string) {
    API.setInstance(instance);
    location.href = API.getLoginUrl(instance);
  }

  function save() {
    const path = getPath();
    if (path) {
      editPage(path, { body });
    }
  }
  function publish() {
    const path = getPath();
    if (path) {
      publishPage(path);
    }
  }
</script>

<div>
  <TopNav></TopNav>
  <main class="text-gray-900 dark:text-white">
    {#if getPath() === ''}
      <h1 class="text-3xl">Home</h1>
      <div>
        {#if !hasAccount}
          <button onclick={() => createAccount()}>Create account</button>
        {:else}
          <button onclick={() => addPage()}>Add page</button>
        {/if}
      </div>
      {#if mastodons.length > 0}
        <h2 class="text-2xl">Instances</h2>
        <ul>
          {#each mastodons as instance}
            <li>
              {instance.id}
              <button onclick={() => login(instance.id)}>Login</button>
            </li>
          {/each}
        </ul>
      {/if}

      {#if pages.length > 0}
        <h2 class="text-2xl">Pages</h2>
        <ul>
          {#each pages as page}
            <li>
              <a href={page.id}>{page.title} ({page.id})</a>
              <button onclick={() => deletePage(page.id)}>Delete</button>
              <button onclick={() => publishPage(page.id)}>Publish</button>
            </li>
          {/each}
        </ul>
      {/if}
    {:else if currentPage}
      <h1 class="text-3xl">{currentPage.title}</h1>
      <a
        href={viewLink}
        target="_blank"
      >
        Link
      </a>
      <textarea bind:value={body}></textarea>

      <button onclick={() => save()}>Save</button>
    {:else}
      Unknown content
    {/if}
  </main>
</div>
