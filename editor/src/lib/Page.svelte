<script lang="ts">
  import { editPage } from './core.svelte';
  import { getPath, getState } from './store.svelte';

  let currentPage = $derived(getState().currentPage);
  let body = $state('');
  let viewLink = $state('');

  $effect(() => {
    body = currentPage?.body || '';
    viewLink = currentPage?.['@id'] || '';
  });

  function save() {
    const path = getPath();
    if (path) {
      editPage(path, { body });
    }
  }
</script>

{#if currentPage}
  <h1 class="text-3xl">{currentPage.title}</h1>
  <a
    href={viewLink}
    target="_blank"
  >
    Link
  </a>
  <textarea bind:value={body}></textarea>

  <button onclick={() => save()}>Save</button>
{/if}
