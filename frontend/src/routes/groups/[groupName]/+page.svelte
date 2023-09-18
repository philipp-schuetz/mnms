<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { fetchData } from '../../../api.js'
	import StationsTable from './StationsTable.svelte';

	const groupName = $page.params.groupName;
	const className = groupName.replace(/-\d$/, '')

	let classData = {};

	onMount(async () => {
		classData = await fetchData(`/classes/info?class_name=${className}`);
	});
</script>
<div class="container">
	<div class="row">
	  <div class="col">
		<StationsTable {groupName} />
	  </div>
	  <div class="col">
		<span class="bold">Klassenraum:</span> {classData.room} <br>
		<span class="bold">KlassenlehrerIn:</span> {classData.teacher}
	  </div>
	</div>
  </div>
<style>
	.bold {
		font-weight: bold;
	}
</style>
