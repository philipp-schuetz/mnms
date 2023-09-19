<script>
	import { onMount } from 'svelte';
	import { fetchData } from '../../api.js'

	let groups = [];
	let group_scores = {};
	let mounted = false;

	onMount(async () => {
		let group_scores_tmp;
		groups = await fetchData(`/groups/get-all`);
		for (let group of groups) {
			group_scores_tmp = await fetchData(`/groups/${group}/scores`);
			group_scores[group] = group_scores_tmp;
		}
		console.log(group_scores);
		console.log(group_scores['7midi-1'])
		mounted = true;
	});
</script>

<table class="table table-striped">
	<thead>
	  <tr>
		<th scope="col">Gruppe</th>
		<th scope="col">Station 1</th>
		<th scope="col">Station 2</th>
		<th scope="col">Station 3</th>
		<th scope="col">Station 4</th>
		<th scope="col">Station 5</th>
		<th scope="col">Station 6</th>
		<th scope="col">Fairness</th>
		<th scope="col">Gesamt</th>
	  </tr>
	</thead>
	<tbody>
		{#if mounted}
			{#each groups as group}
				<tr>
					<th>{group}</th>
					{#each group_scores[String(group)].station_scores as score}
						<td>{score}</td>
					{/each}
					<td>{group_scores[String(group)].fairness_score}</td>
					<th>0</th>
				</tr>
			{/each}
		{/if}
	</tbody>
</table>
