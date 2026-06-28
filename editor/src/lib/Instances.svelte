<script lang="ts">
  import { API } from './api';
  import { getState } from './store.svelte';

  let mastodons = $derived(getState().mastodons);

  function login(instance: string) {
    API.setInstance(instance);
    location.href = API.getLoginUrl(instance);
  }
</script>

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
