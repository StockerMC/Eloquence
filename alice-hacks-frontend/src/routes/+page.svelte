<script lang="ts">
	import { FileDropzone, ProgressBar, ProgressRadial } from "@skeletonlabs/skeleton";
	import type { PopupSettings } from "@skeletonlabs/skeleton";
	import { popup } from "@skeletonlabs/skeleton";
	import "iconify-icon";
	import { enhance } from "$app/forms";
	import { LinkedChart, LinkedLabel, LinkedValue } from "svelte-tiny-linked-charts";
	import App from "$lib/components/App.svelte";
	import { browser } from "$app/environment";
	import { inview } from "svelte-inview";
	import type { Options } from "svelte-inview";

	let isInViewTop: boolean;
	let isInViewBottom: boolean;
	const options: Options = {
		unobserveOnEnter: false
	};

	export let form;
	$: if (form) {
		sentenceLengths = {};
		mostUsedWords = {};
		averageSentenceLength = 0;

		playLoadingAnimation = false;
		form?.result.sentence_length.map((data) => {
			if (data > 0) {
				sentenceLengths[data] = (sentenceLengths[data] || 0) + 1;
			}
		});
		for (const key of Object.keys(sentenceLengths)) {
			const intKey = parseInt(key);
			averageSentenceLength += intKey * sentenceLengths[intKey];
		}
		averageSentenceLength /= Object.values(sentenceLengths).reduce((a, b) => a + b, 0);

		for (const data of form.result.most_common_words) {
			mostUsedWords[data[0]] = data[1];
		}

		// Add fillers to set
		const fillerSet = new Set();
		for (const [start, length] of form.result.filler_indices) {
			const filler = form.result.transcript
				.substring(start, start + length)
				.replaceAll(",", "")
				.trim();
			if (!filler || filler === "") continue;
			fillerSet.add(filler);
		}
		fillersFormatted = Array.from(fillerSet).join(", ");
	}

	let playLoadingAnimation = false;
	let file: FileList;

	// Key: sentence length
	// Value: number of sentences with that length
	let sentenceLengths: Record<number, number> = {};
	let averageSentenceLength = 0;

	let mostUsedWords: Record<string, number> = {};

	const scoreToLetter = (score: number): string => {
		score *= 100;
		score = Math.round(score * 10) / 10;
		if (score < 50) return "F";
		if (score < 60) return "D";
		if (score < 75) return "C";
		if (score < 88) return "B";
		if (score < 93) return "A";
		if (score != 100) return "S";
		return "SS";
	};

	const letterColours: Record<string, string> = {
		F: "tertiary-900",
		D: "error-700",
		C: "primary-500",
		B: "warning-400",
		A: "success-600",
		S: "secondary-500"
	};

	let fillersFormatted: string;

	let observer: MutationObserver;
	if (browser) {
		observer = new MutationObserver(() => {
			scrollToElement("bottom");
		});
		observer.observe(document.body, { childList: true, subtree: true });
	}

	const scrollToElement = (id: string) => {
		const element = document.getElementById(id);
		if (element) {
			element.scrollIntoView({ behavior: "smooth" });
		}
	};

	const popupHover: PopupSettings = {
		event: "hover",
		target: "popupHover",
		placement: "top"
	};
</script>

