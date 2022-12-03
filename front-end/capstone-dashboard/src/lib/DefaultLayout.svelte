<script>
	import Banner from '$lib/Banner.svelte';
	import Navbar from '$lib/Navbar.svelte';
	import { onMount } from 'svelte';

	export let show_banner = true;
	export let show_navbar = true;

	export let banner_has_icon = false;
	export let banner_title = 'Capstone Dashboard';
	export let banner_username = '';

	export let courseName = '';

	onMount(() => {
		banner_username = window.localStorage.getItem('username') || '';
	});
</script>

<main>
	{#if show_banner}
		<div class="banner">
			<Banner has_icon={banner_has_icon} header={banner_title} username={banner_username} />
		</div>
	{/if}
	{#if show_navbar}
		<div class="navbar">
			<Navbar>
				<a href="/dashboard/course?course={courseName}"><span>Course</span></a>
				<a href="/dashboard/teams?course={courseName}"><span>Teams</span></a>
				<a href="/dashboard/students?course={courseName}"><span>Students</span></a>
			</Navbar>
		</div>
	{/if}
	<section>
		<slot />
	</section>
</main>

{#if show_navbar}
	<style>
		main {
			display: grid;
			grid-template-areas:
				'banner banner'
				'nav main';
			grid-template-columns: 7rem 1fr;
			grid-template-rows: 4rem 1fr;
			min-height: 100vh;
			max-width: 100%;

			background-color: hsl(0, 0%, 90%);
		}

		main > .banner {
			grid-area: banner;
		}

		main > .navbar {
			grid-area: nav;
		}

		/* Main Content */
		main > section {
			grid-area: main;
			padding-bottom: 1rem;
		}
	</style>
{:else}
	<style>
		main {
			min-height: 100%;
			max-width: 100%;
			background-color: hsl(0, 0%, 90%);
		}
	</style>
{/if}
