<script>
	export let groupName;

	import { onMount } from 'svelte';
	import { fetchData } from '../../../api.js'

	let stationsData = [];
	let stationScores = [];
	let fairnessScore = 0;

	onMount(async () => {
		const data = await fetchData(`/groups/${groupName}/stations`);
		stationsData = data.stations;
		const scoreData = await fetchData(`/groups/${groupName}/scores`);
		stationScores = scoreData.station_scores;
		fairnessScore = scoreData.fairness_score;
	});

	let times = ['17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00'];
	let timesCount = 0;

	function scoreIncrement(station_number) {
		if (stationScores[station_number] < 5) {
			stationScores[station_number] += 1;
		}
	}
	function scoreDecrement(station_number) {
		if (stationScores[station_number] > 0) {
			stationScores[station_number] -= 1;
		}
	}

</script>

<table class="table table-striped">
	<thead>
	  <tr>
		<th scope="col">Zeit</th>
		<th scope="col">Station</th>
		<th scope="col">Raum</th>
		<th scope="col">Punkte</th>
	  </tr>
	</thead>
	<tbody>
		{#each stationsData as station (station.name)}
			<tr>
				<th scope="row">{times[timesCount]}</th>
				{#if station.name === 'allgemein-1'}
					<td colspan="3" class="bold">{station.subject} in der {station.room}</td>
				{:else if station.name === 'allgemein-2'}
					<td colspan="3" class="bold">{station.subject} auf dem {station.room}</td>
				{:else}
					<td>{station.subject}</td>
					<td>{station.room}</td>
					<td>
						{stationScores[0]}
						<button type="button" class="btn btn-primary" on:click={scoreDecrement(0)}>-</button>
						<button type="button" class="btn btn-primary" on:click={scoreIncrement(0)}>+</button>
					</td>
				{/if}
			</tr>
		{/each}
	</tbody>
</table>
