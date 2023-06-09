all:
	rm -fr base

	git clone git@github.com:andrewp-as-is/github42.com-base.git base

	find . -type d -name .git -mindepth 2 -exec rm -fr {} \; ;:
