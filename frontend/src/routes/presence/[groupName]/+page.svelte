<script>
	import { page } from '$app/stores';
	import ParticipantsTable from './ParticipantsTable.svelte';

	const groupName = $page.params.groupName;
</script>

<ParticipantsTable {groupName} />
