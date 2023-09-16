<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { env } from '$env/dynamic/public';
	import StationsTable from './StationsTable.svelte';
	import ParticipantsTable from './ParticipantsTable.svelte';

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
	let participantsData = [];

	onMount(async () => {
		const data = await getData(`/groups/${groupName}/stations`);
		stationsData = data.stations;
		classData = await getData(`/classes/info?class_name=${className}`);
		participantsData = await getData(`/groups/${groupName}/participants`);
	});
</script>
<div class="container">
	<div class="row">
	  <div class="col">
		<StationsTable {stationsData} />
	  </div>
	  <div class="col">
		<span class="bold">Klassenraum:</span> {classData.room} <br>
		<span class="bold">KlassenlehrerIn:</span> {classData.teacher}
		<ParticipantsTable {participantsData} />
	  </div>
	</div>
  </div>
<style>
	.bold {
		font-weight: bold;
	}
</style>
