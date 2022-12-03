<script>
	export const quick_panel = [
		{ page_name: 'Teams', link: '/dashboard/course' },
		{ page_name: 'Students', link: '/dashboard/students' }
	];
</script>

<section class="quick-access">
	<a href="/dashboard"> Dashboard</a>
	{#each quick_panel as quick_link}
		>
		<a href={quick_link.link} target="_self"> {quick_link.page_name} </a>
	{/each}
</section>

<style>
	.quick-access {
		height: auto;
		width: 100vw;
		position: fixed;
		background-color: hsl(0, 0%, 100%);
		z-index: 0;
		padding: 0.5em;
		border: 1px solid rgb(207, 206, 206);
		margin-left: 5em;
		z-index: 2;
		margin-top: 4em;
	}

	.quick-access > a {
		text-decoration: none;
		color: black;
	}
</style>
