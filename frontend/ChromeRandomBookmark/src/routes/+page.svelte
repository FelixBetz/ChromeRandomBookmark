<script lang="ts">
	import { onMount } from 'svelte';
	import { Row, Col, Container, Button, FormGroup, Label, Input } from 'sveltestrap/src';

	interface Folder {
		name: string;
		url_ids: number[];
	}

	interface Url {
		date_added: number;
		date_last_used: number;
		id: number;
		name: string;
		url: string;
	}

	interface Bookmarks {
		folders: Folder[];
		urls: Url[];
	}

	const API_URL = 'http://localhost:8080/api/';

	let urls: Url[] = [];
	let folders: Folder[] = [];

	let numTabs = 1;

	async function getBookmarks(): Promise<Bookmarks | undefined> {
		const response = await fetch(API_URL + 'bookmarks')
			.then((res) => res.json())
			.then((res: Bookmarks) => res)
			.catch((error: Error) => {
				console.log(error);
				return undefined;
			});
		return response;
	}

	function getRandomInt(max: number): number {
		return Math.floor(Math.random() * max);
	}

	function onClickOpenRandomBookmark(numTabs: number) {
		let numBookmarks = urls.length;
		if (numBookmarks == 0) {
			return;
		}
		for (let i = 0; i < numTabs; i++) {
			console.log('test');
			window.open(urls[getRandomInt(numBookmarks)].url, '_blank');
		}
	}

	function getUrlById(id: number): Url | null {
		for (let i = 0; i < urls.length; i++) {
			if (urls[i].id == id) {
				return urls[i];
			}
		}
		return null;
	}

	onMount(async () => {
		let bookmarks = await getBookmarks();
		if (bookmarks != undefined) {
			urls = bookmarks.urls;
			folders = bookmarks.folders;
		}
	});
</script>

<Container style="padding: 10px;">
	<Row>
		<Col sm="3">
			<FormGroup>
				<Label for="exampleNumber">Number</Label>
				<Input
					type="number"
					name="number"
					id="exampleNumber"
					placeholder="number placeholder"
					bind:value={numTabs}
				/>
			</FormGroup>
			<Button block color="primary" on:click={() => onClickOpenRandomBookmark(numTabs)}>
				Open Random Bookmarks</Button
			>
		</Col>
	</Row>
	<Row style="margin-top: 50px;">
		<Col>
			<ul>
				{#each urls as url}
					<li><a target="_blank" href={url.url}>{url.name}</a></li>
				{/each}
			</ul>
		</Col>
		<Col>
			<ul>
				{#each folders as folder}
					<li>{folder.name}</li>
					<ul>
						{#each folder.url_ids as id}
							<li>{getUrlById(id)?.name}</li>
						{/each}
					</ul>
				{/each}
			</ul>
		</Col>
	</Row>
</Container>

<style>
</style>
