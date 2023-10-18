<script>
	import StationsTable from './StationsTable.svelte';

	export let data;
</script>

<div class="container">
	<div class="col">
		<div class="row">
			<h1>Punkteübersicht - {data.className} - Gruppe {data.groupNumber}</h1>
			<h2>Raum: {data.classData.room} - {data.classData.teacher}</h2>
		</div>
		<div class="row">
			<StationsTable
				stationsData={data.stationsData}
				stationScores={data.stationScores}
				fairnessScore={data.fairnessScore}
			/>
		</div>
	</div>
</div>
