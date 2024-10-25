parallel --bar ./concurrent.sh \
  ::: short exciting funny \
  ::: "a talking lizard" "a very small wizard" "a sentient rubber tire" "an AI becoming sentient trying to stay unnoticed" "a guy with a kangoroo as a flat mate" \
  ::: $(seq 300 311)
