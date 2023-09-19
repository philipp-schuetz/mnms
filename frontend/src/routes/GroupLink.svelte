<script>
	import { onMount } from 'svelte';
	import { fetchData } from '../api.js'

	export let baseUrl;

	let groups = [];

	onMount(async () => {
		groups = await fetchData(`/groups/get-all`);
	});
</script>
{#each groups as group}
	<a href="/{baseUrl}/{group}">{group}</a><br>
{/each}
