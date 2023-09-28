<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { fetchData } from '../../../api.js';
	import StationsTable from './StationsTable.svelte';

	const groupName = $page.params.groupName;
	const className = groupName.replace(/-\d$/, '');

	let classData = {};

	onMount(async () => {
		classData = await fetchData(`/classes/info?class_name=${className}`);
	});
</script>

<div class="container">
	<div class="col">
		<div class="row">
			<span class="bold">Klassenraum: {classData.room}</span>
			<span class="bold">KlassenlehrerIn: {classData.teacher}</span>
		</div>
		<div class="row">
			<StationsTable {groupName} />
		</div>
	</div>
</div>

<style>
	.bold {
		font-weight: bold;
	}
</style>
