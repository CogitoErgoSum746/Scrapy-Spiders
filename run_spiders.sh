#!/bin/bash

countries=( 'aed' 'usd' 'inr' 'aud' 'afn' 'all' 'amd' 'ang' 'aoa' 'ars' 'awg' 'azn' 'bam' 'bbd' 'bdt' 'bgn' 'bhd' 'bif' 'bmd' 'bnd' 'bob' 'brl' 'bsd' 'btn' 'bwp' 'byn' 'bzd' 'cad' 'cdf' 'chf' 'clf' 'clp' 'cny' 'cop' 'crc' 'cuc' 'cup' 'cve' 'czk' 'djf' 'dkk' 'dop' 'dzd' 'egp' 'ern' 'etb' 'eur' 'fjd' 'fkp' 'gbp' 'gel' 'ggp' 'ghs' 'gip' 'gmd' 'gnf' 'gtq' 'gyd' 'hkd' 'hnl' 'hrk' 'htg' 'huf' 'idr' 'ils' 'imp' 'isk' 'jep' 'jmd' 'jod' 'jpy' 'kes' 'kgs' 'khr' 'kir' 'kmf' 'krw' 'kwd' 'kyd' 'kzt' 'lak' 'lbp' 'lkr' 'lrd' 'lsl' 'ltl' 'lvl' 'lyd' 'mad' 'mdl' 'mga' 'mkd' 'mmk' 'mnt' 'mop' 'mro' 'mur' 'mvr' 'mwk' 'mxn' 'myr' 'mzn' 'nad' 'ngn' 'nio' 'nok' 'npr' 'nzd' 'omr' 'pab' 'pen' 'pgk' 'php' 'pkr' 'pln' 'pyg' 'qar' 'ron' 'rsd' 'rub' 'rwf' 'sar' 'sbd' 'scr' 'sdg' 'sek' 'sgd' 'shp' 'sll' 'sos' 'spl' 'srd' 'std' 'svc' 'syp' 'szl' 'thb' 'tjs' 'tmt' 'tnd' 'top' 'try' 'ttd' 'tvd' 'twd' 'tzs' 'uah' 'ugx' 'uyu' 'uzs' 'vef' 'vnd' 'vuv' 'wst' 'xaf' 'xag' 'xau' 'xcd' 'xdr' 'xof' 'xpd' 'xpf' 'xpt' 'yer' 'zar' 'zmk' 'zmw' 'zwl' )

start_urls=()

# Generate the start URLs
for ((i=0; i<${#countries[@]}; i++)); do
    for ((j=0; j<${#countries[@]}; j++)); do
        if [[ $i != $j ]]; then
            start_url="https://wise.com/in/currency-converter/${countries[i]}-to-${countries[j]}-rate?"
            start_urls+=("$start_url")
        fi
    done
done

# Define twelve new variables
start_url_1=("${start_urls[@]:0:10}")
start_url_2=("${start_urls[@]:2338:2338}")
start_url_3=("${start_urls[@]:4676:2338}")
start_url_4=("${start_urls[@]:7014:2338}")
start_url_5=("${start_urls[@]:9352:2338}")
start_url_6=("${start_urls[@]:11690:2338}")
start_url_7=("${start_urls[@]:14028:2338}")
start_url_8=("${start_urls[@]:16366:2338}")
start_url_9=("${start_urls[@]:18704:2338}")
start_url_10=("${start_urls[@]:21042:2338}")
start_url_11=("${start_urls[@]:23380:2338}")
start_url_12=("${start_urls[@]:25718}")

# Convert each new list to a comma-separated string
start_url_1=$(IFS=, ; echo "${start_url_1[*]}")
start_url_2=$(IFS=, ; echo "${start_url_2[*]}")
start_url_3=$(IFS=, ; echo "${start_url_3[*]}")
start_url_4=$(IFS=, ; echo "${start_url_4[*]}")
start_url_5=$(IFS=, ; echo "${start_url_5[*]}")
start_url_6=$(IFS=, ; echo "${start_url_6[*]}")
start_url_7=$(IFS=, ; echo "${start_url_7[*]}")
start_url_8=$(IFS=, ; echo "${start_url_8[*]}")
start_url_9=$(IFS=, ; echo "${start_url_9[*]}")
start_url_10=$(IFS=, ; echo "${start_url_10[*]}")
start_url_11=$(IFS=, ; echo "${start_url_11[*]}")
start_url_12=$(IFS=, ; echo "${start_url_12[*]}")

# Function to run the scraper with a specific start URL and handle potential errors
run_scraper() {
  start_url="$1"
  if [[ -z "$start_url" ]]; then
    echo "Error: Empty start URL provided."
    return 1
  fi
  python3 test.py "$start_url" || echo "Error: Scraper failed."
  sleep 5  # Wait for 5 seconds before next run
}

# Run the scraper for each variable sequentially
start_url_vars=(
  "start_url_1" "start_url_2" "start_url_3" "start_url_4" "start_url_5"
  "start_url_6" "start_url_7" "start_url_8" "start_url_9" "start_url_10"
  "start_url_11" "start_url_12"
)

for var in "${start_url_vars[@]}"; do
  run_scraper "${!var}"  # Use indirect expansion to access variable value
done

echo "All scraping tasks completed."

# gnome-terminal -- python3 test.py "$start_url_1"
# gnome-terminal -- python3 test.py "$start_url_2"
# gnome-terminal -- python3 test.py "$start_url_3"
# gnome-terminal -- python3 test.py "$start_url_4"
# gnome-terminal -- python3 test.py "$start_url_5"
# gnome-terminal -- python3 test.py "$start_url_6"
# gnome-terminal -- python3 test.py "$start_url_7"
# gnome-terminal -- python3 test.py "$start_url_8"
# gnome-terminal -- python3 test.py "$start_url_9"
# gnome-terminal -- python3 test.py "$start_url_10"
# gnome-terminal -- python3 test.py "$start_url_11"
# gnome-terminal -- python3 test.py "$start_url_12"

# python3 test.py "$start_url_1"