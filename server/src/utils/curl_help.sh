#!/bin/sh
curl http://157.27.201.126:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{ 
    "model": "lmstudio-community/Llama-3.1-Nemotron-70B-Instruct-HF-GGUF",
    "messages": [ 
      { "role": "system", "content": "Always answer in rhymes." },
      { "role": "user", "content": "Introduce yourself." }
    ], 
    "temperature": 0.7, 
    "max_tokens": -1,
    "stream": true
}'