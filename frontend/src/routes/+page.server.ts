import type { Actions } from "./$types";
import { SECRET_BACKEND_SERVER_ADDRESS } from "$env/static/private";

interface Response {
	transcript: string;
	filler_indices: [number, number][];
	filler_count: number;
	wpm: number;
	words: string;
	most_common_words: [string, number][];
	sentence_length: number[];
	overall_score: number;
	detailed_feedback: string;
	duration: number;
	max_combo: number;
	full_combo: boolean;
	grammar_mistakes: number;
}

export const actions = {
	default: async (event) => {
		const formData = await event.request.formData();
		const file = formData.get("file") as File;

		const postFormData = new FormData();
		postFormData.append("input", file);

		const response = await fetch(`${SECRET_BACKEND_SERVER_ADDRESS}/api`, {
			method: "post",
			body: postFormData
		});

		const json: Response = await response.json();

		return {
			success: true,
			result: json
		};
	}
} satisfies Actions;
