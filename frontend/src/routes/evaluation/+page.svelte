<script>
	export let data;

	function sumScores(station_scores, fairness_score) {
		let sum = 0;
		for (let score of station_scores) {
			sum += score;
		}
		sum += fairness_score;
		return sum;
	}
</script>

<div class="container">
	<div class="col">
		<div class="row">
			<h2>Auswertung</h2>
		</div>
		<div class="row">
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
					{#each data.groups as group}
						<tr>
							<th>{group}</th>
							{#each data.group_scores[String(group)].station_scores as score}
								<td>{score}</td>
							{/each}
							<td>{data.group_scores[String(group)].fairness_score}</td>
							<th
								>{sumScores(
									data.group_scores[String(group)].station_scores,
									data.group_scores[String(group)].fairness_score
								)}</th
							>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>
