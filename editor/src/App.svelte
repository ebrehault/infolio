<script lang="ts">
  import { onMount } from 'svelte';
  import { getPath, getState } from './lib/store.svelte';
  import TopNav from './lib/TopNav.svelte';
  import { initNavigation } from './lib/navigation';
  import { API } from './lib/api';
  import { addPage, createAccount, getPage, initLogin, loadPages } from './lib/core.svelte';
  import Page from './lib/Page.svelte';
  import PagesList from './lib/PagesList.svelte';
  import Instances from './lib/Instances.svelte';

  let hasAccount = $state(false);
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
  onMount(() => {
    initNavigation();
    initLogin();
  });
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
      <Instances></Instances>

      <PagesList></PagesList>
    {:else if currentPage}
      <Page></Page>
    {:else}
      Unknown content
    {/if}
  </main>
</div>
