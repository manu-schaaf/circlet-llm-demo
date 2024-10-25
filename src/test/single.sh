_filename=$(echo "$2" | base64);
_filename="output/l=${1}-w=${3}-t=$_filename.json";
_prompt="Here is a $1 story about $2 with at least $3 words: ";
curl http://gondor.hucompute.org:11434/api/generate -o "$_filename" -d '{
  "model": "nemotron:latest",
  "prompt": "'$_prompt'"
}';
