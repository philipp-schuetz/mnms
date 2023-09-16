<script>
	export let stationsData;

	let times = ['17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00'];
	let timesCount = 0;
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
				{#if station.name == 'allgemein-1'}
					<td colspan="3" class="bold">{station.subject} in der {station.room}</td>
				{:else if station.name == 'allgemein-2'}
					<td colspan="3" class="bold">{station.subject} auf dem {station.room}</td>
				{:else}
					<td>{station.subject}</td>
					<td>{station.room}</td>
					<td>Placeholder: 0</td>
				{/if}
			</tr>
		{/each}
	</tbody>
</table>
