<script>
	export let name = 'Manage Course';
	export let url = '';

	function open_page() {
		window.location.href = url;
	}
</script>

<button on:click={open_page} class="edit-button">
	{name}
</button>

<style>
	.edit-button {
		margin-left: calc(100% - 12rem);
		width: 7rem;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		margin-top: 1rem;
		position: relative;
		z-index: 0;
	}
</style>
