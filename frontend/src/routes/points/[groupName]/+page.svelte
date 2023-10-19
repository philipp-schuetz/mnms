<script>
	import StationsTable from './StationsTable.svelte';

	export let data;
</script>

<div class="container">
	<div class="col">
		<div class="row">
			<h2>Punkteübersicht - {data.className} - Gruppe {data.groupNumber}</h2>
			<h3>Raum {data.classData.room} - {data.classData.teacher}</h3>
		</div>
		<div class="row">
			<StationsTable
				stationsData={data.stationsData}
				stationScores={data.stationScores}
				fairnessScore={data.fairnessScore}
				groupName={data.groupName}
			/>
		</div>
	</div>
</div>
