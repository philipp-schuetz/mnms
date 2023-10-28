<script>
	import { onMount } from 'svelte';
	import { env } from '$env/dynamic/public';

	export let baseUrl;

	let groups = [];
	onMount(async () => {
		const response = await fetch(`${env.PUBLIC_API_PATH}/groups/get-all`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
		});
		groups = await response.json();
	});
</script>

{#each groups as group}
	<a href="/{baseUrl}/{group}">{group}</a><br />
{/each}
