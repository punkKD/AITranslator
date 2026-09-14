import os
import cohere 

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))