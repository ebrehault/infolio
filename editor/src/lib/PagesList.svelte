<script lang="ts">
  import { deletePage, publishPage } from './core.svelte';
  import { getState } from './store.svelte';

  let pages = $derived(getState().pages);

  function publish(id: string) {
    const path = id; // TODO: support nested pages
    if (path) {
      publishPage(path);
    }
  }
</script>

{#if pages.length > 0}
  <h2 class="text-2xl">Pages</h2>
  <ul>
    {#each pages as page}
      <li>
        <a href={page.id}>{page.title} ({page.id})</a>
        <button onclick={() => deletePage(page.id)}>Delete</button>
        <button onclick={() => publish(page.id)}>Publish</button>
      </li>
    {/each}
  </ul>
{/if}
