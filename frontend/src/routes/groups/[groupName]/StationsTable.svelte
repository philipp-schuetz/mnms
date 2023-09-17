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

	/**
	 * @param {int} station_index
	 * @param {boolean} increment
	 */
	function scoreChange(station_index, increment) {
		if (increment && stationScores[station_index] < 5) {
			stationScores[station_index] += 1;
		} else if (!increment && stationScores[station_index] > 0) {
			stationScores[station_index] -= 1;
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
		{#each stationsData as station, index (station.name)}
			<tr>
				<th scope="row">{times[index]}</th>
				{#if station.name === 'allgemein-1'}
					<td colspan="3" class="bold">{station.subject} in der {station.room}</td>
				{:else if station.name === 'allgemein-2'}
					<td colspan="3" class="bold">{station.subject} auf dem {station.room}</td>
				{:else}
					<td>{station.subject}</td>
					<td>{station.room}</td>
					<td>
						{#if index < 5}
							{stationScores[index]}
							<button type="button" class="btn btn-primary" on:click={() => scoreChange(index, false)}>-</button>
							<button type="button" class="btn btn-primary" on:click={() => scoreChange(index, true)}>+</button>
						{:else}
							{stationScores[index-2]}
							<button type="button" class="btn btn-primary" on:click={() => scoreChange(index-2, false)}>-</button>
							<button type="button" class="btn btn-primary" on:click={() => scoreChange(index-2, true)}>+</button>
						{/if}
					</td>
				{/if}
			</tr>
		{/each}
	</tbody>
</table>
