<script>
	import { page } from '$app/stores';
	import ParticipantsTable from './ParticipantsTable.svelte';

	export let data;

	const groupName = $page.params.groupName;
</script>

<ParticipantsTable participantsData={data.participantsData} />
