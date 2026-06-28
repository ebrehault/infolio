<script lang="ts">
  import Logo from './components/Logo.svelte';
  import { getState } from './store.svelte';

  let username = $derived(getState().username);
</script>

<header class="sticky top-0 left-0 right-0 z-1 bg-indigo-900 text-white h-15 flex items-center px-4">
  <Logo />
  <h1 class="text-3xl">Infolio</h1>
  {#if username}
    <div><a href="/">@{username}</a></div>
  {:else}
    <div>Logged out</div>
  {/if}
</header>
