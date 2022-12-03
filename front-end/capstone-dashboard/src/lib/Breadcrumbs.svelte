<section class="breadcrumbs">
	<slot />
</section>

<style>
	.breadcrumbs {
		display: flex;
		align-items: center;

		margin: 0;
		padding-left: 1rem;
		height: 2.1rem;

		background-color: white;
	}

	.breadcrumbs > :global(*) {
		color: hsl(175, 55%, 35%);
		text-decoration: none;
		mask-content: content-box;
		font-size: 12pt;
	}

	.breadcrumbs > :global(*)::after {
		margin: 0 0.3rem;
		content: '>';
		color: black;
	}

	.breadcrumbs > :global(:last-child)::after {
		content: '';
	}
</style>
