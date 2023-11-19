import type { CustomThemeConfig } from "@skeletonlabs/tw-plugin";

export const theme: CustomThemeConfig = {
	name: "theme",
	properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `system-ui`,
		"--theme-font-family-heading": `system-ui`,
		"--theme-font-color-base": "0 0 0",
		"--theme-font-color-dark": "255 255 255",
		"--theme-rounded-base": "12px",
		"--theme-rounded-container": "8px",
		"--theme-border-base": "2px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "0 0 0",
		"--on-secondary": "0 0 0",
		"--on-tertiary": "0 0 0",
		"--on-success": "0 0 0",
		"--on-warning": "0 0 0",
		"--on-error": "255 255 255",
		"--on-surface": "255 255 255",
		// =~= Theme Colors  =~=
		// primary | #8391d5
		"--color-primary-50": "236 239 249", // #eceff9
		"--color-primary-100": "230 233 247", // #e6e9f7
		"--color-primary-200": "224 228 245", // #e0e4f5
		"--color-primary-300": "205 211 238", // #cdd3ee
		"--color-primary-400": "168 178 226", // #a8b2e2
		"--color-primary-500": "131 145 213", // #8391d5
		"--color-primary-600": "118 131 192", // #7683c0
		"--color-primary-700": "98 109 160", // #626da0
		"--color-primary-800": "79 87 128", // #4f5780
		"--color-primary-900": "64 71 104", // #404768
		// secondary | #f56c67
		"--color-secondary-50": "254 233 232", // #fee9e8
		"--color-secondary-100": "253 226 225", // #fde2e1
		"--color-secondary-200": "253 218 217", // #fddad9
		"--color-secondary-300": "251 196 194", // #fbc4c2
		"--color-secondary-400": "248 152 149", // #f89895
		"--color-secondary-500": "245 108 103", // #f56c67
		"--color-secondary-600": "221 97 93", // #dd615d
		"--color-secondary-700": "184 81 77", // #b8514d
		"--color-secondary-800": "147 65 62", // #93413e
		"--color-secondary-900": "120 53 50", // #783532
		// tertiary | #ee93b8
		"--color-tertiary-50": "252 239 244", // #fceff4
		"--color-tertiary-100": "252 233 241", // #fce9f1
		"--color-tertiary-200": "251 228 237", // #fbe4ed
		"--color-tertiary-300": "248 212 227", // #f8d4e3
		"--color-tertiary-400": "243 179 205", // #f3b3cd
		"--color-tertiary-500": "238 147 184", // #ee93b8
		"--color-tertiary-600": "214 132 166", // #d684a6
		"--color-tertiary-700": "179 110 138", // #b36e8a
		"--color-tertiary-800": "143 88 110", // #8f586e
		"--color-tertiary-900": "117 72 90", // #75485a
		// success | #a2ee93
		"--color-success-50": "241 252 239", // #f1fcef
		"--color-success-100": "236 252 233", // #ecfce9
		"--color-success-200": "232 251 228", // #e8fbe4
		"--color-success-300": "218 248 212", // #daf8d4
		"--color-success-400": "190 243 179", // #bef3b3
		"--color-success-500": "162 238 147", // #a2ee93
		"--color-success-600": "146 214 132", // #92d684
		"--color-success-700": "122 179 110", // #7ab36e
		"--color-success-800": "97 143 88", // #618f58
		"--color-success-900": "79 117 72", // #4f7548
		// warning | #e3614f
		"--color-warning-50": "251 231 229", // #fbe7e5
		"--color-warning-100": "249 223 220", // #f9dfdc
		"--color-warning-200": "248 216 211", // #f8d8d3
		"--color-warning-300": "244 192 185", // #f4c0b9
		"--color-warning-400": "235 144 132", // #eb9084
		"--color-warning-500": "227 97 79", // #e3614f
		"--color-warning-600": "204 87 71", // #cc5747
		"--color-warning-700": "170 73 59", // #aa493b
		"--color-warning-800": "136 58 47", // #883a2f
		"--color-warning-900": "111 48 39", // #6f3027
		// error | #d93d27
		"--color-error-50": "249 226 223", // #f9e2df
		"--color-error-100": "247 216 212", // #f7d8d4
		"--color-error-200": "246 207 201", // #f6cfc9
		"--color-error-300": "240 177 169", // #f0b1a9
		"--color-error-400": "228 119 104", // #e47768
		"--color-error-500": "217 61 39", // #d93d27
		"--color-error-600": "195 55 35", // #c33723
		"--color-error-700": "163 46 29", // #a32e1d
		"--color-error-800": "130 37 23", // #822517
		"--color-error-900": "106 30 19", // #6a1e13
		// surface | #d1b0a3
		// 253, 226, 225
		"--color-surface-50": "248 243 241", // #f8f3f1
		"--color-surface-100": "246 239 237", // #f6efed
		"--color-surface-200": "244 235 232", // #f4ebe8
		"--color-surface-300": "255, 239, 239", // #fde2e1
		"--color-surface-400": "223 200 191", // #dfc8bf
		"--color-surface-500": "209 176 163", // #d1b0a3
		"--color-surface-600": "188 158 147", // #bc9e93
		"--color-surface-700": "157 132 122", // #9d847a
		"--color-surface-800": "125 106 98", // #7d6a62
		"--color-surface-900": "102 86 80" // #665650
	}
};
