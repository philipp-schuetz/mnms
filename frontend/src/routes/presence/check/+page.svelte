<script>
	import { onMount } from 'svelte';
	import { fetchData } from '../../../api.js';

	let participantsData = [];
	let not_present_switch = false;

	onMount(async () => {
		participantsData = await fetchData(`/participants/get-all`);
		participantsData = sortByGroup(participantsData);
	});

	function sortByGroup(persons) {
		return persons.sort((a, b) => {
			if (a.group < b.group) {
				return -1;
			}
			if (a.group > b.group) {
				return 1;
			}
			return 0;
		});
	}
</script>

<div class="container">
	<div class="col">
		<div class="row">
			<h2>Anwesenheit - Alle Klassen</h2>
		</div>
		<div class="row">
			<button
				type="button"
				class="btn btn-primary"
				on:click={() => (not_present_switch = !not_present_switch)}
			>
				{#if not_present_switch}
					Abwesend
				{:else}
					Alle
				{/if}
			</button>
			<table class="table table-striped">
				<thead>
					<tr>
						<th scope="col">Gruppe</th>
						<th scope="col">Vorname</th>
						<th scope="col">Nachname</th>
						<th scope="col">Anwesend</th>
					</tr>
				</thead>
				<tbody>
					{#each participantsData as participant}
						{#if not_present_switch}
							{#if !participant.present}
								<tr>
									<td>{participant.group}</td>
									<td>{participant.firstname}</td>
									<td>{participant.lastname}</td>
									<td>
										<div class="form-check">
											<input
												class="form-check-input"
												type="checkbox"
												bind:checked={participant.present}
												disabled
											/>
										</div>
									</td>
								</tr>
							{/if}
						{:else}
							<tr>
								<td>{participant.group}</td>
								<td>{participant.firstname}</td>
								<td>{participant.lastname}</td>
								<td>
									<div class="form-check">
										<input
											class="form-check-input"
											type="checkbox"
											bind:checked={participant.present}
											disabled
										/>
									</div>
								</td>
							</tr>
						{/if}
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>
