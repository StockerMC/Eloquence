<script lang="ts">
    import { FileDropzone, ProgressBar } from "@skeletonlabs/skeleton";
    import "iconify-icon";
    import { enhance } from "$app/forms";
    import { LinkedChart, LinkedLabel, LinkedValue } from "svelte-tiny-linked-charts";

    export let form;
    $: if (form) {
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
    }

    let playLoadingAnimation = false;
    let file: FileList;

    const getFillerWords = ([start, length]: [number, number]) => {
        return form?.result["transcript"].substring(start, start + length);
    };

    // Key: sentence length
    // Value: number of sentences with that length
    const sentenceLengths: Record<number, number> = {};
    let averageSentenceLength = 0;

    let mostUsedWords: Record<string, number> = {};
</script>

<div class="flex justify-center items-center flex-col p-4">
    <h1 class="mt-24 mb-12 title p-12">Eloquence</h1>
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
            >
                <svelte:fragment slot="lead">
                    <iconify-icon icon="bi:upload" class="icon"/>
                </svelte:fragment>
                <svelte:fragment slot="message">
                    <span class="font-bold">Upload a file </span>
                    <span>or drag and drop</span>
                </svelte:fragment>
                <svelte:fragment slot="meta">
                    MP3, and WAV are allowed.
                    {#if file && file?.length > 0}
                        <br/>
                        <br/>
                        <span class="font-semibold">{file?.[0].name}</span>
                    {/if}
                </svelte:fragment>
            </FileDropzone>
        </div>
        {#if playLoadingAnimation}
            <div class="w-3/4 mt-4">
                <ProgressBar value={undefined} meter="bg-primary-800"/>
            </div>
        {/if}
        <button
                on:click={() => (playLoadingAnimation = true)}
                type="submit"
                class="btn variant-filled-primary text-2xl w-3/4 mt-4"
        >
            <span class="pt-1 pb-1"> Analyse </span>
        </button>
    </form>
    {#if form?.result}
		<div class="flex gap-4">
			<div class="box-small flex flex-col gap-8 justify-center">
                <div class="flex flex-col gap-2 border-2 border-secondary-300 p-4">
                    <LinkedChart data={sentenceLengths} grow fill="#F56C67" linked="link-1" uid="link-1" on:hover/>
                    <span class="text-sm">
                        Average sentence length:
                        {averageSentenceLength.toFixed(1)} words
                    </span>
                    <span class="text-sm">
                        Sentence length:
                        <LinkedLabel linked="link-1" empty="N/A"/> words
                    </span>
                    <span class="text-sm">
                        Count:
                        <LinkedValue uid="link-1" empty="N/A"/> sentences
                    </span>
                </div>
                <div class="flex flex-col gap-2 border-2 border-secondary-300 p-4">
                    <LinkedChart data={mostUsedWords} grow fill="#F56C67" linked="link-2" uid="link-2" on:hover/>
                    <span class="text-sm">
                        Word:
                        <LinkedLabel linked="link-2" empty="N/A"/>
                    </span>
                    <span class="text-sm">
                        Count:
                        <LinkedValue uid="link-2" empty="N/A"/> times
                    </span>
                </div>
			</div>
			<div class="box-large border-2 border-secondary-300">
				<h1>
					{form.result.overall_score}
				</h1>
			</div>
			<div class="box-small border-2 border-secondary-300">
				<h1>
					{form.result.wpm}
				</h1>
			</div>
		</div>
	{/if}
    <p>
        {form?.success}
        {form?.result["transcript"]}
    </p>
    <h1>Fillers:</h1>
    <p>
        {#if form}
            {#each form.result["filler_indices"].map(getFillerWords) as word}
                <p>{word}</p>
            {/each}
        {/if}
        <!-- {form?.result.words} -->
    </p>
</div>

<style>
    .title {
        font-size: 12em;
        font-family: "MrsSaintDelafield", cursive;
    }

    .icon {
        font-size: 3rem;
    }

	.box-small {
		width: 22vw;
	}

    .box-large {
        width: 30vw;
    }
</style>
