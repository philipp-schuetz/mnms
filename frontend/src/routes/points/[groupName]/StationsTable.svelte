<script>
	export let stationsData;
	export let stationScores;
	export let fairnessScore;
	export let groupName;

	import { onMount } from 'svelte';

	import { env } from '$env/dynamic/public';

	let mounted = false;
	let isConnected = false;

	let showWarning = false;

	$: {
		if (mounted) {
			if (isConnected) {
				putScores(stationScores, fairnessScore);
			}
		}
	}

	onMount(async () => {
		mounted = true;

		isConnected = navigator.onLine;
		window.addEventListener('online', () => {
			console.log('online');
			isConnected = true;
			showWarning = false;
		});
		window.addEventListener('offline', () => {
			console.log('offline');
			isConnected = false;
			showWarning = true;
		});

		window.addEventListener('beforeunload', (event) => {
			if (!isConnected) {
				event.preventDefault();
				event.returnValue =
					'You have unsaved data. Are you sure you want to leave?';
			}
		});
	});

	let times = [
		'17:30',
		'18:00',
		'18:30',
		'19:00',
		'19:30',
		'20:00',
		'20:30',
		'21:00',
	];

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

	async function putScores(stationScores, fairnessScore) {
		const url = `${env.PUBLIC_API_PATH}/groups/${groupName}/scores?fairness=${fairnessScore}`;
		const requestOptions = {
			method: 'PUT',
			body: JSON.stringify(stationScores),
			headers: {
				'Content-Type': 'application/json',
			},
		};
		try {
			const response = await fetch(url, requestOptions);
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			const data = await response.json();
			return data;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
</script>

{#if showWarning}
	<div class="warning">
		<p>
			By leaving the site data could be lost due to missing network connection.
		</p>
	</div>
{/if}

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
					<td
						colspan="3"
						class="bold">{station.subject} in der {station.room}</td
					>
				{:else if station.name === 'allgemein-2'}
					<td
						colspan="3"
						class="bold">{station.subject} auf dem {station.room}</td
					>
				{:else}
					<td>{station.subject}</td>
					<td>{station.room}</td>
					<td>
						{#if index < 5}
							{stationScores[index]}<br />
							<button
								type="button"
								class="btn btn-primary"
								on:click={() => scoreChange(index, false)}>-</button
							>
							<button
								type="button"
								class="btn btn-primary"
								on:click={() => scoreChange(index, true)}>+</button
							>
						{:else}
							{stationScores[index - 2]}<br />
							<button
								type="button"
								class="btn btn-primary"
								on:click={() => scoreChange(index - 2, false)}>-</button
							>
							<button
								type="button"
								class="btn btn-primary"
								on:click={() => scoreChange(index - 2, true)}>+</button
							>
						{/if}
					</td>
				{/if}
			</tr>
			{#if index === 7}
				<tr>
					<td colspan="4">
						Fairness Punkte: {fairnessScore}
						<button
							type="button"
							class="btn btn-primary"
							on:click={() => {
								if (fairnessScore > 0) {
									fairnessScore -= 1;
								}
							}}>-</button
						>
						<button
							type="button"
							class="btn btn-primary"
							on:click={() => {
								if (fairnessScore < 3) {
									fairnessScore += 1;
								}
							}}>+</button
						>
					</td>
				</tr>
			{/if}
		{/each}
	</tbody>
</table>
