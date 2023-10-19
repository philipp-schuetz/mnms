<script>
	import ParticipantsTable from './ParticipantsTable.svelte';

	export let data;
</script>

<div class="container">
	<div class="col">
		<div class="row">
			<h2>Anwesenheit - {data.className} - Gruppe {data.groupNumber}</h2>
		</div>
		<div class="row">
			<ParticipantsTable participantsData={data.participantsData} />
		</div>
	</div>
</div>
