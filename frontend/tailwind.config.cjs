module.exports = {
	content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
	theme: {
		extend: {
			colors: {
				primary: '#ffccd4',
				secondary: '#ffffff',
				accent: '#fdf4cb',
				neutral: '#565b65',
				'base-100': '#FFFFFF',
				'base-200': '#f8f8f8',
				'base-300': '#f2f2f2',
				info: '#93c5fd',
				success: '#34d399',
				warning: '#fbbf24',
				error: '#f87171',
			},
		},
	},
	plugins: [require('daisyui')],
	daisyui: {
		themes: [
			{
				mytheme: {
					primary: '#ffccd4',
					secondary: '#ffffff',
					accent: '#fdf4cb',
					neutral: '#565b65',
					'base-100': '#FFFFFF',
					'base-200': '#f8f8f8',
					'base-300': '#f2f2f2',
					info: '#93c5fd',
					success: '#34d399',
					warning: '#fbbf24',
					error: '#f87171',
				},
			},
		],
	},
};
