/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      gridTemplateColumns: {
        mobileGrid: 'repeat(auto-fill, minmax(100px, 1fr))',
        WebGrid: 'repeat(auto-fill, minmax(195px, 1fr))',
        watchingMobileGrid: 'repeat(auto-fill, minmax(164px, 1fr))',
        watchingWebGrid: 'repeat(auto-fill, minmax(320px, 1fr))'
      },
      aspectRatio: {
        'poster': '800 / 1200',
        'backdrop': '314 / 216'
      },
      transitionProperty: {
        'width': 'width'
      }
    },
  },
  plugins: [],
}