<div class="flex justify-center items-center flex-col bg-surface-300">
	<h1 class="mt-24 mb-8 title p-12">Eloquence.</h1>
	<h2 class="text-3xl mb-12">Your words, perfected</h2>
	<div class="flex h-36 mb-24 w-screen justify-start">
		<App />
	</div>
	<form
		class="w-3/4 mt-12 mb-8 flex justify-center items-center flex-col"
		method="POST"
		use:enhance
	>
		<div class="w-3/4">
			<!--TODO: Make it darker on hover instead of lighter-->
			<FileDropzone
				name="file"
				bind:files={file}
				required
				accept="audio/*"
				enctype="multipart/form-data"
				border="border-solid"
			>
				<svelte:fragment slot="lead">
					<iconify-icon icon="bi:upload" class="icon" />
				</svelte:fragment>
				<svelte:fragment slot="message">
					<span class="font-bold">Upload a file </span>
					<span>or drag and drop</span>
				</svelte:fragment>
				<svelte:fragment slot="meta">
					MP3, and WAV are allowed.
					{#if file && file?.length > 0}
						<br />
						<br />
						<span class="font-semibold">{file?.[0].name}</span>
					{/if}
				</svelte:fragment>
			</FileDropzone>
		</div>
		{#if playLoadingAnimation}
			<div class="w-3/4 mt-4">
				<ProgressBar value={undefined} meter="bg-tertiary-500" />
			</div>
		{/if}
		<button
			on:click={() => {
				playLoadingAnimation = true;
				form = null;
			}}
			type="submit"
			class="btn variant-filled-tertiary bg-tertiary-500 text-2xl w-3/4 mt-4"
		>
			<span class="pt-1 pb-1 text-surface-50">Analyse</span>
		</button>
	</form>
	{#if form?.result}
		<button on:click={() => scrollToElement("bottom")}>
			<iconify-icon icon="ei:arrow-down" class="icon-large pt-12" />
		</button>
		<div class="bg-tertiary-900 w-full h-1 mt-48" id="bottom" />
		<div class=" pt-24 pb-24 bg-secondary-50 flex justify-center w-full">
			<div class="flex flex-col gap-32">
				<div
					class="flex gap-4 opacity-0 translate-y-64"
					use:inview={options}
					on:inview_change={(event) => {
						const { inView } = event.detail;
						isInViewTop = inView;
					}}
					class:animate={isInViewTop || isInViewBottom}
				>
					<div class="box-small flex flex-col gap-4 justify-center">
						<div class="flex flex-col card card-hover variant-glass-tertiary gap-2 p-8">
							<h1 class="font-bold text-3xl pb-2">Sentence Analysis:</h1>
							<LinkedChart
								data={sentenceLengths}
								grow
								fill="#EE93B8"
								linked="link-1"
								uid="link-1"
							/>
							<span class="text-xl">
								Average sentence length:
								{averageSentenceLength.toFixed(1)} words
							</span>
							<span class="text-xl">
								Sentence length:
								<LinkedLabel linked="link-1" empty="N/A" /> words
							</span>
							<span class="text-xl">
								Count:
								<LinkedValue uid="link-1" empty="N/A" /> sentences
							</span>
						</div>
						<div class="flex flex-col gap-2 card card-hover variant-glass-tertiary p-8">
							<h1 class="font-bold text-3xl h-full pb-2">Word Analysis:</h1>
							<LinkedChart
								data={mostUsedWords}
								grow
								fill="#EE93B8"
								linked="link-2"
								uid="link-2"
							/>
							<span class="text-xl">
								Word:
								<LinkedLabel linked="link-2" empty="N/A" />
							</span>
							<span class="text-xl">
								Count:
								<LinkedValue uid="link-2" empty="N/A" /> times
							</span>
						</div>
					</div>
					<div
						class="box-large h-full card card-hover variant-glass-tertiary p-8 flex flex-col gap-4 align-middle justify-center items-center border-4 border-tertiary-400"
					>
						<h1 class="font-bold pb-2 text-4xl">Overall Score</h1>
						<ProgressRadial
							value={form.result.overall_score * 100}
							stroke={80}
							track="stroke-secondary-100"
							fill={"fill-" + letterColours[scoreToLetter(form.result.overall_score)]}
							meter="stroke-tertiary-500"
							font={128}
							width="w-52"
						>
							{scoreToLetter(form.result.overall_score)}
						</ProgressRadial>
						<h1
							class="text-4xl font-bold text-{letterColours[
								scoreToLetter(form.result.overall_score)
							]}"
						>
							{(form.result.overall_score * 100).toFixed(2)}%
						</h1>
					</div>
					<div class="box-small card card-hover variant-glass-tertiary h-full p-8">
						<h1 class="font-bold text-3xl pb-2">Stats:</h1>
						<div class="card p-2 variant-filled-tertiary" data-popup="popupHover">
							<p class="text-sm leading-4">
								Number of words spoken in a row without fillers
							</p>
							<div class="arrow variant-filled-tertiary" />
						</div>
						<br />
						<h1 class="text-xl">
							<span class="font-semibold">Filler word count: </span>
							{form?.result.filler_count}
							<br />
							<br />
							<span class="[&>*]:pointer-events-none" use:popup={popupHover}>
								<span class="font-semibold">Highest combo: </span>
								{form?.result.max_combo} words
							</span>
							<br />
							<br />
							<span class="font-semibold">Average WPM: </span>
							{form?.result.wpm.toFixed(1)}
							<br />
							<br />
							<span class="font-semibold">Grammar mistakes: </span>
							{form?.result.grammar_mistakes}
						</h1>
					</div>
				</div>
				<div class="bg-tertiary-900 relative rule h-1" id="bottom" />
				<div
					class="flex gap-4 opacity-0 translate-y-64"
					use:inview={options}
					on:inview_change={(event) => {
						const { inView } = event.detail;
						isInViewBottom = inView;
					}}
					class:animate={isInViewBottom}
				>
					<div class="flex flex-col gap-4">
						<div class="card card-hover variant-glass-tertiary p-8 box-small">
							<h1 class="font-bold text-3xl pb-2">List Of Filler Words Detected:</h1>
							<p class="text-xl">
								{fillersFormatted === "" ? "N/A" : fillersFormatted}
							</p>
						</div>
						<div class="card card-hover variant-glass-tertiary h-full p-8 box-small">
							<h1 class="font-bold text-3xl pb-4">Transcript:</h1>
							<p class="text-xl leading-8">{form.result.transcript}</p>
						</div>
					</div>
					<div class="card card-hover variant-glass-tertiary h-full p-8 box-larger">
						<h1 class="font-bold pb-2 text-3xl leading-6">Feedback:</h1>
						{#each form.result.detailed_feedback
							.replaceAll("\\n", "\n")
							.replaceAll("\\t", "\t")
							.replaceAll("\\r", "\r")
							.replaceAll("\\'", "'")
							.replaceAll("[", "")
							.replaceAll("]", "")
							.replaceAll('\\"', '"')
							.replaceAll("\\\\", "\\")
							.split("\n") as line}
							{#if !isNaN(parseInt(line.trim().charAt(0))) || line
									.toLowerCase()
									.startsWith("overall")}
								<br />
								<p
									class:font-semibold={!isNaN(parseInt(line.trim().charAt(0)))}
									class="text-xl leading-8"
								>
									{line}
								</p>
							{:else if line.trim().charAt(0) === "-"}
								<p class="text-xl leading-8">{"•" + line.substring(1)}</p>
							{/if}
						{/each}
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.title {
		font-size: 8em;
	}

	.icon {
		font-size: 3rem;
	}

	.icon-large {
		font-size: 5rem;
	}

	.box-small {
		width: 22vw;
	}

	.box-large {
		width: 30vw;
	}

	.box-larger {
		width: 53vw;
	}

	.rule {
		width: 100%;
	}

	.animate {
		transition: all 0.5s ease-in-out;
		opacity: 1;
		transform: none;
	}
</style>
