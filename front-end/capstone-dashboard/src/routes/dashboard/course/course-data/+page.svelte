<script>
	import { Datatable } from 'svelte-simple-datatables';
	import { writable } from 'svelte/store';
	import add from '$lib/add.svg';
	import Modal from './Modal.svelte';
	import Breadcrumbs from '$lib/Breadcrumbs.svelte';
	import { variables } from '$lib/variables';
	import csv from '$lib/csv-file-icon.svg';
	import DefaultLayout from '$lib/DefaultLayout.svelte';
	import { goto } from '$app/navigation';
	import { refresh } from '$lib/refresh.js';

	// temporary data for the table. Once the table data is fetched from the backend, this will be updated with the fetched data
	let table_data = [
		{
			id: 1,
			Sprint: 'Sprint 1',
			Start_date: '2022/09/01',
			End_date: '2022/10/01',
			File: 'Sprint1.csv'
		}
	];
	let current_course_csv = '';
	let course_csv;
	let sprint_csv;
	let sprint_Number = '';
	let sprint_start_date = '';
	let sprint_end_date = '';
	let add_or_edit = 'Add Sprint';
	let can_edit = false;
	let course_bread_crumb = '';
	let form_link = '';
	let sprint_f_name = '';
	let course_name_edit = '';
	let selected_menu_item = 0;

	// these settings are used in data table
	const settings = {
		columnFilter: true,
		rowsPerPage: 20,
		pagination: false,
		blocks: {
			searchInput: false,
			paginationButtons: false,
			paginationRowCount: false
		}
	};
	let rows = writable([]);

	let modal;
	let courseName = '';

	// use this function to submit the course csv to backend
	async function submit_course_csv() {
		if (course_csv == undefined) {
			alert('Please upload a new course file if you want to update the course file');
		} else {
			const dataArray = new FormData();
			dataArray.append('file', course_csv[0]);
			fetch(variables.basePath + '/students/' + course_name_edit + '/' + 0, {
				headers: {
					Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
				},
				method: 'POST',
				body: dataArray
			})
				.then((response) => {
					if (response.status === 401) {
						refresh();
					}
					if (response.ok) {
						get_current_course_fileName();
						alert('Course data updated successfully');
						return response;
					} else {
						throw new Error('Something went wrong');
					}
				})
				.catch((error) => {
					console.error('Error uploading course data:', error);
				});
		}
	}

	// use this function to sprint the course csv to backend
	async function submit_sprint_csv() {
		if (
			sprint_Number.value == '' ||
			sprint_start_date.value == '' ||
			sprint_end_date.value == '' ||
			sprint_csv == undefined
		) {
			alert('Please enter all required fields');
		} else {
			sprint_f_name = sprint_csv[0].name;
			const dataArray = new FormData();
			dataArray.append('file', sprint_csv[0]);

			fetch(variables.basePath + '/students/' + course_name_edit + '/' + parseInt(sprint_Number), {
				headers: {
					Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
				},
				method: 'POST',
				body: dataArray
			})
				.then((response) => {
					if (response.status === 401) {
						refresh();
					}
					if (response.ok) {
						if (add_or_edit == 'Add Sprint') {
							create_sprint();
						} else {
							update_sprint();
						}
						return response;
					} else {
						throw new Error('Something went wrong');
					}
				})
				.catch((error) => {
					console.error('Error uploading sprint data:', error);
				});

			modal.hide();
			sprint_csv = undefined;
		}
	}

	// this function is used to create a new sprint
	async function create_sprint() {
		const res = await fetch(variables.basePath + '/courses/' + course_name_edit + '/sprints', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			},
			body: JSON.stringify({
				sprint_number: parseInt(sprint_Number),
				start_date: sprint_start_date,
				end_date: sprint_end_date,
				sprint_file_name: sprint_f_name,
				forms_url: form_link
			})
		});
		if (res.ok) {
			alert('Sprint added successfully');
			get_sprint_list();
		} else {
			alert('Error ' + res.status + ' ' + res.statusText);
		}
	}

	// this functiom is used to update existing sprint
	async function update_sprint() {
		const res = await fetch(variables.basePath + '/courses/' + course_name_edit + '/sprints', {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			},
			body: JSON.stringify({
				sprint_number: parseInt(sprint_Number),
				start_date: sprint_start_date,
				end_date: sprint_end_date,
				sprint_file_name: sprint_f_name,
				forms_url: form_link
			})
		});
		if (res.ok) {
			alert("Sprint's data updated successfully");

			get_sprint_list();
		} else {
			alert('Error ' + res.status + ' ' + res.statusText);
		}
	}

	async function delete_sprint(sprint_number) {
		var spr = sprint_number;
		const res = await fetch(
			variables.basePath + '/courses/' + course_name_edit + '/sprints/' + spr,
			{
				headers: {
					Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
				},
				method: 'DELETE'
			}
		);
		if (res.ok) {
			alert('Sprint deleted successfully');
			get_sprint_list();
		} else {
			alert(res.status + ' ' + res.statusText);
		}
	}

	try {
		// getting the course name from the passed in props
		course_bread_crumb = getParameterByName('courseName');
		course_name_edit = getParameterByName('courseName');
		courseName = 'Manage ' + getParameterByName('courseName');
	} catch (error) {
		console.log('Failed to get course name');
	}

	// this function is used to get the query string parameters
	function getParameterByName(name, url) {
		if (!url) {
			url = window.location.href;
		}
		let regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$())'),
			results = regex.exec(url);

		if (!results) return null;
		if (!results[2]) return '';
		return decodeURIComponent(results[2].replace(/\+/g, ' '));
	}

	// this function is used to get sprint list from backend
	async function get_sprint_list() {
		let courseName_p_h = 'course1';

		// replace with base path.. import basepath not working on my machine - vm
		const res = await fetch(variables.basePath + '/courses/' + course_name_edit + '/sprints', {
			headers: {
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			}
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				if (response.ok) {
					return response.json();
				} else {
					throw new Error('Something went wrong');
				}
			})
			.then((data) => (table_data = data))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
	}

	// this function is used to get course csv from backend so that it can be displayed in the page
	async function get_current_course_fileName() {
		let courseName_p_h = course_name_edit;
		let course_list;

		const res = await fetch(variables.basePath + '/courses/', {
			headers: {
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			}
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				if (response.ok) {
					return response.json();
				} else {
					throw new Error('Something went wrong');
				}
			})
			.then((data) => (course_list = data))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});

		for (let i = 0; i < course_list.length; i++) {
			if (course_list[i].name === courseName_p_h) {
				current_course_csv = course_list[i].roster_file_name;
				break;
			}
		}
	}

	async function export_data() {
		const res = await fetch(variables.basePath + '/export/all/' + course_name_edit, {
			headers: {
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			},
			method: 'GET'
		});
		if (res.ok) {
			const blob = await res.blob();
			const newBlob = new Blob([blob]);
			const blolUrl = window.URL.createObjectURL(newBlob);

			const link = document.createElement('a');
			link.href = blolUrl;
			link.setAttribute('download', course_name_edit + '.xlsx');
			document.body.appendChild(link);
			link.click();
			link.parentNode.removeChild(link);

			window.URL.revokeObjectURL(blolUrl);
		} else {
			alert('Error downloading file');
		}
	}

	async function delete_course() {
		const res = await fetch(variables.basePath + '/courses/' + course_name_edit, {
			headers: {
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			},
			method: 'DELETE'
		});
		if (res.ok) {
			goto('/dashboard');
		} else {
			alert('Error deleting course');
		}
	}

	// this function opens the modal to edit a sprint
	function edit_sprint(x, start_d, end_d) {
		add_or_edit = 'Edit Sprint';
		modal.show();
		sprint_Number = x;
		sprint_start_date = start_d;
		sprint_end_date = end_d;
		can_edit = true;
	}

	// this function opens the modal to add a sprint
	function show_modal() {
		add_or_edit = 'Add Sprint';
		sprint_Number = '';
		sprint_start_date = '';
		sprint_end_date = '';
		modal.show();
		can_edit = false;
	}

	// once the user clicks on cancel button, go back to previous page
	function redirect_to_course() {
		history.back();
	}

	function get_menu_option() {
		if (selected_menu_item == 1) {
			export_data();
		} else if (selected_menu_item == 2) {
			var result = confirm('Are you sure you want to delete this course?');
			if (result) {
				delete_course();
			}
		} else if (selected_menu_item == 3) {
			var sprint_to_delete = prompt('Enter the sprint number to delete');
			if (sprint_to_delete != null) {
				delete_sprint(sprint_to_delete);
			}
		}

		selected_menu_item = 0;
	}
