build-tailwind:
	rm -f static/css/tailwind.css
	./tailwindcss \
		-i src/tailwind.css \
		-o static/css/tailwind.css \
		--config src/tailwind.config.js \
		--minify \