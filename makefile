dist_dir := src/dist
client_dir := web/

clean-dist:
	rm -rf ${dist_dir}

dist: clean-dist
	cd ${client_dir} && npm run build
	mv ${client_dir}/dist ${dist_dir}