</script>

<DefaultLayout banner_username="Username" courseName={course_bread_crumb}>
	<section>
		<Breadcrumbs>
			<a href="/dashboard">Dashboard</a>
			<a href="/dashboard/course?course={course_bread_crumb}">{course_bread_crumb}</a>
			<p>{courseName}</p>
		</Breadcrumbs>

		<section class="course-name">
			<h1>{courseName}</h1>
		</section>
		<section class="edit-grid">
			<h3>
				Course Data <div>
					<div class="select-wrapper">
						<select
							title="Course Options"
							bind:value={selected_menu_item}
							id="menu-items"
							on:change={get_menu_option}
						>
							<option value="1">Export Data</option>
							<option value="2">Delete Course</option>
							<option value="3">Delete Sprint</option>
						</select>
					</div>
				</div>
			</h3>

			<section>
				<button disabled class="fetch-course-data"> Fetch Course data </button>
				<input
					title="Fetch course data from a link"
					class="fetch-input"
					type="text"
					placeholder="Coming Soon......."
				/>
			</section>

			<section class="course-data-input">
				<input type="file" bind:files={course_csv} accept=".csv" />
				{#await get_current_course_fileName() then data}
					<input
						class="current-course-file"
						type="text"
						placeholder={'Current file: ' + current_course_csv}
					/>
				{/await}
			</section>

			<section class="sprint-data">
				<h3>Sprint data</h3>
				<section class="data-box">
					{#await get_sprint_list()}
						<p>loading...</p>
					{:then data}
						<Datatable {settings} data={table_data} bind:dataRows={rows}>
							<thead style>
								<th data-key="sprint_number">Sprint</th>
								<th data-key="start_date">Start date</th>
								<th data-key="end_date">End date</th>
								<th data-key="sprint_file_name">File</th>
							</thead>
							<tbody>
								{#if rows}
									{#each $rows as row}
										<tr>
											<td
												class="sprint-link"
												on:click={() =>
													edit_sprint(row.sprint_number, row.start_date, row.end_date)}
												style="width: 10px;">Sprint{row.sprint_number}</td
											>
											<td style="width: 8px;">{row.start_date}</td>
											<td style="width: 8px;">{row.end_date}</td>
											<td style="width: 8px;">{row.sprint_file_name}</td>
										</tr>
									{/each}
								{/if}
							</tbody>
						</Datatable>
					{/await}
				</section>
				<section class="add-btn">
					<img on:click={() => show_modal()} src={add} alt="add button" />
					<h5>Add Sprint</h5>
					<Modal bind:this={modal}>
						<h3>{add_or_edit}</h3>
						<section class="modal-h4">
							<h4>
								*Sprint Number <input
									id="spr"
									min="1"
									bind:value={sprint_Number}
									class="sprint-name"
									type="number"
									placeholder="Sprint No."
									disabled={can_edit}
								/>
							</h4>
							<h4>
								*Start Date <input
									bind:value={sprint_start_date}
									class="sprint-start-date"
									type="date"
									placeholder="Start Date"
								/>
							</h4>
							<h4>
								*End Date <input
									bind:value={sprint_end_date}
									class="sprint-end-date"
									type="date"
									placeholder="End Date"
								/>
							</h4>
							<h4>
								Form Link <input
									bind:value={form_link}
									class="form-link"
									type="text"
									placeholder="Form url"
								/>
							</h4>

							<h4 class="sprint-file-heading">
								*
								<img class="img" src={csv} alt="csv file" /> Sprint File
								<input bind:files={sprint_csv} type="file" accept=".csv" />
							</h4>
							<section>
								<button on:click={submit_sprint_csv} class="confirm-btn-modal"> Confirm </button>

								<button on:click={() => modal.hide()} class="cancel-btn"> Close </button>
							</section>
						</section>
					</Modal>
				</section>
			</section>

			<section>
				<button on:click={submit_course_csv} class="confirm-btn"> Confirm </button>

				<button on:click={redirect_to_course} class="cancel-btn">Go Back</button>
			</section>
		</section>
	</section>
</DefaultLayout>

<style>
	/* width */
	::-webkit-scrollbar {
		width: 4px;
		height: 4px;
	}

	/* Handle */
	::-webkit-scrollbar-thumb {
		background: rgba(0, 0, 0, 0.25);
	}
	::-webkit-scrollbar-track {
		margin-top: 10px;
		margin-bottom: 10px;
	}

	/* Handle on hover */
	::-webkit-scrollbar-thumb:hover {
		background: #555;
	}
	tr:nth-of-type(odd) {
		background-color: rgb(195, 226, 201);
	}

	td {
		text-align: center;
		padding: 4px 0;
	}

	:global(body) {
		background-color: hsl(0, 0%, 90%);
	}

	.edit-grid {
		margin-left: auto;
		margin-right: auto;
		background-color: white;
		position: relative;
		border-radius: 0.5em;
		border: 00.005em solid;
		border-color: silver;
		height: auto;
		padding: 2em;
		width: fit-content;
		text-align: center;
		padding-left: 5vw;
		padding-right: 5vw;
	}
	.edit-grid > h3 {
		text-align: center;
		font-weight: 300;
	}
	.edit-grid > h3 > div {
		margin-left: 95%;
		margin-top: -1rem;
	}

	.fetch-course-data {
		margin-left: auto;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 10em;
		margin-right: -0.4rem;
	}

	.course-name {
		/* margin-top: 5.8em; */
		position: relative;
		align-items: center;
		justify-content: center;
		text-align: center;
	}

	.course-name > h1 {
		font-weight: 400;
		font-size: 1.5rem;
		text-align: center;
		margin: 1.4rem;
	}

	.fetch-input {
		margin-left: 9rem;
		overflow: visible;
		background: transparent;
		box-shadow: none;
		outline: none;
		border: none;
		border-bottom: 1px solid #3b3b3b;
		width: 20em;
	}

	.current-course-file {
		margin-left: 5rem;
		overflow: visible;
		background: transparent;
		box-shadow: none;
		outline: none;
		border: none;
		border-bottom: 1px solid #3b3b3b;
		width: 20em;
		overflow-x: scroll;
	}

	.sprint-data {
		margin-top: 3rem;
	}

	.sprint-data > h3 {
		text-align: center;
		font-weight: 300;
	}

	.sprint-link:hover {
		cursor: pointer;
	}

	.data-box {
		border-radius: 0.2em;
		border: 00.05em solid;
		border-color: #8e8e8e;
		min-width: 700px;
		max-width: 800px;
		height: 20vh;
		padding: 00.05em;
		z-index: 1;
		/* overflow: auto; */
	}

	.add-btn {
		position: relative;
		margin-top: 1rem;
		margin-left: auto;
		margin-right: auto;
		width: 30px;
		height: 30px;
	}

	.add-btn:hover {
		width: 35px;
	}

	.add-btn > h5 {
		margin-top: -0.1em;
		text-align: center;
		width: 100px;
		margin-left: -2.5em;
		font-weight: 200;
	}

	.confirm-btn {
		margin-top: 2em;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 10em;
	}

	.confirm-btn-modal {
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 10em;
		margin-left: 1.5rem;
		margin-right: auto;
	}

	.cancel-btn {
		margin-top: 4em;
		margin-left: 6vw;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 10em;
	}

	.modal-h4 {
		/* margin-top: 3rem; */
		text-align: left;
		margin-left: 12vw;
	}

	.modal-h4 :disabled {
		background-color: rgb(232, 232, 232);
	}

	.sprint-name {
		margin-top: 1rem;
		margin-left: 10rem;
		overflow: visible;
		background: transparent;
		box-shadow: none;
		outline: none;
		border: none;
		border-bottom: 1px solid #3b3b3b;
		width: 10vw;
		font-size: large;
	}

	.form-link {
		margin-left: 2.5rem;
		overflow: visible;
		background: transparent;
		box-shadow: none;
		outline: none;
		border: none;
		border-bottom: 1px solid #3b3b3b;
		width: 20vw;
	}

	.sprint-start-date {
		margin-left: 12.2rem;
		overflow: visible;
		background: transparent;
		box-shadow: none;
		outline: none;
		border: none;
		border-bottom: 1px solid #3b3b3b;
		width: 10vw;
		font-size: large;
	}

	.sprint-end-date {
		margin-left: 12.5rem;
		overflow: visible;
		background: transparent;
		box-shadow: none;
		outline: none;
		border: none;
		border-bottom: 1px solid #3b3b3b;
		width: 10vw;
		font-size: large;
	}

	input::file-selector-button {
		margin-top: 2rem;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 7em;
		margin-left: 4rem;
	}

	.course-data-input {
		margin-left: -4rem;
	}

	.modal-h4 > .sprint-file-heading {
		border: 00.05em solid;
		border-color: hsl(54, 78%, 60%);
		border-radius: 0.5em;
		height: 4rem;
		background-color: #fffbfb;
		margin-left: -12vw;
		padding: 1em;
		overflow: auto;
	}

	.modal-h4 > .sprint-file-heading > img {
		height: 1.5rem;
		width: 1.5rem;
	}

	.modal-h4 > .sprint-file-heading > input {
		margin-left: 2rem;
	}

	.data-box :global(section) {
		z-index: 0;
	}

	.img {
		margin-left: 11.1vw;
	}
	.select-wrapper {
		position: relative;
		width: 50px;
		height: 50px;
		overflow: hidden;
		scale: 0.75;
	}
	.select-wrapper:before {
		content: '\2630';
		position: absolute;
		width: 40px;
		height: 42px;
		background-color: hsl(54, 78%, 60%);
		font-size: 40px;
		line-height: 46px;
		text-align: center;
		border-radius: 5px;
		border: 1.5px solid hsl(0, 0%, 0%);
		pointer-events: none;
	}

	.select-wrapper > select {
		cursor: pointer;
		width: 50px;
		height: 50px;
		opacity: 0.00001;
	}

	.fetch-course-data:hover {
		cursor: default;
	}
</style>
