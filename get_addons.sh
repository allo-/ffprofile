#!/bin/sh
set -e

if ! which jq >/dev/null; then
	echo "Please install jq"
	exit 1
fi

test -d addons || mkdir addons
cd addons

for addon_url in `cat ../addon_urls.txt`; do
	echo "Downloading ${addon_url}"
	wget -q "${addon_url}"
	unzip -q latest.xpi manifest.json
	addon_id=`jq ".browser_specific_settings.gecko.id // .applications.gecko.id" < manifest.json|sed 's/"//g'`
	mv latest.xpi "${addon_id}.xpi"
	rm manifest.json
done
