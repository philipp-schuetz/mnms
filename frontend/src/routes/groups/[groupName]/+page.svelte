<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import StationsTable from './StationsTable.svelte';
	import ParticipantsTable from './ParticipantsTable.svelte';

	const groupName = $page.params.groupName;
	const className = groupName.replace(/-\d$/, '')

	let stationsData = [];
	let classData = {};
	let participantsData = [];
	let scoreData = {};

	onMount(async () => {
		const data = await getData(`/groups/${groupName}/stations`);
		stationsData = data.stations;
		classData = await getData(`/classes/info?class_name=${className}`);
		participantsData = await getData(`/groups/${groupName}/participants`);
		console.log(participantsData)
		scoreData = await getData(`/groups/${groupName}/scores`);
	});
</script>
<div class="container">
	<div class="row">
	  <div class="col">
		<StationsTable {stationsData} {scoreData} />
	  </div>
	  <div class="col">
		<span class="bold">Klassenraum:</span> {classData.room} <br>
		<span class="bold">KlassenlehrerIn:</span> {classData.teacher}
		<ParticipantsTable />
	  </div>
	</div>
  </div>
<style>
	.bold {
		font-weight: bold;
	}
</style>
