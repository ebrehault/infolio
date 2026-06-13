<script lang="ts">
  import { onMount } from 'svelte';
  import { getPath, getState } from './lib/store.svelte';
  import TopNav from './lib/TopNav.svelte';
  import { initNavigation } from './navigation';
  import { API } from './lib/api';
  import { addPage, createAccount, deletePage, initLogin, loadPages } from './core.svelte';

  let hasAccount = $state(false);

  let mastodons = $derived(getState().mastodons);
  let pages = $derived(getState().pages);
  $effect(() => {
    if (getState().username) {
      API.getAccount().then((res) => {
        hasAccount = res.success;
      });
      loadPages();
    }
  });
  onMount(() => {
    initNavigation();
    initLogin();
  });

  function login(instance: string) {
    API.setInstance(instance);
    location.href = API.getLoginUrl(instance);
  }
</script>

<div>
  <TopNav></TopNav>
  <main class="text-gray-900 dark:text-white">
    <div>
      <a href="/test">Test</a>
      Path = {getPath()}
    </div>
    <div>
      {#if !hasAccount}
        <button onclick={() => createAccount()}>Create account</button>
      {:else}
        <button onclick={() => addPage()}>Add page</button>
      {/if}
    </div>
    {#if mastodons.length > 0}
      <h2>Instances</h2>
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
      <h2>Pages</h2>
      <ul>
        {#each pages as page}
          <li>
            {page.title} ({page.id})
            <button onclick={() => deletePage(page.id)}>Delete</button>
          </li>
        {/each}
      </ul>
    {/if}
  </main>
</div>
