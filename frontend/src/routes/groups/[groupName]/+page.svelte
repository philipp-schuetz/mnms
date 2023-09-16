<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { env } from '$env/dynamic/public';

	const groupName = $page.params.groupName;
	const className = groupName.replace(/-\d$/, '')

	async function getData(url) {
		try {
			const response = await fetch(`${env.PUBLIC_API_PATH}${url}`);
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			const data = await response.json();
			return data;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	let stationsData = [];
	let classData = {};

	onMount(async () => {
		const data = await getData(`/groups/${groupName}/stations`);
		stationsData = data.stations;
		classData = await getData(`/classes/info?class_name=${className}`);
	});
</script>

{#each stationsData as station (station.name)}
<p>
	Station: {station.subject}<br>
	Raum: {station.room}
</p>
{/each}

{classData.room}, {classData.teacher}
